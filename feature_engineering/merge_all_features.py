#!/usr/bin/python3
# -*-coding:utf-8
import time
import numpy as np
import pandas as pd

def log_transformation(df):
    """
    Perform Log Transformation on features, which max value is > 100 (NOT LOGICAL!)
    """
    for col in df.columns:
        if 'label' in col:
            pass
        elif df[col].dtypes == np.int64 and df[col].max() > 100:
            print('Perform Transformation on column: ', col)
            df['log_{}'.format(col)] = np.log(df[col] + 1) # smoothing
            df.drop(col, axis = 1, inplace = True)
        elif df[col].dtypes == np.float64 and df[col].max() > 100:
            print('Perform Log Transformation on column: ', col)
            df['log_{}'.format(col)] = np.log(df[col] + 1) # smoothing
            df.drop(col, axis = 1, inplace = True)
    return df

def merge_features(dataType, airQuality):
    """
    Merge datetime features and air quality features into a dataframe

    params: dataType: str = ['train', 'test']
    params: airQuality: str = ['PM2.5', 'PM10']
    return: dataframe
    """
    df_datetime = pd.read_csv('../feature/london/{}/{}/datetime_features.csv'.format(dataType, airQuality))
    df_airquality = pd.read_csv('../feature/london/{}/{}/air_quality_features.csv'.format(dataType, airQuality))
    df = pd.merge(df_airquality, df_datetime, on=['station_id', 'utc_time'])
 
    return df

if __name__ == "__main__":
    s = time.time()

    inputPair = [(dataType, airQuality) for dataType in ['train', 'test'] for airQuality in ['PM2.5', 'PM10']]
    for pair in inputPair:
        print('Merging {} {} dataset...'.format(pair[1], pair[0]))
        df = merge_features(pair[0], pair[1])
        df.to_csv('../feature/london/{}/{}/all_features.csv'.format(pair[0], pair[1]), index=False)

    e = time.time()
    print('Process time: {:.2f} secs'.format(e-s))
