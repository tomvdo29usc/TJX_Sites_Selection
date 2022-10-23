#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 23:55:18 2022

@author: tomvdo29
"""
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
from joblib import Parallel, delayed
import os
os.chdir("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data")

AL_tract = gpd.read_file("/Users/tomvdo29/Desktop/Consulting Project/Data/All_Tracts/AL_Tract/tl_2022_01_tract.shp")
FL_tract = gpd.read_file("/Users/tomvdo29/Desktop/Consulting Project/Data/All_Tracts/FL_Tract/tl_2022_12_tract.shp")
TN_tract = gpd.read_file("/Users/tomvdo29/Desktop/Consulting Project/Data/All_Tracts/TN_Tract/tl_2022_47_tract.shp")

All_States_Tract = gpd.GeoDataFrame(pd.concat([AL_tract, FL_tract, TN_tract])).reset_index(drop=True)
All_States_Tract = pd.DataFrame(All_States_Tract.drop(columns='geometry'))

All_States_Tract['Household_Income_0-25K'] = np.nan
All_States_Tract['Household_Income_25K-50K'] = np.nan
All_States_Tract['Household_Income_50K-75K'] = np.nan
All_States_Tract['Household_Income_75K-100K'] = np.nan
All_States_Tract['Household_Income_100K-150K'] = np.nan
All_States_Tract['Household_Income_150K+'] = np.nan


def censustract(i):
    tract_pop_array = []
    tract_med_income = [] 
    state = str(All_States_Tract['STATEFP'][i])
    tract = str(All_States_Tract['TRACTCE'][i])
    county = str(All_States_Tract['COUNTYFP'][i])
    
    
    AcsData = censusdata.download('acs5', 2020, censusdata.censusgeo([('state',state),
                                                                      ('county',county), 
                                                                      ('tract',tract)]), 
                                  ['B19101_002E','B19101_003E','B19101_004E','B19101_005E','B19101_006E',
                                   'B19101_007E','B19101_008E','B19101_009E','B19101_010E','B19101_011E',
                                   'B19101_012E','B19101_013E','B19101_014E','B19101_015E','B19101_016E',"B19101_017E"],
                                  key = "456cc172706c0e88d800aa401a0daef16a303b00").values
    
    # All_States_Tract.loc[i,'Household_Income_0-25K'] = AcsData[0,0]+AcsData[0,1]+AcsData[0,2] + AcsData[0,3]
    # All_States_Tract.loc[i,'Household_Income_25K-50K'] = AcsData[0,4]+AcsData[0,5]+AcsData[0,6] + AcsData[0,7] + AcsData[0,8]
    # All_States_Tract.loc[i,'Household_Income_50K-75K'] = AcsData[0,9] + AcsData[0,10]
    # All_States_Tract.loc[i,'Household_Income_75K-100K'] = AcsData[0,11]
    # All_States_Tract.loc[i,'Household_Income_100K-150K'] = AcsData[0,12] + AcsData[0,13]
    # All_States_Tract.loc[i,'Household_Income_150K+'] = AcsData[0,14] + AcsData[0,15]
    
    return AcsData[0,0]+AcsData[0,1]+AcsData[0,2]+AcsData[0,3],AcsData[0,4]+AcsData[0,5]+\
           AcsData[0,6]+AcsData[0,7]+AcsData[0,8],AcsData[0,9]+AcsData[0,10],AcsData[0,11],\
           AcsData[0,12]+AcsData[0,13],AcsData[0,14]+AcsData[0,15]
    #tract_med_income.append(AcsData[0,1])
    
    
results = Parallel(n_jobs=20)(delayed(censustract)(i) for i in range(0,len(All_States_Tract)))

# All_States_Tract["Tract_Population"] = np.array(results)
for i in range(len(results)):
    All_States_Tract.loc[i,'Household_Income_0-25K'] = results[i][0]
    All_States_Tract.loc[i,'Household_Income_25K-50K'] = results[i][1]
    All_States_Tract.loc[i,'Household_Income_50K-75K'] = results[i][2]
    All_States_Tract.loc[i,'Household_Income_75K-100K'] = results[i][3]
    All_States_Tract.loc[i,'Household_Income_100K-150K'] = results[i][4]
    All_States_Tract.loc[i,'Household_Income_150K+'] = results[i][5]

