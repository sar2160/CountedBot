# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 21:04:08 2016

This creates an initial list of ids to track people already present in the
Counted Database. 

@author: sar2160
"""



#
#import json


from functions import * 


url = 'http://thecountedapi.com/api/counted'

### getting all ids for tracking
return_all = requests.get(url).json()

all_ids = list()
for a in return_all:
    id_str = encode_id(a)
    all_ids.append(id_str) # create index with name, age, state, presumably unique

### saving existing to file 


save_ids(all_ids)