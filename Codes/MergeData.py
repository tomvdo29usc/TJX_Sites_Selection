#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 16:48:18 2022

@author: tomvdo29
"""

import os
import point
os.chdir("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data")
import pandas as pd
import numpy as np

final_output_df = pd.read_csv("final_output.csv")
Demographics10min_df = pd.read_csv("Demographics10min.csv")
Tapestry10min_df = pd.read_csv("Tapestry10min.csv")

column_names = Demographics10min_df.columns[27:].values.tolist()
column_names.append(Demographics10min_df.columns[2])

column_names1 = Tapestry10min_df.columns[26:].values.tolist()
column_names1.append(Tapestry10min_df.columns[2])



Demographics10min_df = Demographics10min_df.loc[:, column_names]
Tapestry10min_df = Tapestry10min_df.loc[:, column_names1]


final_output_test = final_output_df.merge(Demographics10min_df,left_on='Total_Visits', right_on='Total_Visits',how='left')

final_output_test = final_output_df.merge(Tapestry10min_df,left_on='Total_Visits', right_on='Total_Visits',how='left')

final_output_test.to_csv("demo_groc_prop_tapestry_output.csv")