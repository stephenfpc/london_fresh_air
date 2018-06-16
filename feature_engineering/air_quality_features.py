#!/usr/bin/python3
# -*-coding:utf-8
'''
Generate air quality features.
1. Try rolling windows method with different window size due to time-series characteristics.
2. Try different statistic method.

Conclusion:
    PM2.5: window_size = 1-3 days, stats = mean, std, median, max, min
    PM10: window_size = 1-3 days, stat = mean, std, median, max, min

@author: Stephen, Ray
'''

import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
import itertools
import utils
import sys

# =====================
# Read Air Quality data
# =====================
# PM2.5 air quality data
PM25_hist_data = pd.read_csv('../input/london/london_PM25_hist_data_w_label.csv')
PM25_live_data = pd.read_csv('../input/london/london_PM25_live_data_w_label.csv')
PM25_data = pd.concat([PM25_hist_data, PM25_live_data])
PM25_data = PM25_data.drop(['latitude', 'longitude', 'PM10', 'NO2'], axis=1)
del PM25_hist_data, PM25_live_data

# PM10 air quality data
PM10_hist_data = pd.read_csv('../input/london/london_PM10_hist_data_w_label.csv')
PM10_live_data = pd.read_csv('../input/london/london_PM10_live_data_w_label.csv')
PM10_data = pd.concat([PM10_hist_data, PM10_live_data])
PM10_data = PM10_data.drop(['latitude', 'longitude', 'PM2.5', 'NO2'], axis=1)
del PM10_hist_data, PM10_live_data

# convert utc_time to datetime type
PM25_data['utc_time'] = pd.to_datetime(PM25_data.utc_time)
PM10_data['utc_time'] = pd.to_datetime(PM10_data.utc_time)

# check time period
print('PM25 training data starts from {} to {}'.format(PM25_data['utc_time'].min(), PM25_data['utc_time'].max()))
print('PM10 training data starts from {} to {}'.format(PM10_data['utc_time'].min(), PM10_data['utc_time'].max()))

# ======================================================
# Append empty rows for testing data (The next two days)
# ======================================================
if len(sys.argv) > 1:
    submission_day1 = sys.argv[1]
    submission_day2 = sys.argv[2]
else:
    today = datetime.date(PM25_data['utc_time'].max())
    submission_day1 = today + timedelta(days=1)
    submission_day2 = today + timedelta(days=2)

testStartTime = datetime(year=submission_day1.year, month=submission_day1.month, day=submission_day1.day)
testTime = [testStartTime+timedelta(hours=delta) for delta in range(48)]
stationId = PM25_data.station_id.unique()
testPair = [(sid, time) for sid in stationId for time in testTime]
df = pd.DataFrame(testPair, columns=['station_id', 'utc_time'])

PM25_data = pd.concat([PM25_data, df], axis=0)[['station_id', 'utc_time', 'PM2.5', 'PM2.5_label']]
PM10_data = pd.concat([PM10_data, df], axis=0)[['station_id', 'utc_time', 'PM10', 'PM10_label']]

# ========================================
# Generate Air Quality statistics features
# ========================================
# Given a station and utc_time, generate air quality stats with rolling windows.
# There are 15 features generated in total, combinations from window size: 1-3 days and stats: mean, std, median, max, min.

d = {'PM2.5': PM25_data, 'PM10': PM10_data}
for air_quality in ['PM2.5', 'PM10']:
    print('Generate {} Features...'.format(air_quality))
    stats = list()
    df = d[air_quality]
    df_group = df.groupby('station_id')
    df_group_w_null = df.where(df>0, np.nan).groupby('station_id')
    for win in ['1d', '2d', '3d']:
        df_mean = df_group_w_null.apply(lambda row: row.set_index('utc_time')[air_quality].rolling(window=win).mean())
        df_std = df_group_w_null.apply(lambda row: row.set_index('utc_time')[air_quality].rolling(window=win).std())
        df_median = df_group_w_null.apply(lambda row: row.set_index('utc_time')[air_quality].rolling(window=win).median())
        
        # Note: max() and min() return NaN when the first value in the rolling window is NaN.
        # For max(), keep values(<=0) instead of replacing them with NaN.
        # For min(), replacing NaN with infinity still cause problems. 
        df_max = df_group.apply(lambda row: row.set_index('utc_time')[air_quality].rolling(window=win).max())
        df_min = df_group_w_null.apply(lambda row: row.set_index('utc_time')[air_quality].rolling(window=win).min())
        
        df_stat = pd.concat([df_mean, df_std, df_median, df_max, df_min], axis=1).reset_index()
        prefix = '{}_{}'.format(air_quality, win)
        df_stat.columns = ['station_id', 'utc_time', prefix+'_mean', prefix+'_std', prefix+'_median', prefix+'_max', prefix+'_min']
        stats.append(df_stat)

    for i in range(3):
        df = pd.merge(df, stats[i], on=['station_id','utc_time'], how='left')
    df = df.sort_values(['station_id', 'utc_time'], axis=0)
    df_train = df[df['utc_time'] < testStartTime]
    df_test = df[df['utc_time'] >= testStartTime]
    df_train.to_csv('../feature/london/train/{}/air_quality_features.csv'.format(air_quality), index = False)
    df_test.to_csv('../feature/london/test/{}/air_quality_features.csv'.format(air_quality), index = False)