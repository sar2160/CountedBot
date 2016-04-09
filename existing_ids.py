# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 21:04:08 2016

@author: simonrimmele
"""




import json
import requests

url = 'http://thecountedapi.com/api/counted'

### getting all ids for tracking
return_all = requests.get(url).json()

all_ids = list()
for a in return_all:
    all_ids.append(a['_id'])

### saving existing to file 


def save_ids(id_list, filename='existing_ids.json'):
    with open(filename, 'w') as f:  # only writing 
        json.dump(id_list, f)
    
def load_ids(filename='existing_ids.json'):
    with open(filename, 'rb') as f:
        my_list = json.load(f)
    return my_list

save_ids(all_ids)