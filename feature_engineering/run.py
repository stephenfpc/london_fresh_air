#!/usr/bin/python3
# -*-coding:utf-8
"""
For feature engineering, It take approximately __ mins.

Please put the below instruction in the terminal:
    - python3 run.py Y-M-D1 Y-M-D2
    i.e. python3 run.py 2018-05-08 2018-05-09
@author: Ray
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