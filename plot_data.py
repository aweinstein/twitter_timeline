import sqlite3
import datetime

DT_FMT = '%Y-%m-%d %H:%M:%S'

def get_db_connection(file_name):
    dt = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    conn = sqlite3.connect(file_name, detect_types=dt)
    return conn

def get_time_interval(db_name, start, end):
    conn = get_db_connection(db_name)
    c = conn.cursor()
    s = start.strftime(DT_FMT)
    e = end.strftime(DT_FMT)

    print 'Selecting rows between %s and %s' % (s, e)
    
    c.execute('select * from timeline where created_at between '
              'datetime(?) and datetime(?)', (s, e))
    k = 0
    for r in  c.fetchall():
        print r[3]
        k += 1
    print '%d rows in the time interval' % k
    
    conn.close()
    
if __name__ == '__main__':
    db_name = 'tweets.sqlite'
    s = datetime.datetime(2011, 8, 21)
    e = datetime.datetime(2011, 8, 22)
    get_time_interval(db_name, s, e)
    
