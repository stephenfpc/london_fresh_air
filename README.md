# London Air Quality Prediction

## Overview
This project is for participating the annual data competition, [KDD Cup 2018 of fresh air](https://biendata.com/competition/kdd_2018/).  
Here, the solution of London air quality prediction is provided. 

**Goal:**  
Given air quality and grid weather data, predict the air quality data of next 48 hours in London.

## Data
Data is all provided on official site. [[link](https://biendata.com/competition/kdd_2018/data/)]
- Air Quality
  - Stations: stations ID, latitude, longitude, site type, site name 
  - Data Type: PM2.5, PM10, NO2
  - 13 stations to be predicted, and other 11 stations for reference
- Grid Weather
  - Stations: station ID, latitude, longitude
  - Data Type: temperature, pressure, humidity, wind direction, wind speed, weather description
  - 861 grids in total
- Historical vs Live
  - Historical data can be directly downloaded on official website, which includes dates on 2017/01/01-2018/03/30.
  - Live data can retrieved by official API. [[Tutorial](https://biendata.com/forum/view_post_category/9)]

## Data Preprocessing
**The pipeline is in the data_processing folder**
1. Data Retrieval: Retrieve live data by API [*retrieve_data.py*]
2. Data Integration: Merge air quality and grid weather data with station data [*data_integration.py*]
3. Create Labels: Set the air quality at the next hour as label [*create_label.py*]
