# -*- coding: utf-8 -*-
"""

"""

import requests
import tweepy
from json import dump, load
from local_settings import *


    
def load_ids(filename='existing_ids.json'):
    with open(filename, 'r') as f:
        my_list = load(f)
    return my_list

def save_ids(id_list, filename='existing_ids.json'):
    with open(filename, 'w') as f:
        dump(id_list, f)




all_ids = load_ids()


# Just testing functionality with some test data
if TEST_DATA:
    del all_ids[-1]
    del all_ids[-2]




auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


url = 'http://thecountedapi.com/api/counted'
r = requests.get(url)
json = r.json()


new_cases = 0

for j in json:
    if j['_id'] not in all_ids:

        if j['name'] == 'Unknown':
            tweet_string =  'An unknown ' + j['sex'] + ' , age ' + j['age'].lower() + ', was killed by ' +\
                j['dept'] + ' in ' + j['city'] + ', ' + j['state'] + '.'
        else:
            tweet_string =  j['name'] + ', ' + j['sex'] + ' , age ' + j['age'].lower() + ', was killed by ' + \
                j['dept'] + ' in ' + j['city'] + ', ' + j['state'] + '.'
                
        print tweet_string if DEBUG else api.update_status(tweet_string)
        new_cases += 1
        all_ids.append(j['_id'])


if new_cases > 0 :
    print str(new_cases) + ' new cases'
else:
    print 'no new cases'


save_ids(all_ids)       
        

