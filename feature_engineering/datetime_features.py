#!/usr/bin/python3
# -*-coding:utf-8
'''
Convert absolute time into relative time.

relative columns names:
month_of_year, week_of_year, week_of_month,
day_of_month, day_of_week, hour_of_day

Range of relative time columns:
    month of year: [1-12]
    week of year: [1-52]
    week of month: [1-6]
    day of month: [1-31]
    day of week: [0-6]
    hour of day: [0-23]

@author: Stephen Fang
'''
import pandas as pd
import sys
import os
from datetime import datetime, date, timedelta
from math import ceil 
import itertools


def week_of_month(date):
    """ 
    Returns the week of the month given the specified date.
    Adjust the date with an offset, the weekday of the first date of that month.

    params: date: datetime64[ns]
    return: int
    """
    offset = date.replace(day=1).weekday()
    return ceil((date.day + offset)/7)

if __name__ == "__main__":
    # ===========================================
    # Create relative time columns of London data
    # ===========================================

    # Initialize default directories
    folders = [(dataType, airQuality) for dataType in ('train', 'test') for airQuality in ('PM2.5', 'PM10')]
    for f in folders:
        path = '../feature/london/{}/{}'.format(f[0], f[1])
        if not os.path.isdir(path):
            os.makedirs(path)

    # =======================================
    # Generate London PM2.5 datetime features
    # =======================================
    PM25_hist_data = pd.read_csv('../input/london/london_PM25_hist_data_w_label.csv')
    PM25_live_data = pd.read_csv('../input/london/london_PM25_live_data_w_label.csv')
    PM25_data = pd.concat([PM25_hist_data, PM25_live_data])
    del PM25_hist_data, PM25_live_data

    PM25_data['utc_time'] = pd.to_datetime(PM25_data['utc_time'])
    PM25_data['month_of_year'] = PM25_data['utc_time'].dt.month
    PM25_data['week_of_year'] = PM25_data['utc_time'].dt.week
    PM25_data['week_of_month'] = PM25_data['utc_time'].apply(week_of_month)
    PM25_data['day_of_month'] = PM25_data['utc_time'].dt.day
    PM25_data['day_of_week'] = PM25_data['utc_time'].dt.weekday
    PM25_data['hour_of_day'] = PM25_data['utc_time'].dt.hour

    cols = ['station_id', 'utc_time', 'PM2.5_label', 'month_of_year',
            'week_of_year', 'week_of_month', 'day_of_month',
            'day_of_week', 'hour_of_day']

    PM25_datetime_featues = PM25_data[cols]
    PM25_datetime_featues = PM25_datetime_featues.sort_values(by=['station_id', 'utc_time'])
    PM25_datetime_featues.to_csv('../feature/london/train/PM2.5/datetime_features.csv', index=False)
    print('Current latest date in PM2.5 training data: {}'.format(PM25_datetime_featues['utc_time'].max()))
    print('London PM2.5 datetime features: Done!')

    # ======================================
    # Generate London PM10 datetime features
    # ======================================
    PM10_hist_data = pd.read_csv('../input/london/london_PM10_hist_data_w_label.csv')
    PM10_live_data = pd.read_csv('../input/london/london_PM10_live_data_w_label.csv')
    PM10_data = pd.concat([PM10_hist_data, PM10_live_data])
    del PM10_hist_data, PM10_live_data

    PM10_data['utc_time'] = pd.to_datetime(PM10_data['utc_time'])
    PM10_data['month_of_year'] = PM10_data['utc_time'].dt.month
    PM10_data['week_of_year'] = PM10_data['utc_time'].dt.week
    PM10_data['week_of_month'] = PM10_data['utc_time'].apply(week_of_month)
    PM10_data['day_of_month'] = PM10_data['utc_time'].dt.day
    PM10_data['day_of_week'] = PM10_data['utc_time'].dt.weekday
    PM10_data['hour_of_day'] = PM10_data['utc_time'].dt.hour

    cols = ['station_id', 'utc_time', 'PM10_label', 'month_of_year',
            'week_of_year', 'week_of_month', 'day_of_month',
            'day_of_week', 'hour_of_day']

    PM10_datetime_featues = PM10_data[cols]
    PM10_datetime_featues = PM10_datetime_featues.sort_values(by=['station_id', 'utc_time'])

    PM10_datetime_featues.to_csv('../feature/london/train/PM10/datetime_features.csv', index=False)
    print('Current latest date in PM10 training data: {}'.format(PM10_datetime_featues['utc_time'].max()))
    print('London PM10 dateime features: Done!')
    print('Training Data Process: Done!')

    # ==========================================
    # Process Testing Dataset (The next two day)
    # ==========================================

    if len(sys.argv) > 1:
        submission_day1 = sys.argv[1]
        submission_day2 = sys.argv[2]
    else:
        today = date.today()
        submission_day1 = today + timedelta(days=1)
        submission_day2 = today + timedelta(days=2)

    # Initialize station ID and utc time columns
    testStartTime = datetime(year=submission_day1.year, month=submission_day1.month, day=submission_day1.day)
    testTime = [testStartTime+timedelta(hours=delta) for delta in range(48)]
    stationId = PM25_data.station_id.unique()
    testPair = [(sid, time) for sid in stationId for time in testTime]
    test = pd.DataFrame(testPair, columns=['station_id', 'utc_time'])

    # Generate testing datetime features
    test['month_of_year'] = test['utc_time'].dt.month
    test['week_of_year'] = test['utc_time'].dt.week
    test['week_of_month'] = test['utc_time'].apply(week_of_month)
    test['day_of_month'] = test['utc_time'].dt.day
    test['day_of_week'] = test['utc_time'].dt.weekday
    test['hour_of_day'] = test['utc_time'].dt.hour

    test.to_csv('../feature/london/test/PM2.5/datetime_features.csv', index = False)
    test.to_csv('../feature/london/test/PM10/datetime_features.csv', index = False)
    print('Testing Data Process: Done!')