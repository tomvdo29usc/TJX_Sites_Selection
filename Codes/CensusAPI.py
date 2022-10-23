#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 00:35:04 2022

@author: tomvdo29
"""
# import packages
import census
import pandas as pd
import geopandas as gpd
import censusdata
import censusgeocode as cg
import geopy
from geopy.geocoders import Nominatim
import numpy as np
import plotly_express as px
import matplotlib.pyplot as plt
import requests
from plotnine import *
import os

# Change working directory
os.chdir("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data")

df = pd.read_csv('Clients_Data.csv')
df = df[df.State == "FL"].reset_index(drop=True)

df.drop(['Store_Address','City','State'],axis = 1,inplace = True)

df['Place_ID'] = np.nan
df['City'] = np.nan
df['County'] = np.nan
df['State'] = np.nan
df['zipcode'] = np.nan
df['GEOID'] = np.nan
df['TRACT'] = np.nan
df['StateID'] = np.nan
df['CountyID'] = np.nan
df['TractPopulation'] = np.nan
df['TractMedianIncome'] = np.nan

locator = Nominatim(user_agent="google") # you can use binge, yahoo, etc.
for i in  list(range(0,len(df))):
    coordinates = str(df.Lat[i]) + ',' + str(df.Long[i])
    location = locator.reverse(coordinates)

    # try:
    #     df.loc[i,'State'] = location.raw['address']['state']     # list((list(location.raw.items())[7][1]).items())[5][1] # state
    #     df.loc[i,'Place_ID'] = location.raw['place_id']         # list(location.raw.items())[0][1] #place_id
    #     df.loc[i,'City'] = location.raw['address']['city' if 'city' in location.raw['address'] else 'town' if 'town' in location.raw['address'] else 'hamlet'] # alabama calls cities towns or hamlets - very strange
    #     df.loc[i,'County'] = location.raw['address']['county']    # list((list(location.raw.items())[7][1]).items())[4][1] # county
    #     df.loc[i,'zipcode'] = location.raw['address']['postcode']   # list((list(location.raw.items())[7][1]).items())[7][1] # zip code
    # except:
    #     df.loc[i,'zipcode'] = np.nan
    #     df.loc[i,'Place_ID'] = np.nan
    #     df.loc[i,'City'] = np.nan
    #     df.loc[i,'County'] = np.nan
    #     df.loc[i,'zipcode'] = np.nan
        
    CensusGeoData = cg.coordinates(x=df.Long[i], y=df.Lat[i])
    df.loc[i,'GEOID'] = CensusGeoData ['Census Tracts'][0]['GEOID']
    df.loc[i,'TRACT'] = CensusGeoData ['Census Tracts'][0]['TRACT']
    df.loc[i,'StateID'] = CensusGeoData ['Census Tracts'][0]['STATE']
    df.loc[i,'CountyID'] = CensusGeoData ['Census Tracts'][0]['COUNTY']
    
    # print("StateID: "+df.loc[i,'StateID'])
    # print("tract: "+ df.loc[i,'TRACT'])
    # print("CountyID: "+df.loc[i,'CountyID'])
    # 'B01003_001E' = population 
    # 'B19113_001E' = median income
    AcsData = censusdata.download('acs5', 2020, censusdata.censusgeo([('state', df.loc[i,'StateID']),  ('county', df.loc[i,'CountyID']), ('tract', df.loc[i,'TRACT'])]), ['B01003_001E','B19113_001E']).values
    df.loc[i,'TractPopulation'] = AcsData[0,0]
    #print(df.loc[i,'TractPopulation'])
    df.loc[i,'TractMedianIncome'] = AcsData[0,1]
    coordinates = str(df.Lat[i]) + ',' + str(df.Long[i])
    location = locator.reverse(coordinates)
    print(i)

    try:
        df.loc[i,'State'] = location.raw['address']['state']     # list((list(location.raw.items())[7][1]).items())[5][1] # state
        df.loc[i,'Place_ID'] = location.raw['place_id']         # list(location.raw.items())[0][1] #place_id
        df.loc[i,'City'] = location.raw['address']['city' if 'city' in location.raw['address'] else 'town' if 'town' in location.raw['address'] else 'hamlet'] # alabama calls cities towns or hamlets - very strange
        df.loc[i,'County'] = location.raw['address']['county']    # list((list(location.raw.items())[7][1]).items())[4][1] # county
        df.loc[i,'zipcode'] = location.raw['address']['postcode']   # list((list(location.raw.items())[7][1]).items())[7][1] # zip code
    except:
        df.loc[i,'zipcode'] = np.nan
        df.loc[i,'Place_ID'] = np.nan
        df.loc[i,'City'] = np.nan
        df.loc[i,'County'] = np.nan
        df.loc[i,'zipcode'] = np.nan
        
    CensusGeoData = cg.coordinates(x=df.Long[i], y=df.Lat[i])
    df.loc[i,'GEOID'] = CensusGeoData ['Census Tracts'][0]['GEOID']
    df.loc[i,'TRACT'] = CensusGeoData ['Census Tracts'][0]['TRACT']
    df.loc[i,'StateID'] = CensusGeoData ['Census Tracts'][0]['STATE']
    df.loc[i,'CountyID'] = CensusGeoData ['Census Tracts'][0]['COUNTY']
    # 'B01003_001E' = population 
    # 'B19113_001E' = median income
    AcsData = censusdata.download('acs5', 2020, censusdata.censusgeo([('state', df.loc[i,'StateID'] ),  ('county', df.loc[i,'CountyID']), ('tract', df.loc[i,'TRACT'])]), ['B01003_001E','B19113_001E']).values
    df.loc[i,'TractPopulation'] = AcsData[0,0]
    df.loc[i,'TractMedianIncome'] = AcsData[0,1]
    
df.head()
df.to_csv("AL_census_pull.csv")

census_tract = pd.read_csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data/Census_FL.csv",dtype="string") 
# for i in  list(range(0,len(census_tract))):
#     print("StateID: "+census_tract.loc[i,'STATEFP'])
#     print("tract: "+str(tpye(census_tract.loc[i,'COUNTYFP'])))
#     print("CountyID: "+census_tract.loc[i,'TRACTCE'])
#     census_tract["Tract_Population"] = censusdata.download('acs5', 2020, censusdata.censusgeo([('state', census_tract.loc[i,'STATEFP']),  ('county', census_tract.loc[i,'COUNTYFP']), ('tract', census_tract.loc[i,'TRACTCE'])]), ['B01003_001E','B19113_001E']).values[0]
