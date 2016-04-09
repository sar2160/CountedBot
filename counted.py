# -*- coding: utf-8 -*-
"""

"""

import requests
import tweepy

url = 'http://thecountedapi.com/api/counted'



### getting all ids for tracking
return_all = requests.get(url).json()

all_ids = list()
for a in return_all:
    all_ids.append(a['_id'])





r = requests.get(url)
json = r.json()


for j in json:
    if j['_id'] not in all_ids:
        print j['_id']


for j in json:
    if j['name'] == 'Unknown':
        tweet_string =  'An unknown ' + j['sex'] + ' , Age ' + j['age'].lower() + ', was killed by ' +\
            j['dept'] + ' in ' + j['city'] + ', ' + j['state'] + '.'
    else:
        tweet_string =  j['name'] + ', ' + j['sex'] + ' , Age ' + j['age'].lower() + ', was killed by ' + \
            j['dept'] + ' in ' + j['city'] + ', ' + j['state'] + '.'
    
    print tweet_string
    
    

# Twitter details 
CONSUMER_KEY = 'dsrOQwVtaJkOAIzAAZjXk9oCN'
CONSUMER_SECRET ='oJrUvgKCbAQYBwoDJoCeoHKs0gPEK89g9QHKZ5PMt4yCldAhmL'
ACCESS_KEY = '717142719223697408-eVDSpMRGUzyareFx1HZv0K6EOKiB7vk'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'Bk7zKGjJ7y314KcgVP55HbhwQOs1ns4JKbOBn5en55XmS'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)