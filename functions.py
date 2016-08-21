# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 12:46:55 2016

Functions and needed modules

@author: sar2160
"""

from unicodedata import normalize
from time import sleep
import tweepy
import requests
from json import dump, load
from random import randint
import sqlite3
import os
import psycopg2
import urlparse
from local_settings import db

### Connect to db, this to be subbed for Postgres

def connect_postgres():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
        sslmode='require')
    return conn

if db == 'postgres':
    connection = connect_postgres()
else:
    connection = sqlite3.connect('counted')


def connect_tweepy():
    CONSUMER_KEY    = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_KEY      = os.environ['ACCESS_KEY']
    ACCESS_SECRET   = os.environ['ACCESS_SECRET']


    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    return api



## create a (hopefully) unique id from name+age+state, normalize the unicode to avoid headaches
def encode_id(the_json, normalized = True):
    name   = u' '.join( ( the_json['name'], the_json['age'],the_json['state'] ) ).strip()
    name.encode('utf8')
    if normalized:
        return normalize( 'NFC',name)
    else:
        return name


## tweet with a semi-random wait between tweets
def tweet_and_sleep(api,tweet_text,max_wait=5):

    try :
        api.update_status(tweet_text)
        print 'tweeted: ' + tweet_text
    except Exception,e:
        print str(e)
    sleep(randint(0,max_wait))

def run_counted(all_ids, max_wait,debug=True ):
    if not debug:
        api = connect_tweepy()

    url = 'http://thecountedapi.com/api/counted'
    r = requests.get(url)
    counted_json = r.json()

    new_cases = 0
    new_ids = list()
    for j in counted_json:
        if encode_id(j, normalized=True) not in all_ids:

            if j['name'].lower() == 'unknown':
                tweet_string = None # don't tweet unknown names
                #tweet_string =  'An unknown '  + j['sex'] + ' , age ' + j['age'].lower() + ', was killed by ' + \
                #    j['dept'] + ' in ' + j['city'] + ', ' + j['state'] + '.'
            elif j['race'].lower() == 'unknown':
                 tweet_string =  j['name'] + ', a ' + j['sex'] +  ', race unknown' ' , age ' + j['age'].lower() + ', was killed by ' + \
                    j['dept'] + ' in ' + j['city'] + ', ' + j['state'] + '.'
            else:
                tweet_string =  j['name'] + ', a ' + j['race'] + ' ' + j['sex'] + ', age ' + j['age'].lower() + ', was killed by ' + \
                    j['dept'] + ' in ' + j['city'] + ', ' + j['state'] + '.'

            print tweet_string if debug else tweet_and_sleep(api,tweet_string,max_wait)

            new_ids.append(encode_id(j, normalized=True))
            new_cases += 1

    if new_cases > 0 :
        print str(new_cases) + ' new cases'
    else:
        print 'no new cases'


    save_ids(new_ids)

# load ids already stored
def load_ids(encode=True):
    c =  connection.cursor()

    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, c) #  return query as unicode

    c.execute('SELECT * FROM public.counted_id')
    my_list = c.fetchall()
    c.close()
    if encode: # to unicode from tuple
        my_list = [l[0] for l in my_list]
    return my_list

# save new ids to keep track of names already tweeted
def save_ids(id_list):
    c = connection.cursor()
    dump_list = [(i, ) for i in id_list ]
    c.executemany("INSERT INTO public.counted_id (id) VALUES (%s)",dump_list)
    c.close()
    connection.commit()
