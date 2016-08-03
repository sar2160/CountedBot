# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 21:04:08 2016

This creates an initial list of ids to track people already present in the
Counted Database.

@author: sar2160
"""

from functions import *

all_ids = load_ids()

run_counted(all_ids, debug=True)
