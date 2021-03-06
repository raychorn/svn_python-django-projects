import testenv; testenv.configure_for_tests()
import gc
from sqlalchemy.orm import mapper, relation, create_session, clear_mappers, sessionmaker
from sqlalchemy.orm.mapper import _mapper_registry
from sqlalchemy.orm.session import _sessions
import operator
from testlib import testing
from testlib.sa import MetaData, Table, Column, Integer, String, ForeignKey, PickleType
import sqlalchemy as sa
from sqlalchemy.sql import column
from orm import _base


class A(_base.ComparableEntity):
    pass
class B(_base.ComparableEntity):
    pass

def profile_memory(func):
    # run the test 50 times.  if length of gc.get_objects()
    # keeps growing, assert false
    def profile(*args):
        gc.collect()
        samples = [0 for x in range(0, 50)]
        for x in range(0, 50):
            func(*args)
            gc.collect()
            samples[x] = len(gc.get_objects())
        print "sample gc sizes:", samples

        assert len(_sessions) == 0
        
        for x in samples[-4:]:
            if x != samples[-5]:
                flatline = False
                break
        else:
            flatline = True

        if not flatline and samples[-1] > samples[0]:  # object count is bigger than when it started
            for x in samples[1:-2]:
                if x > samples[-1]:     # see if a spike bigger than the endpoint exists
                    break
            else:
                assert False, repr(samples) + " " + repr(flatline)

    return profile

def assert_no_mappers():
    clear_mappers()
    gc.collect()
    assert len(_mapper_registry) == 0

class EnsureZeroed(_base.ORMTest):
    def setUp(self):
        _sessions.clear()
        _mapper_registry.clear()

class MemUsageTest(EnsureZeroed):
    
    # ensure a pure growing test trips the assertion
    @testing.fails_if(lambda:True)
    def test_fixture(self):
        class Foo(object):
            pass
            
        x = []
        @profile_memory
        def go():
            x[-1:] = [Foo(), Foo(), Foo(), Foo(), Foo(), Foo()]
        go()
            
    def test_session(self):
        metadata = MetaData(testing.db)

        table1 = Table("mytable", metadata,
            Column('col1', Integer, primary_key=True),
            Column('col2', String(30)))

        table2 = Table("mytable2", metadata,
            Column('col1', Integer, primary_key=True),
            Column('col2', String(30)),
            Column('col3', Integer, ForeignKey("mytable.col1")))

        metadata.create_all()

        m1 = mapper(A, table1, properties={
            "bs":relation(B, cascade="all, delete", order_by=table2.c.col1)},
            order_by=table1.c.col1)
        m2 = mapper(B, table2)

        m3 = mapper(A, table1, non_primary=True)

        @profile_memory
        def go():
            sess = create_session()
            a1 = A(col2="a1")
            a2 = A(col2="a2")
            a3 = A(col2="a3")
            a1.bs.append(B(col2="b1"))
            a1.bs.append(B(col2="b2"))
            a3.bs.append(B(col2="b3"))
            for x in [a1,a2,a3]:
                sess.add(x)
            sess.flush()
            sess.expunge_all()

            alist = sess.query(A).all()
            self.assertEquals(
                [
                    A(col2="a1", bs=[B(col2="b1"), B(col2="b2")]),
                    A(col2="a2", bs=[]),
                    A(col2="a3", bs=[B(col2="b3")])
                ],
                alist)

            for a in alist:
                sess.delete(a)
            sess.flush()
        go()

        metadata.drop_all()
        del m1, m2, m3
        assert_no_mappers()

    def test_mapper_reset(self):
        metadata = MetaData(testing.db)

        table1 = Table("mytable", metadata,
            Column('col1', Integer, primary_key=True),
            Column('col2', String(30)))

        table2 = Table("mytable2", metadata,
            Column('col1', Integer, primary_key=True),
            Column('col2', String(30)),
            Column('col3', Integer, ForeignKey("mytable.col1")))

        @profile_memory
        def go():
            m1 = mapper(A, table1, properties={
                "bs":relation(B, order_by=table2.c.col1)
            })
            m2 = mapper(B, table2)

            m3 = mapper(A, table1, non_primary=True)

            sess = create_session()
            a1 = A(col2="a1")
            a2 = A(col2="a2")
            a3 = A(col2="a3")
            a1.bs.append(B(col2="b1"))
            a1.bs.append(B(col2="b2"))
            a3.bs.append(B(col2="b3"))
            for x in [a1,a2,a3]:
                sess.add(x)
            sess.flush()
            sess.expunge_all()

            alist = sess.query(A).order_by(A.col1).all()
            self.assertEquals(
                [
                    A(col2="a1", bs=[B(col2="b1"), B(col2="b2")]),
                    A(col2="a2", bs=[]),
                    A(col2="a3", bs=[B(col2="b3")])
                ],
                alist)

            for a in alist:
                sess.delete(a)
            sess.flush()
            sess.close()
            clear_mappers()

        metadata.create_all()
        try:
            go()
        finally:
            metadata.drop_all()
        assert_no_mappers()

    def test_with_inheritance(self):
        metadata = MetaData(testing.db)

        table1 = Table("mytable", metadata,
            Column('col1', Integer, primary_key=True),
            Column('col2', String(30))
            )

        table2 = Table("mytable2", metadata,
            Column('col1', Integer, ForeignKey('mytable.col1'),
                   primary_key=True),
            Column('col3', String(30)),
            )

        @profile_memory
        def go():
            class A(_base.ComparableEntity):
                pass
            class B(A):
                pass

            mapper(A, table1,
                   polymorphic_on=table1.c.col2,
                   polymorphic_identity='a')
            mapper(B, table2,
                   inherits=A,
                   polymorphic_identity='b')

            sess = create_session()
            a1 = A()
            a2 = A()
            b1 = B(col3='b1')
            b2 = B(col3='b2')
            for x in [a1,a2,b1, b2]:
                sess.add(x)
            sess.flush()
            sess.expunge_all()

            alist = sess.query(A).order_by(A.col1).all()
            self.assertEquals(
                [
                    A(), A(), B(col3='b1'), B(col3='b2')
                ],
                alist)

            for a in alist:
                sess.delete(a)
            sess.flush()

            # dont need to clear_mappers()
            del B
            del A

        metadata.create_all()
        try:
            go()
        finally:
            metadata.drop_all()
        assert_no_mappers()

    def test_with_manytomany(self):
        metadata = MetaData(testing.db)

        table1 = Table("mytable", metadata,
            Column('col1', Integer, primary_key=True),
            Column('col2', String(30))
            )

        table2 = Table("mytable2", metadata,
            Column('col1', Integer, primary_key=True),
            Column('col2', String(30)),
            )

        table3 = Table('t1tot2', metadata,
            Column('t1', Integer, ForeignKey('mytable.col1')),
            Column('t2', Integer, ForeignKey('mytable2.col1')),
            )

        @profile_memory
        def go():
            class A(_base.ComparableEntity):
                pass
            class B(_base.ComparableEntity):
                pass

            mapper(A, table1, properties={
                'bs':relation(B, secondary=table3, backref='as', order_by=table3.c.t1)
            })
            mapper(B, table2)

            sess = create_session()
            a1 = A(col2='a1')
            a2 = A(col2='a2')
            b1 = B(col2='b1')
            b2 = B(col2='b2')
            a1.bs.append(b1)
            a2.bs.append(b2)
            for x in [a1,a2]:
                sess.add(x)
            sess.flush()
            sess.expunge_all()

            alist = sess.query(A).order_by(A.col1).all()
            self.assertEquals(
                [
                    A(bs=[B(col2='b1')]), A(bs=[B(col2='b2')])
                ],
                alist)

            for a in alist:
                sess.delete(a)
            sess.flush()

            # dont need to clear_mappers()
            del B
            del A

        metadata.create_all()
        try:
            go()
        finally:
            metadata.drop_all()
        assert_no_mappers()

    def test_join_cache(self):
        metadata = MetaData(testing.db)

        table1 = Table("table1", metadata,
            Column('id', Integer, primary_key=True),
            Column('data', String(30))
            )

        table2 = Table("table2", metadata,
            Column('id', Integer, primary_key=True),
            Column('data', String(30)),
            Column('t1id', Integer, ForeignKey('table1.id'))
            )
        
        class Foo(object):
            pass
            
        class Bar(object):
            pass
            
        mapper(Foo, table1, properties={
            'bars':relation(mapper(Bar, table2))
        })
        metadata.create_all()

        session = sessionmaker()
        
        @profile_memory
        def go():
            s = table2.select()
            sess = session()
            sess.query(Foo).join((s, Foo.bars)).all()
            sess.rollback()
        try:
            go()
        finally:
            metadata.drop_all()
            
            
    def test_mutable_identity(self):
        metadata = MetaData(testing.db)

        table1 = Table("mytable", metadata,
            Column('col1', Integer, primary_key=True),
            Column('col2', PickleType(comparator=operator.eq))
            )
        
        class Foo(object):
            def __init__(self, col2):
                self.col2 = col2
        
        mapper(Foo, table1)
        metadata.create_all()
        
        session = sessionmaker()()
        
        def go():
            obj = [
                Foo({'a':1}),
                Foo({'b':1}),
                Foo({'c':1}),
                Foo({'d':1}),
                Foo({'e':1}),
                Foo({'f':1}),
                Foo({'g':1}),
                Foo({'h':1}),
                Foo({'i':1}),
                Foo({'j':1}),
                Foo({'k':1}),
                Foo({'l':1}),
            ]
            
            session.add_all(obj)
            session.commit()
            
            testing.eq_(len(session.identity_map._mutable_attrs), 12)
            testing.eq_(len(session.identity_map), 12)
            obj = None
            gc.collect()
            testing.eq_(len(session.identity_map._mutable_attrs), 0)
            testing.eq_(len(session.identity_map), 0)
            
        try:
            go()
        finally:
            metadata.drop_all()

    def test_type_compile(self):
        from sqlalchemy.databases.sqlite import SQLiteDialect
        cast = sa.cast(column('x'), sa.Integer)
        @profile_memory
        def go():
            dialect = SQLiteDialect()
            cast.compile(dialect=dialect)
        go()
        
if __name__ == '__main__':
    testenv.main()
