#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 16:34:55 2022

@author: tomvdo29
"""
import numpy as np
import pandas as pd
import os
os.chdir("/Users/tomvdo29/Desktop/Consulting Project/Data/Starbucks_Data")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

Starbuck_FL = pd.read_csv("Starbucks_FL.csv")
Starbuck_TN = pd.read_csv("Starbucks_TN.csv")
Starbuck_AL = pd.read_csv("Starbucks_AL.csv")

Starbucks_df = pd.concat([Starbuck_FL,Starbuck_TN,Starbuck_AL],ignore_index=True)
Starbucks_df.to_csv("Starbucks_Data.csv", index = False)



#HG_ALdf.to_csv("HGData.csv")