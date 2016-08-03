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

# Police_Scan, set environment variables before running
if not DEBUG:
    CONSUMER_KEY    = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_KEY      = os.environ['ACCESS_KEY']
    ACCESS_SECRET   = os.environ['ACCESS_SECRET']

    #
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)




run_counted(all_ids, debug=DEBUG)
