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






## create a (hopefully) unique id from name+age+state, normalize the unicode to avoid headaches
def encode_id(the_json):
    name   = u' '.join( ( the_json['name'], the_json['age'],the_json['state'] ) ).strip()
    
    return normalize( 'NFC',name)
    
## tweet with a semi-random wait between tweets
def tweet_and_sleep(api,tweet_text,max_wait=5):
    
    try :
        api.update_status(tweet_text)
        print 'tweeted: ' + tweet_text
    except Exception,e:
        print str(e)
    sleep(randint(0,max_wait))

# load ids already stored
def load_ids(filename='existing_ids.txt'):
    with open(filename, 'r') as f:
        my_list = load(f)
    return my_list
# save new ids to keep track of names already tweeted
def save_ids(id_list, filename='existing_ids.txt'):
    with open(filename, 'w') as f:
        dump(id_list, f)

