#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 16:34:55 2022

@author: tomvdo29
"""
import numpy as np
import pandas as pd

HG_TN = pd.read_csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Client_Data/homegoods-tennessee.csv",skiprows=2)
HG_TN["State"] = "TN"
HG_FL = pd.read_csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Client_Data/homegoods-florida.csv",skiprows=2)
HG_FL["State"] = "FL"
HG_AL = pd.read_csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Client_Data/homegoods-alabama.csv",skiprows=2)
HG_AL["State"] = "AL"

TJM_TN = pd.read_csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Client_Data/t-j-maxx-tennessee.csv",skiprows=2)
TJM_TN["State"] = "TN"
TJM_FL = pd.read_csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Client_Data/t-j-maxx-florida.csv",skiprows=2)
TJM_FL["State"] = "FL"
TJM_AL = pd.read_csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Client_Data/t-j-maxx-alabama.csv",skiprows=2)
TJM_AL["State"] = "AL"

MS_TN = pd.read_csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Client_Data/marshalls-tennessee.csv",skiprows=2)
MS_TN["State"] = "TN"
MS_FL = pd.read_csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Client_Data/marshalls-florida.csv",skiprows=2)
MS_FL["State"] = "FL"
MS_AL = pd.read_csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Client_Data/marshalls-alabama.csv",skiprows=2)
MS_AL["State"] = "AL"

colnames = list(HG_TN.columns)

df = pd.DataFrame(columns=colnames)

for data in [HG_AL,HG_FL,HG_TN,TJM_AL,TJM_FL,TJM_AL,MS_AL,MS_FL,MS_TN]:
    #data = data.dropna().reset_index(drop=True)
    df = pd.concat([df,data], axis=0)
df = df.reset_index(drop=True)
df["Address"] = ""
for i in range(len(df.Name)):
    name_n_add = df["Name"][i].split(" / ")
    df['Name'][i] = name_n_add[0]
    df['Address'][i] = name_n_add[1]

df = df.rename(columns={"lat": "Lat", "lng": "Long", "Total Visits":"Total_Visits"},errors="raise")

df.to_csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data/Clients_Data.csv",index=False)
