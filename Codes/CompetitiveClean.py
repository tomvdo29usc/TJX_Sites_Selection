#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 00:56:09 2022

@author: tomvdo29
"""

import os
import point
import pandas as pd
import numpy as np
import numpy.core.defchararray as np_f
import geopy.distance
import geopandas as gpd
from geopy import distance
import matplotlib.pyplot as plt

os.chdir("/Users/tomvdo29/Desktop/Consulting Project/Data/Competing_stores")

burlingtonAL_df = pd.read_csv("Ranked Venues - burlington-alabama (Total).csv",skiprows=2)
burlingtonAL_df['State'] = "AL"
burlingtonFL_df = pd.read_csv("Ranked Venues - burlington-florida (Total).csv",skiprows=2)
burlingtonFL_df['State'] = "FL"
burlingtonTN_df = pd.read_csv("Ranked Venues - burlington-tennessee (Total).csv",skiprows=2)
burlingtonTN_df['State'] = "TN"

KohlsAL_df = pd.read_csv("Ranked Venues - kohl-s-alabama (Total).csv",skiprows=2,index_col=None)
KohlsFL_df = pd.read_csv("Ranked Venues - kohl-s-florida (Total).csv",skiprows=2,index_col=None)
KohlsTN_df = pd.read_csv("Ranked Venues - kohl-s-tennessee (Total).csv",skiprows=2,index_col=None)
KohlsAL_df['State'] = "AL"
KohlsFL_df['State'] = "FL"
KohlsTN_df['State'] = "TN"

lowesAL_df = pd.read_csv("Ranked Venues - lowe-s-alabama (Total).csv",skiprows=2,index_col=None)
lowesFL_df = pd.read_csv("Ranked Venues - lowe-s-florida (Total).csv",skiprows=2,index_col=None)
lowesTN_df = pd.read_csv("Ranked Venues - lowe-s-tennessee (Total).csv",skiprows=2,index_col=None)
lowesAL_df['State'] = "AL"
lowesFL_df['State'] = "FL"
lowesTN_df['State'] = "TN"

rossAL_df = pd.read_csv("Ranked Venues - ross-dress-for-less-alabama (Total).csv",skiprows=2,index_col=None)
rossFL_df = pd.read_csv("Ranked Venues - ross-dress-for-less-florida (Total).csv",skiprows=2,index_col=None)
rossTN_df = pd.read_csv("Ranked Venues - ross-dress-for-less-tennessee (Total).csv",skiprows=2,index_col=None)
rossAL_df['State'] = "AL"
rossFL_df['State'] = "FL"
rossTN_df['State'] = "TN"

HomeDepotAL_df = pd.read_csv("Ranked Venues - the-home-depot-alabama (Total).csv",skiprows=2,index_col=None)
HomeDepotFL_df = pd.read_csv("Ranked Venues - the-home-depot-florida (Total).csv",skiprows=2,index_col=None)
HomeDepotTN_df = pd.read_csv("Ranked Venues - the-home-depot-tennessee (Total).csv",skiprows=2,index_col=None)
HomeDepotAL_df['State'] = "AL"
HomeDepotFL_df['State'] = "FL"
HomeDepotTN_df['State'] = "TN"

WalmartAL_df = pd.read_csv("Ranked Venues - walmart-alabama (Total).csv",skiprows=2,index_col=None)
WalmartFL_df = pd.read_csv("Ranked Venues - walmart-florida (Total).csv",skiprows=2,index_col=None)
WalmartTN_df = pd.read_csv("Ranked Venues - walmart-tennessee (Total).csv",skiprows=2,index_col=None)
WalmartAL_df['State'] = "AL"
WalmartFL_df['State'] = "FL"
WalmartTN_df['State'] = "TN"

competitors_df = pd.concat([burlingtonAL_df,burlingtonFL_df,burlingtonTN_df,
                            KohlsAL_df,KohlsFL_df,KohlsTN_df,
                            lowesAL_df,lowesFL_df,lowesTN_df,
                            rossAL_df,rossFL_df,rossTN_df,
                            HomeDepotAL_df,HomeDepotFL_df,HomeDepotTN_df,
                            WalmartAL_df,WalmartFL_df,WalmartTN_df],ignore_index=True)

competitors_df[['lat','lng']] = competitors_df[['lat','lng']].astype(str)
competitors_df["competitor_coords"] = competitors_df["lat"]+","+competitors_df["lng"]
competitors_df['Comp_Name'] = ""
competitors_df['Comp_Address'] = ""


for i in range(len(competitors_df.Name)):
    name_n_add = competitors_df["Name"][i].split(" / ")
    competitors_df['Comp_Name'][i] = name_n_add[0]
    competitors_df['Comp_Address'][i] = name_n_add[1]

competitors_df.drop(columns = "Name")
competitors_df.to_csv('competing_data.csv',index=False)
    



