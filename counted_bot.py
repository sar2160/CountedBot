# -*- coding: utf-8 -*-
"""
This script runs on a designated interval, checking for new records added
to the Counted DataBase and tweeting them. New records are given a unique id and 
added to 'existing_ids.txt' for tracking (in lieu of a real database)
"""

from local_settings import *
from functions import *
import os




all_ids = load_ids()


# Just testing functionality with some test data
if TEST_DATA:
    del all_ids[1]




url = 'http://thecountedapi.com/api/counted'
r = requests.get(url)
counted_json = r.json()

## Police_Scan

CONSUMER_KEY    = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_KEY      = os.environ['ACCESS_KEY']
ACCESS_SECRET   = os.environ['ACCESS_SECRET']


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)




new_cases = 0

for j in counted_json:
    if encode_id(j) not in all_ids:
        
        if j['name'].lower() == 'unknown':
            tweet_string =  'An unknown '  + j['sex'] + ' , age ' + j['age'].lower() + ', was killed by ' + \
                j['dept'] + ' in ' + j['city'] + ', ' + j['state'] + '.'
        elif j['race'].lower() == 'unknown':
             tweet_string =  j['name'] + ', a ' + j['sex'] +  ', race unknown' ' , age ' + j['age'].lower() + ', was killed by ' + \
                j['dept'] + ' in ' + j['city'] + ', ' + j['state'] + '.'
        else:
            tweet_string =  j['name'] + ', a ' + j['race'] + ' ' + j['sex'] + ' , age ' + j['age'].lower() + ', was killed by ' + \
                j['dept'] + ' in ' + j['city'] + ', ' + j['state'] + '.'
                
        print tweet_string if DEBUG else tweet_and_sleep(api,tweet_string,max_wait)
        new_id = encode_id(j)
        all_ids.append(new_id)
        new_cases += 1


if new_cases > 0 :
    print str(new_cases) + ' new cases'
else:
    print 'no new cases'


save_ids(all_ids)       
        

