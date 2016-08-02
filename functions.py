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

### Connect to db, this to be subbed for Postgres
connection = sqlite3.connect('counted')


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

# load ids already stored
def load_ids(encode=True):
    c =  connection.cursor()
    c.execute('SELECT * FROM counted_id')
    my_list = c.fetchall()
    c.close()
    if encode: # to unicode from tuple
        my_list = [l[0] for l in my_list]
    return my_list

# save new ids to keep track of names already tweeted
def save_ids(id_list):
    c = connection.cursor()
    dump_list = [(i, ) for i in id_list ]
    c.executemany('INSERT INTO counted_id VALUES (?)',dump_list)
    c.close()
    connection.commit()
