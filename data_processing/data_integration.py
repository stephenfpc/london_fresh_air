#!/usr/bin/python3
# -*-coding:utf-8

"""
Historical air quality data Integration:
1. Merge data with station latitude and longitude information.

Live air quality and grid weather data integration:
1. Concatenate the live day-by-day data into one file.
2. Merge air data with station latitude and longitude information.

Output:
historical air quality data as ../input/london/london_aq_hist_data_merged.csv.gz
live air quality data as ../input/london/london_aq_live_data_merged.csv.gz
live grid weather data as ../input/london/london_grid_live_data_merged.csv.gz

@author: Stephen
"""

import pandas as pd
import numpy as np
import os
import time
from glob import glob

def read_multiple_csv(path, col = None, parse_dates = None):

    # glob(path+'/*'): return a list, which consist of each files in path
    # tqdm is a package which shows the progressive bar on Pythton CLI
    if parse_dates == None:
        if col is None:
            df = pd.concat([pd.read_csv(f) for f in sorted(glob(path+'/*'))])
        else:
            df = pd.concat([pd.read_csv(f)[col] for f in sorted(glob(path+'/*'))])
    else:
        if col is None:
            df = pd.concat([pd.read_csv(f, parse_dates = ['date'] ) for f in sorted(glob(path+'/*'))])
        else:
            df = pd.concat([pd.read_csv(f, parse_dates = ['date'] )[col] for f in sorted(glob(path+'/*'))])
    return df


if __name__ == '__main__':

    stations = ['BL0', 'CD9', 'CD1', 'GN0', 'GR4', 'GN3', 'GR9', 'HV1', 'KF1', 'LW2', 'ST5', 'TH4', 'MY7']

    # Initialize a directory
    path = '../input/london'
    if not os.path.isdir(path):
        os.makedirs(path)

        
    start = time.time()
    ###############################
    # Historical Air Quality Data #
    ###############################
    if not os.path.isfile('../input/ld/london_aq_hist_data_merged.csv.gz'):

        # Read official historical data from file
        hist_data = pd.read_csv('../raw_data/London_historical_aqi_forecast_stations_20180331.csv', index_col=0)
        hist_data.columns = ['utc_time', 'station_id', 'PM2.5', 'PM10', 'NO2']
        hist_data = hist_data.fillna(0).drop_duplicates()

        # Merge latitude and longitude data
        aq_stations = pd.read_csv('../raw_data/London_AirQuality_Stations.csv', index_col=0)
        hist_data = hist_data.join(aq_stations[['Latitude', 'Longitude']], on='station_id')
        hist_data = hist_data.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'})
        hist_data = hist_data.reindex(columns=['station_id', 'utc_time', 'longitude', 'latitude', 'PM2.5', 'PM10', 'NO2'])

        # Save the file
        hist_data.to_csv('../input/london/london_aq_hist_data_merged.csv.gz', index=False, compression='gzip')

    #########################
    # Live Air Quality Data #
    #########################
    # Read live data
    live_aq_data = read_multiple_csv('../raw_data/london/airquality')
    live_aq_data = live_aq_data.drop(['id', 'CO_Concentration', 'O3_Concentration', 'SO2_Concentration'], axis=1)
    live_aq_data.columns = ['station_id', 'utc_time', 'PM2.5', 'PM10', 'NO2']
    live_aq_data = live_aq_data.reindex(columns=['utc_time', 'station_id', 'PM2.5', 'PM10', 'NO2'])
    live_aq_data = live_aq_data.fillna(0).drop_duplicates()

    # Merge latitude and longitude data
    aq_stations = pd.read_csv('../raw_data/London_AirQuality_Stations.csv', index_col=0)
    live_aq_data = live_aq_data.join(aq_stations[['Latitude', 'Longitude']], on='station_id')
    live_aq_data = live_aq_data.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'})
    live_aq_data = live_aq_data.reindex(columns=['station_id', 'utc_time', 'longitude', 'latitude' , 'PM2.5', 'PM10', 'NO2'])

    # Filter out the data which stations aren't required for predictions
    live_aq_data = live_aq_data.loc[live_aq_data['station_id'].isin(stations)]
    live_aq_data.sort_values(['station_id', 'utc_time'], inplace=True)

    live_aq_data.to_csv('../input/london/london_aq_live_data_merged.csv.gz', index=False, compression='gzip')
    del live_aq_data
    print('London Air Quality Data: Done.')

    ##########################
    # Live Grid Weather Data #
    ##########################
    # Read grid weather data
    live_grid_data = read_multiple_csv('../raw_data/london/grid')
    live_grid_data = live_grid_data.drop(['id', 'weather'], axis=1)
    live_grid_data.columns = ['station_id', 'utc_time', 'temperature', 'pressure', 'humidity', 'wind_direction', 'wind_speed']
    live_grid_data = live_grid_data.fillna(0).drop_duplicates()

    # Add longitude data and latitude data to live meo data
    grid_stations_data = pd.read_csv('../raw_data/London_grid_weather_station.csv', index_col=0)
    live_grid_data = live_grid_data.join(grid_stations_data, on='station_id')
    live_grid_data = live_grid_data.reindex(columns=['station_id', 'utc_time', 'longitude', 'latitude', 'temperature', 'pressure', 'humidity', 'wind_direction', 'wind_speed'])

    live_grid_data.to_csv('../input/london/london_grid_live_data_merged.csv.gz', index=False, compression='gzip')
    del live_grid_data
    print('London Grid Weather Data: Done.')
    
    end = time.time()
    print('Data Integration Time: {:.2f} secs'.format(end-start))
