import testenv; testenv.configure_for_tests()
import datetime
from sqlalchemy import *
from sqlalchemy.sql import table, column
from sqlalchemy import databases, sql, util
from sqlalchemy.sql.compiler import BIND_TEMPLATES
from sqlalchemy.engine import default
from testlib.engines import all_dialects
from sqlalchemy import types as sqltypes
from testlib import *
from sqlalchemy.sql.functions import GenericFunction
from testlib.testing import eq_
from decimal import Decimal as _python_Decimal

from sqlalchemy.databases import *

# FIXME!
dialects = [d for d in all_dialects() if d.name not in ('access', 'informix')]


class CompileTest(TestBase, AssertsCompiledSQL):
    def test_compile(self):
        for dialect in dialects:
            bindtemplate = BIND_TEMPLATES[dialect.paramstyle]
            self.assert_compile(func.current_timestamp(), "CURRENT_TIMESTAMP", dialect=dialect)
            self.assert_compile(func.localtime(), "LOCALTIME", dialect=dialect)
            if isinstance(dialect, firebird.dialect):
                self.assert_compile(func.nosuchfunction(), "nosuchfunction", dialect=dialect)
            else:
                self.assert_compile(func.nosuchfunction(), "nosuchfunction()", dialect=dialect)
            
            # test generic function compile    
            class fake_func(GenericFunction):
                __return_type__ = sqltypes.Integer

                def __init__(self, arg, **kwargs):
                    GenericFunction.__init__(self, args=[arg], **kwargs)
                
            self.assert_compile(fake_func('foo'), "fake_func(%s)" % bindtemplate % {'name':'param_1', 'position':1}, dialect=dialect)
            
    def test_use_labels(self):
        self.assert_compile(select([func.foo()], use_labels=True), 
            "SELECT foo() AS foo_1"
        )
    def test_underscores(self):
        self.assert_compile(func.if_(), "if()")
        
    def test_generic_now(self):
        assert isinstance(func.now().type, sqltypes.DateTime)

        for ret, dialect in [
            ('CURRENT_TIMESTAMP', sqlite.dialect()),
            ('now()', postgres.dialect()),
            ('now()', mysql.dialect()),
            ('CURRENT_TIMESTAMP', oracle.dialect())
        ]:
            self.assert_compile(func.now(), ret, dialect=dialect)

    def test_generic_random(self):
        assert func.random().type == sqltypes.NULLTYPE
        assert isinstance(func.random(type_=Integer).type, Integer)

        for ret, dialect in [
            ('random()', sqlite.dialect()),
            ('random()', postgres.dialect()),
            ('rand()', mysql.dialect()),
            ('random()', oracle.dialect())
        ]:
            self.assert_compile(func.random(), ret, dialect=dialect)

    def test_generic_count(self):
        assert isinstance(func.count().type, sqltypes.Integer)

        self.assert_compile(func.count(), 'count(*)')
        self.assert_compile(func.count(1), 'count(:param_1)')
        c = column('abc')
        self.assert_compile(func.count(c), 'count(abc)')

    def test_constructor(self):
        try:
            func.current_timestamp('somearg')
            assert False
        except TypeError:
            assert True

        try:
            func.char_length('a', 'b')
            assert False
        except TypeError:
            assert True

        try:
            func.char_length()
            assert False
        except TypeError:
            assert True

    def test_return_type_detection(self):
        
        for fn in [func.coalesce, func.max, func.min, func.sum]:
            for args, type_ in [
                            ((datetime.date(2007, 10, 5), datetime.date(2005, 10, 15)), sqltypes.Date),
                            ((3, 5), sqltypes.Integer),
                            ((_python_Decimal(3), _python_Decimal(5)), sqltypes.Numeric),
                            (("foo", "bar"), sqltypes.String),
                            ((datetime.datetime(2007, 10, 5, 8, 3, 34), datetime.datetime(2005, 10, 15, 14, 45, 33)), sqltypes.DateTime)
                        ]:
                assert isinstance(fn(*args).type, type_), "%s / %s" % (fn(), type_)
        
        assert isinstance(func.concat("foo", "bar").type, sqltypes.String)


    def test_assorted(self):
        table1 = table('mytable',
            column('myid', Integer),
        )

        table2 = table(
            'myothertable',
            column('otherid', Integer),
        )

        # test an expression with a function
        self.assert_compile(func.lala(3, 4, literal("five"), table1.c.myid) * table2.c.otherid,
            "lala(:lala_1, :lala_2, :param_1, mytable.myid) * myothertable.otherid")

        # test it in a SELECT
        self.assert_compile(select([func.count(table1.c.myid)]),
            "SELECT count(mytable.myid) AS count_1 FROM mytable")

        # test a "dotted" function name
        self.assert_compile(select([func.foo.bar.lala(table1.c.myid)]),
            "SELECT foo.bar.lala(mytable.myid) AS lala_1 FROM mytable")

        # test the bind parameter name with a "dotted" function name is only the name
        # (limits the length of the bind param name)
        self.assert_compile(select([func.foo.bar.lala(12)]),
            "SELECT foo.bar.lala(:lala_2) AS lala_1")

        # test a dotted func off the engine itself
        self.assert_compile(func.lala.hoho(7), "lala.hoho(:hoho_1)")

        # test None becomes NULL
        self.assert_compile(func.my_func(1,2,None,3), "my_func(:my_func_1, :my_func_2, NULL, :my_func_3)")

        # test pickling
        self.assert_compile(util.pickle.loads(util.pickle.dumps(func.my_func(1, 2, None, 3))), "my_func(:my_func_1, :my_func_2, NULL, :my_func_3)")

        # assert func raises AttributeError for __bases__ attribute, since its not a class
        # fixes pydoc
        try:
            func.__bases__
            assert False
        except AttributeError:
            assert True

    def test_functions_with_cols(self):
        users = table('users', column('id'), column('name'), column('fullname'))
        calculate = select([column('q'), column('z'), column('r')],
            from_obj=[func.calculate(bindparam('x'), bindparam('y'))])

        self.assert_compile(select([users], users.c.id > calculate.c.z),
            "SELECT users.id, users.name, users.fullname "
            "FROM users, (SELECT q, z, r "
            "FROM calculate(:x, :y)) "
            "WHERE users.id > z"
        )

        s = select([users], users.c.id.between(
            calculate.alias('c1').unique_params(x=17, y=45).c.z,
            calculate.alias('c2').unique_params(x=5, y=12).c.z))

        self.assert_compile(s,
            "SELECT users.id, users.name, users.fullname "
            "FROM users, (SELECT q, z, r "
            "FROM calculate(:x_1, :y_1)) AS c1, (SELECT q, z, r "
            "FROM calculate(:x_2, :y_2)) AS c2 "
            "WHERE users.id BETWEEN c1.z AND c2.z"
            , checkparams={'y_1': 45, 'x_1': 17, 'y_2': 12, 'x_2': 5})


class ExecuteTest(TestBase):

    def test_standalone_execute(self):
        x = testing.db.func.current_date().execute().scalar()
        y = testing.db.func.current_date().select().execute().scalar()
        z = testing.db.func.current_date().scalar()
        assert (x == y == z) is True

        # ansi func
        x = testing.db.func.current_date()
        assert isinstance(x.type, Date)
        assert isinstance(x.execute().scalar(), datetime.date)

    def test_conn_execute(self):
        conn = testing.db.connect()
        try:
            x = conn.execute(func.current_date()).scalar()
            y = conn.execute(func.current_date().select()).scalar()
            z = conn.scalar(func.current_date())
        finally:
            conn.close()
        assert (x == y == z) is True

    def test_update(self):
        """
        Tests sending functions and SQL expressions to the VALUES and SET
        clauses of INSERT/UPDATE instances, and that column-level defaults
        get overridden.
        """

        meta = MetaData(testing.db)
        t = Table('t1', meta,
            Column('id', Integer, Sequence('t1idseq', optional=True), primary_key=True),
            Column('value', Integer)
        )
        t2 = Table('t2', meta,
            Column('id', Integer, Sequence('t2idseq', optional=True), primary_key=True),
            Column('value', Integer, default=7),
            Column('stuff', String(20), onupdate="thisisstuff")
        )
        meta.create_all()
        try:
            t.insert(values=dict(value=func.length("one"))).execute()
            assert t.select().execute().fetchone()['value'] == 3
            t.update(values=dict(value=func.length("asfda"))).execute()
            assert t.select().execute().fetchone()['value'] == 5

            r = t.insert(values=dict(value=func.length("sfsaafsda"))).execute()
            id = r.last_inserted_ids()[0]
            assert t.select(t.c.id==id).execute().fetchone()['value'] == 9
            t.update(values={t.c.value:func.length("asdf")}).execute()
            assert t.select().execute().fetchone()['value'] == 4
            print "--------------------------"
            t2.insert().execute()
            t2.insert(values=dict(value=func.length("one"))).execute()
            t2.insert(values=dict(value=func.length("asfda") + -19)).execute(stuff="hi")

            res = exec_sorted(select([t2.c.value, t2.c.stuff]))
            self.assertEquals(res, [(-14, 'hi'), (3, None), (7, None)])

            t2.update(values=dict(value=func.length("asdsafasd"))).execute(stuff="some stuff")
            assert select([t2.c.value, t2.c.stuff]).execute().fetchall() == [(9,"some stuff"), (9,"some stuff"), (9,"some stuff")]

            t2.delete().execute()

            t2.insert(values=dict(value=func.length("one") + 8)).execute()
            assert t2.select().execute().fetchone()['value'] == 11

            t2.update(values=dict(value=func.length("asfda"))).execute()
            assert select([t2.c.value, t2.c.stuff]).execute().fetchone() == (5, "thisisstuff")

            t2.update(values={t2.c.value:func.length("asfdaasdf"), t2.c.stuff:"foo"}).execute()
            print "HI", select([t2.c.value, t2.c.stuff]).execute().fetchone()
            assert select([t2.c.value, t2.c.stuff]).execute().fetchone() == (9, "foo")
        finally:
            meta.drop_all()

    @testing.fails_on_everything_except('postgres')
    def test_as_from(self):
        # TODO: shouldnt this work on oracle too ?
        x = testing.db.func.current_date().execute().scalar()
        y = testing.db.func.current_date().select().execute().scalar()
        z = testing.db.func.current_date().scalar()
        w = select(['*'], from_obj=[testing.db.func.current_date()]).scalar()

        # construct a column-based FROM object out of a function, like in [ticket:172]
        s = select([sql.column('date', type_=DateTime)], from_obj=[testing.db.func.current_date()])
        q = s.execute().fetchone()[s.c.date]
        r = s.alias('datequery').select().scalar()

        assert x == y == z == w == q == r

    def test_extract_bind(self):
        """Basic common denominator execution tests for extract()"""

        date = datetime.date(2010, 5, 1)

        def execute(field):
            return testing.db.execute(select([extract(field, date)])).scalar()

        assert execute('year') == 2010
        assert execute('month') == 5
        assert execute('day') == 1

        date = datetime.datetime(2010, 5, 1, 12, 11, 10)

        assert execute('year') == 2010
        assert execute('month') == 5
        assert execute('day') == 1

    def test_extract_expression(self):
        meta = MetaData(testing.db)
        table = Table('test', meta,
                      Column('dt', DateTime),
                      Column('d', Date))
        meta.create_all()
        try:
            table.insert().execute(
                {'dt': datetime.datetime(2010, 5, 1, 12, 11, 10),
                 'd': datetime.date(2010, 5, 1) })
            rs = select([extract('year', table.c.dt),
                         extract('month', table.c.d)]).execute()
            row = rs.fetchone()
            assert row[0] == 2010
            assert row[1] == 5
            rs.close()
        finally:
            meta.drop_all()


def exec_sorted(statement, *args, **kw):
    """Executes a statement and returns a sorted list plain tuple rows."""

    return sorted([tuple(row)
                   for row in statement.execute(*args, **kw).fetchall()])

if __name__ == '__main__':
    testenv.main()
