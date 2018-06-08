#!/usr/bin/python3
# -*-coding: utf-8
"""
Data preprocessing pipeline.

@author: Stephen
"""

import os
import time

 ####################
# data preprocessing #
 ####################
s = time.time()

print('Start Data preprocessing...')
print('.')
print('.')
print('.')
print('Step 1: Live Data Retrieval...')
os.system('python3 -u ./retrieve_data.py')

print('Step 2: Data Integration...')
os.system('python3 -u ./data_integration.py')

# The data retrieved from external API may varies due to the timezone issue.
# Temporarily exclude running this script for now.
# os.system('python3 -u ./merge_aq_external.py')

print('Step 3: Data Labeling...')
os.system('python3 -u ./create_label.py')

e = time.time()
print('.')
print('.')
print('.')
print('Data Preprocessing Finished.')
print('It takes {:.2f} mins'.format((e-s)/60.0))
