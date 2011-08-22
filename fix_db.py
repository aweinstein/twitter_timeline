# Fix the DB used to store the tweets. The original DB didn't have a primary
# key, so it has duplicate entries. Also convert from string representation of
# datetime to datetime object representation.

import sqlite3
import datetime

def remove_duplicates(in_db, out_db):
    conn_in = sqlite3.connect(in_db)
    conn_out = sqlite3.connect(out_db)
    c_in = conn_in.cursor()
    c_out = conn_out.cursor()

    c_in.execute('select * from timeline')
    n_dup = 0
    for r in c_in:
        try:
            c_out.execute('insert into timeline values (?,?,?,?,?)', r)
        except sqlite3.IntegrityError:
            n_dup += 1
    
    conn_out.commit()
    c_out.close()
    c_in.close()

    print '%d duplicates eliminated' % n_dup

def convert_to_datetime(in_db, out_db):
    conn_in = sqlite3.connect(in_db)
    dt = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    conn_out = sqlite3.connect(out_db, detect_types=dt)
    c_in = conn_in.cursor()
    c_out = conn_out.cursor()
    
    c_in.execute('select * from timeline')
    n = 0
    for r in c_in:
        r = list(r)
        r[3] = eval(r[3])
        try:
            c_out.execute('insert into timeline values (?,?,?,?,?)', r)
            n += 1
        except sqlite3.IntegrityError:
            pass

    conn_out.commit()
    c_out.close()
    c_in.close()
            
        
    
if __name__ == '__main__':
    #in_db = 'test1.sqlite'
    #out_db = 'test2.sqlite'
    #remove_duplicates(in_db, out_db)

    in_db = 'test2.sqlite'
    out_db = 'test3.sqlite'
    convert_to_datetime(in_db, out_db)
