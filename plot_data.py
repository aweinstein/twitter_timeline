import sqlite3
import datetime
import time

import matplotlib.pyplot as plt
import numpy as np
import pytz

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

    #print 'Selecting rows between %s and %s' % (s, e)
    
    c.execute('select * from timeline where created_at between '
              'datetime(?) and datetime(?)', (s, e))
    k = 0
    #mnt_tz = pytz.timezone('US/Mountain')
    #for r in  c.fetchall():
    #    print r[3], mnt_tz.localize(r[3])
    #    k += 1
    #print '%d rows in the time interval' % k

    records = c.fetchall()
    conn.close()
    return records
    

if __name__ == '__main__':
    db_name = 'tweets.sqlite'
    start = datetime.datetime(2011, 8, 20)
    #e = datetime.datetime(2011, 9, 10)
    dt = datetime.timedelta(minutes=60)
    n_tweets = []
    dts = []
    n_periods = 500
    for i in range(0, n_periods):
        s = start + i*dt
        e = start + (i + 1)*dt
        rs = get_time_interval(db_name, s, e)
        dts.append(s)
        #print 'Got %d records' % len(rs)
        n_tweets.append(len(rs))

    est=pytz.timezone('US/Mountain')
    #plt.plot(n_tweets,':.')
    plt.xticks(rotation=25)
    plt.plot_date(dts, n_tweets, tz=est, linestyle='dashed')

    plt.show()
    #dt = [r[3] for r in rs]
    #print n_tweets
    
if __name__ == '__main__x':
    est=pytz.timezone('US/Mountain')
    n=20
    duration=1000
    now=time.mktime(time.localtime())
    timestamps=np.linspace(now,now+duration,n)
    # You could build timezone-aware datetime objects this way:
    dates=[datetime.datetime.fromtimestamp(ts,est) for ts in timestamps]
    # or use timezone-naive datetime objects using `utcfromtimestamp` below.
    # plt.plot_date interprets naive datetime objects to be in the UTC timezone.
    # dates=[datetime.datetime.utcfromtimestamp(ts) for ts in timestamps]    
    values=np.cumsum(np.random.random(n) - 0.5)
    plt.xticks(rotation=25)
    plt.plot_date(dates,values,tz=est,linestyle='dashed')
    plt.show()

