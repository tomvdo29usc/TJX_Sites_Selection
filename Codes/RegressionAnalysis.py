#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 17:19:10 2022

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
import statsmodels.api as sm

os.chdir("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data")

final_df = pd.read_csv("demo_groc_prop_tapestry_output.csv")
# final_df = final_df[(final_df.State == "FL") & (final_df.Name == "T.J. Maxx")]

print(final_df)

marshalls = final_df.drop(["State","Lat","Long","client_coords","num_grocery_stores","total_grocery_visit"], axis=1).reset_index(drop=True)
marshallsog = marshalls.fillna(0).drop(["Name"],axis=1)
Y = marshallsog.dropna().Total_Visits
X = marshallsog.dropna().drop("Total_Visits",axis=1)
X = sm.add_constant(X)
mar_model = sm.OLS(Y, X).fit()
print(mar_model.summary())



# cols = mar_model.pvalues [mar_model.pvalues < 0.20].index
# cols = list(cols)[1:]
# cols.append("Total_Visits")

# marshalls2 = marshalls[marshalls.Name == "T.J. Maxx"]
# #print(marshalls2)
# marshalls2 = marshalls2.loc[:,list(cols)[1:]]
# marshalls2 = marshalls2.fillna(0)
# #print(marshalls2)
# Y = marshalls2.dropna().Total_Visits
# x = marshalls2[list(cols)[1:]]
# x = sm.add_constant(x)
# mar_model2 = sm.OLS(Y, x).fit()

# print(mar_model2.summary())




# # Correllation Analysis
# mar_com = competitors_var[competitors_var.Name=="Marshalls"].drop(["Rank","Name","Store_Address","City","State","StoreID","Lat","Long","client_coords"], axis=1).reset_index(drop=True)
# mar_com = mar_com.apply(pd.to_numeric,errors = "coerce")
# mar_com = mar_com.dropna()
# print("Marshalls: \n",mar_com.corr().Total_Visits,"\n")

# HG_com = competitors_var[competitors_var.Name=="HomeGoods"].drop(["Rank","Name","Store_Address","City","State","StoreID","Lat","Long","client_coords"], axis=1).reset_index(drop=True)
# HG_com = HG_com.apply(pd.to_numeric,errors = "coerce")
# print("HomeGoods: \n",HG_com.corr().Total_Visits,"\n")

# TJM_com = competitors_var[competitors_var.Name=="T.J. Maxx"].drop(["Rank","Name","Store_Address","City","State","StoreID","Lat","Long","client_coords"], axis=1).reset_index(drop=True)
# TJM_com = TJM_com.apply(pd.to_numeric,errors = "coerce")
# print("TJ MAXX: \n",TJM_com.corr().Total_Visits,"\n")

# # Starbucks Correlation
# mar_star = starbucks_var[starbucks_var.Name=="Marshalls"].drop(["Rank","Name","Store_Address","City","State","StoreID","Lat","Long","client_coords"], axis=1).reset_index(drop=True)
# mar_star = mar_star.apply(pd.to_numeric,errors = "coerce")
# mar_star = mar_star.dropna()
# print("Marshalls: \n",mar_star.corr().Total_Visits,"\n")

# HG_star = starbucks_var[starbucks_var.Name=="HomeGoods"].drop(["Rank","Name","Store_Address","City","State","StoreID","Lat","Long","client_coords"], axis=1).reset_index(drop=True)
# HG_star = HG_star.apply(pd.to_numeric,errors = "coerce")
# #HG_star = HG_star.dropna()
# print("HomeGoods: \n",HG_star.corr().Total_Visits,"\n")

# TJM_star = starbucks_var[starbucks_var.Name=="T.J. Maxx"].drop(["Rank","Name","Store_Address","City","State","StoreID","Lat","Long","client_coords"], axis=1).reset_index(drop=True)
# TJM_star = TJM_star.apply(pd.to_numeric,errors = "coerce")
# #TJM_star = TJM_star.dropna()
# print("TJ MAXX: \n",TJM_star.corr().Total_Visits,"\n")



# # Regression Analysis
# import statsmodels.api as sm

# Y = mar_com.dropna().Total_Visits
# X = mar_com.dropna().drop("Total_Visits",axis=1)
# X = sm.add_constant(X)
# mar_model = sm.OLS(Y, X).fit()
# print(mar_model.summary())

# Y = HG_com.dropna().Total_Visits
# X = HG_com.dropna().drop("Total_Visits",axis=1)
# X = sm.add_constant(X)
# HG_model = sm.OLS(Y, X).fit()
# print(HG_model.summary())

# Y = TJM_com.dropna().Total_Visits
# X = TJM_com.dropna().drop("Total_Visits",axis=1)
# X = sm.add_constant(X)
# TJM_model = sm.OLS(Y, X).fit()
# print(TJM_model.summary())

    # plt.scatter(test.num_grocery_stores[test.Name=="T.J. Maxx"], test.Total_Visits[test.Name=="T.J. Maxx"],color = "orange")
    # z = np.polyfit(test.num_grocery_stores[test.Name=="T.J. Maxx"], test.Total_Visits[test.Name=="T.J. Maxx"],1)
    # p = np.poly1d(z)
    # plt.plot(test.num_grocery_stores[test.Name=="T.J. Maxx"], p(test.total_visit)[test.Name=="T.J. Maxx"],color = "orange")
    
    
    