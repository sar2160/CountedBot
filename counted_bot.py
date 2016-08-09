# -*- coding: utf-8 -*-
"""
This script runs on a designated interval, checking for new records added
to the Counted DataBase and tweeting them. New records are given a unique id and
added to 'existing_ids.txt' for tracking (in lieu of a real database)
"""

from local_settings import *
from functions import *
import os


if __name__ == "__main__":

    all_ids = load_ids()


    # Just testing functionality with some test data
    if TEST_DATA:
        del all_ids[1]

    if not DEBUG:
        api = connect_tweepy()

run_counted(all_ids, max_wait, debug=DEBUG)
