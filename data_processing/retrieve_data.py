#!/usr/bin/python3
# -*-coding:utf-8
"""
Retrive live air quality and meteorology data, from 2018/03/31 to current time, by official API.

@author: Ray & Stephen

Reference: https://biendata.com/forum/view_post/9
"""

import requests
import os
import time
import datetime

def retrieve_data(dataType, city):
    """
    Retrieve live data and save it in folders
    
    params: dataType: string, options: ['meteorology', 'airquality', 'grid']
    params: city: string, options: ['beijing', 'london']
    return: None
    """
    cityAbbr = 'bj' if city == 'beijing' else 'ld'
    
    # Create directories for each city
    path = '../raw_data/{}'.format(city)
    if not os.path.isdir(path):
        os.makedirs(path)

    # Create directories for each kind of data
    path = '../raw_data/{0}/{1}'.format(city, dataType)
    if not os.path.isdir(path):
        os.makedirs(path)

    # Initialize date variables
    utcTime = datetime.datetime.utcnow()
    utcToday = datetime.date(year=utcTime.year, month=utcTime.month, day=utcTime.day)

    # Retrieve data day by day, from 2018/03/31 until now
    currentDate = datetime.date(year=2018, month=3, day=31)
    while currentDate <= utcToday:
        filename = '{0}_{1}_{2:%Y}{2:%m}{2:%d}.csv'.format(cityAbbr, dataType, currentDate)
        path = '../raw_data/{0}/{1}/{2}'.format(city, dataType, filename)
        if not os.path.isfile(path) or currentDate == utcToday:
            if dataType == 'grid':
                input = '{}_{}'.format(cityAbbr, dataType)
                url = 'https://biendata.com/competition/meteorology/{0}/{1}-0/{1}-23/2k0d1d8'.format(input, currentDate)
            else:
                url = 'https://biendata.com/competition/{0}/{1}/{2}-0/{2}-23/2k0d1d8'.format(dataType, cityAbbr, currentDate)

            response = requests.get(url)
            if response.text == 'None':
                print("No data in {}".format(filename))
                pass
            else:
                with open(path, 'w') as f:
                    f.write(response.text)
                print("{}: Retrieved".format(path))

        # Set currentDate to the next day
        currentDate += datetime.timedelta(days=1)
        
    #=============================================
    # Alternative method: Retrive data in one file
    #=============================================
    
    filename = '{0}_{1}_20180331_{2:%Y}{2:%m}{2:%d}.csv'.format(cityAbbr, dataType, currentDate)
    path = '../raw_data/{0}/{1}'.format(city, filename)
    url = 'https://biendata.com/competition/{0}/{1}/2018-03-31-0/{2}-{3}/2k0d1d8'.format(dataType, cityAbbr, utcToday, utcTime.hour)

    response = requests.get(url)
    if response.text == 'None':
        print("No data in {}".format(filename))
        pass
    else:
        with open(path, 'w') as f:
            f.write(response.text)
        print("{}: Retrieved".format(path))


if __name__ == '__main__':

    start = time.time()
    ############################
    # Retrieve Data in Beijing #
    ############################
    retrieve_data('meteorology', 'beijing')
    print('Meteorology in Beijing: Done')

    retrieve_data('airquality', 'beijing')
    print('Air Quality in Beijing: Done')

    retrieve_data('grid', 'beijing')
    print('Grid Meteorology in Beijing: Done')

    ###########################
    # Retrieve Data in London #
    ###########################
    retrieve_data('airquality', 'london')
    print('Air Quality in London: Done')

    retrieve_data('grid', 'london')
    print('Grid Meteorology in London: Done')
    
    end = time.time()
    print('Data Retrieval Time: {:.2f} secs'.format(end-start))