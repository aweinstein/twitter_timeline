#!/usr/bin/env python

import logging
import sqlite3
import sys

from config import *

logging.basicConfig(filename=log_file,
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)


import tweepy

def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return api

def get_timeline(api, limit=None):
    '''Return a list of tuple with the content of the timeline'''
    tl = []
    k = 0
    if limit:
        cursor = tweepy.Cursor(api.home_timeline).items(limit)
    else:
        cursor = tweepy.Cursor(api.home_timeline).items()
    logging.info('Getting the timeline')
    try:
        for t in cursor:
            try:
                tl.append((t.id,
                           t.user.screen_name,
                           repr(t.coordinates),
                           t.created_at,
                           t.text))
            except AttributeError:
                k += 1
        logging.info('%d itemes placed in the timeline', len(tl))
    except tweepy.error.TweepError as exception:
        logging.error('Twitter exception: %s', exception)
        sys.exit(0)
    if k > 0:
        logging.info('%d entries with missing attributes.', k)
        
    return tl

# Move this to something like utils.py or db.py
def get_db_connection(file_name):
    dt = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    conn = sqlite3.connect(file_name, detect_types=dt)
    logging.info('Connected to database %s', file_name)
    return conn

def create_db(file_name):
    conn = get_db_connection(file_name)
    c = conn.cursor()
    
    c.execute("SELECT name FROM sqlite_master WHERE "
              "type='table' AND name='timeline'")
    if c.fetchone():
        c.execute('drop table timeline')
        print 'Table timeline dropped.'
    c.execute('create table timeline'
              '(id integer primary key, screen_name text, coordinates text,'
              'created_at timestamp, content text)')
    print 'Table timeline created.'
    conn.commit()
    c.close()
    print 'Create database %s.' % file_name
    
def insert_timeline(tl, file_name):
    conn = get_db_connection(file_name)
    c = conn.cursor()

    k = 0
    for t in tl:
        try:
            c.execute('insert into timeline values (?,?,?,?,?)', t)
            k += 1
        except sqlite3.IntegrityError:
            pass
        
    conn.commit()
    c.close()

    logging.info('%d register inserted into %s.', k, file_name)
    
if __name__ == '__main__':

    #db_name = './tweets.sqlite'
    #create_db(db_name)
    api = auth()
    timeline = get_timeline(api)
    insert_timeline(timeline, db_name)

    logging.info('Finish updating the timeline')
