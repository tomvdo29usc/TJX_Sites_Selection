#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 17:28:32 2022

@author: tomvdo29
"""
import os
import point
import pandas as pd
import numpy as np
import numpy.core.defchararray as np_f
import geopy.distance
import geopandas as gpd

os.chdir("/Users/tomvdo29/Desktop/Consulting Project/Data/Malls_Data")

AL_mall = pd.read_excel("AlabamaMalls.xlsx")
TN_mall = pd.read_excel("TenesseMalls.xlsx")
FL_mall = pd.read_excel("FloridaMalls.xlsx")

mall_data = pd.concat([AL_mall,TN_mall,FL_mall],ignore_index=True)

mall_data["State"] = np.where(mall_data["State"] == "Florida", "FL",
                              np.where(mall_data["State"] == "Tennessee", "TN",
                              np.where(mall_data["State"] == "Alabama", "AL","")))

mall_data["Total_Stores"] = mall_data["Total_Stores"].str.extract('(\d+)').astype(float)
mall_data[['Latitude','Longitude']] = mall_data[['Latitude','Longitude']].astype(str)
mall_data["mall_coords"] = mall_data["Latitude"]+","+mall_data["Longitude"]

mall_data = mall_data[["Mallname","City","State","mall_coords","Total_Stores"]]
mall_data = mall_data.fillna(0)

mall_data.to_csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data/Mall_Data.csv", index=False)