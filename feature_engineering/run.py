#!/usr/bin/python3
# -*-coding:utf-8
"""
Feature Engineering Pipeline.

Note: The prediction dates can be passed as parameters into scripts

@author: Stephen
"""
import os
import time
import sys
from datetime import date, timedelta

#######################
# Feature Engineering #
#######################
s = time.time()

# Initialize the prediction dates
today = date.today()
submission_day1 = today + timedelta(days=1)
submission_day2 = today + timedelta(days=2)

print(.)
print('Step 1: Generate Datetime Features')
os.system('python3 -u ./datetime_features.py')

print(.)
print('Step 2: Generate Air Quality Features')
os.system('python3 -u ./air_quality_features.py')

print(.)
print('Step 3: Merge all features')
os.system('python3 -u ./merge_all_features.py')

e = time.time()
print('.')
print('.')
print('.')
print('Feature Engineering Done!')
print('It take {} mins'.format((e-s)/60.0))