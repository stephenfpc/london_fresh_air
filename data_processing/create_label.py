# -*-coding: utf-8
"""
Set the label of air quality data.
In our case, the air quality data of next hour is set as label.

For example:
PM2.5 at 13:00 is the label of the input data at 12:00

@author: Stephen

Note:
The rows are dropped if their labels are NaN.
Alternative way is to drop the rows with invalid labels when training the models
Do model training methods neglect invalid row by default?
"""

import pandas as pd
import numpy as np
import os
import time

def create_label(df, target, offset=1):
    """
    Create label, which is the next hour's value of target given a timestamp.

    params: df: DataFrame
    params: target: string, options: ['PM2.5', 'PM10']
    params: offset: int (>0), the hour interval from input time to label time
    return: df: DataFrame, the input dataframe with target labels
    """
    # pre-processing for subsequent procedure
    df.sort_values(by ='utc_time', inplace = True)
    df['utc_time_delta'] = df.utc_time.shift(-1) - df.utc_time
    df['utc_time_delta'] = df.utc_time_delta.map(lambda timedelta: timedelta.seconds // 3600)  # convert time_delta into hours
    # df['utc_time_delta'] = df.utc_time_delta.map(lambda timedelta: timedelta.hour)

    labelName = '{}_label'.format(target)
    df[labelName] = [df[target].tolist()[i + offset] if delta == 1 else np.nan for i, delta in enumerate(df.utc_time_delta.tolist())]
    # df = df.dropna(subset=[labelName]).drop(['utc_time_delta'], axis=1)
    return df


if __name__ == "__main__":

    start = time.time()

    ###################
    # Historical Data #
    ###################
    # Note: This pipeline will be skipped if the historical data already exists.

    london_aq_hist_data = pd.read_csv('../input/london/london_aq_hist_data_merged.csv.gz', compression='gzip')
    london_aq_hist_data['utc_time'] = pd.to_datetime(london_aq_hist_data['utc_time'])

    PM25_hist_filepath = '../input/london/london_PM25_hist_data_w_label.csv'
    if not os.path.isfile(PM25_hist_filepath):
        london_PM25_data = london_aq_hist_data.groupby('station_id').apply(create_label, target='PM2.5').dropna(subset=['PM2.5_label']).drop(['utc_time_delta'], axis=1)
        london_PM25_data.to_csv(PM25_hist_filepath, index=False)
        print('London PM2.5 hist label data created and saved.')
        del london_PM25_data
    else:
        print('London PM2.5 hist label data already exists')

    PM10_hist_filepath = '../input/london/london_PM10_hist_data_w_label.csv'
    if not os.path.isfile(PM10_hist_filepath):
        london_PM10_data = london_aq_hist_data.groupby('station_id').apply(create_label, target='PM10').dropna(subset=['PM10_label']).drop(['utc_time_delta'], axis=1)
        london_PM10_data.to_csv(PM10_hist_filepath, index=False)
        print('London PM10 hist label data created and saved.')
        del london_PM10_data
    else:
        print('London PM10 hist label data already exists')

    #############
    # Live Data #
    #############
    london_aq_live_data = pd.read_csv('../input/london/london_aq_live_data_merged.csv.gz', compression='gzip')
    london_aq_live_data['utc_time'] = pd.to_datetime(london_aq_live_data['utc_time'])

    PM25_live_filepath = '../input/london/london_PM25_live_data_w_label.csv'
    london_PM25_live_data = london_aq_live_data.groupby('station_id').apply(create_label, target='PM2.5').dropna(subset=['PM2.5_label']).drop(['utc_time_delta'], axis=1)
    london_PM25_live_data.to_csv(PM25_live_filepath, index=False)
    print('London PM2.5 live label data created and saved.')
    del london_PM25_live_data

    PM10_live_filepath = '../input/london/london_PM10_live_data_w_label.csv'
    london_PM10_live_data = london_aq_live_data.groupby('station_id').apply(create_label, target='PM10').dropna(subset=['PM10_label']).drop(['utc_time_delta'], axis=1)
    london_PM10_live_data.to_csv(PM10_live_filepath, index=False)
    print('London PM10 live label data created and saved.')
    del london_PM10_live_data

    end = time.time()
    print("Labeling Process time: {:.2f} secs".format(end-start))
