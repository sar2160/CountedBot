# -*- coding: utf-8 -*-
"""
This script runs on a designated interval, checking for new records added
to the Counted DataBase and tweeting them. New records are given a unique id and 
added to 'existing_ids.txt' for tracking (in lieu of a real database)
"""

from local_settings import *
from functions import *


all_ids = load_ids()


# Just testing functionality with some test data
if TEST_DATA:
    del all_ids[1]



url = 'http://thecountedapi.com/api/counted'
r = requests.get(url)
counted_json = r.json()


new_cases = 0

for j in counted_json:
    if encode_id(j) not in all_ids:

        if j['name'] == 'Unknown':
            tweet_string =  'An unknown ' + j['race']+ ' ' + j['sex'] + ' , age ' + j['age'].lower() + ', was killed by ' +\
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
        

