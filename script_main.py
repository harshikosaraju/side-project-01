import json
#import pandas
#import numpy
import os

# Open and read the JSON file
with open('output_response.json', 'r') as file:
    response = json.load(file)

location_lists = response['data'] # list of dictionaries of locations

location_ids = []
for location_dict in location_lists:
    location_ids.append(location_dict['locationId'])

print(len(location_ids))