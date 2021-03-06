import testenv; testenv.configure_for_tests()
from sqlalchemy import *
from sqlalchemy.orm import *
from testlib import *
from testlib import fixtures
import gc

# in this test we are specifically looking for time spent in the attributes.InstanceState.__cleanup() method.

ITERATIONS = 100

class SessionTest(TestBase, AssertsExecutionResults):
    def setUpAll(self):
        global t1, t2, metadata,T1, T2
        metadata = MetaData(testing.db)
        t1 = Table('t1', metadata,
            Column('c1', Integer, primary_key=True),
            Column('c2', String(30)))

        t2 = Table('t2', metadata,
            Column('c1', Integer, primary_key=True),
            Column('c2', String(30)),
            Column('t1id', Integer, ForeignKey('t1.c1'))
            )
        
        metadata.create_all()

        l = []
        for x in range(1,51):
            l.append({'c2':'this is t1 #%d' % x})
        t1.insert().execute(*l)
        for x in range(1, 51):
            l = []
            for y in range(1, 100):
                l.append({'c2':'this is t2 #%d' % y, 't1id':x})
            t2.insert().execute(*l)
        
        class T1(fixtures.Base):
            pass
        class T2(fixtures.Base):
            pass

        mapper(T1, t1, properties={
            't2s':relation(T2, backref='t1')
        })
        mapper(T2, t2)
    
    def tearDownAll(self):
        metadata.drop_all()
        clear_mappers()
        
    @profiling.profiled('clean', report=True)
    def test_session_clean(self):
        for x in range(0, ITERATIONS):
            sess = create_session()
            t1s = sess.query(T1).filter(T1.c1.between(15, 48)).all()
            for index in [2, 7, 12, 15, 18, 20]:
                t1s[index].t2s

            sess.close()
            del sess
            gc.collect()

    @profiling.profiled('dirty', report=True)
    def test_session_dirty(self):
        for x in range(0, ITERATIONS):
            sess = create_session()
            t1s = sess.query(T1).filter(T1.c1.between(15, 48)).all()
            
            for index in [2, 7, 12, 15, 18, 20]:
                t1s[index].c2 = 'this is some modified text'
                for t2 in t1s[index].t2s:
                    t2.c2 = 'this is some modified text'

            del t1s
            gc.collect()
            
            sess.close()
            del sess
            gc.collect()

    @profiling.profiled('noclose', report=True)
    def test_session_noclose(self):
        for x in range(0, ITERATIONS):
            sess = create_session()
            t1s = sess.query(T1).filter(T1.c1.between(15, 48)).all()
            for index in [2, 7, 12, 15, 18, 20]:
                t1s[index].t2s

            del sess
            gc.collect()
        


if __name__ == '__main__':
    testenv.main()
