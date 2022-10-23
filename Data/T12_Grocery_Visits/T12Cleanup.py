#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 16:34:55 2022

@author: tomvdo29
"""
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

Rank = []
Name = []
Address = []
State = []
Total_Visits = []
Lat = []
Long = []
Plotted	= []
Percentile = []


t12_TN = open("/Users/tomvdo29/Desktop/Consulting Project/Data/T12_Grocery_Visits/T12_TN Grocery.csv")
t12_FL = open("/Users/tomvdo29/Desktop/Consulting Project/Data/T12_Grocery_Visits/T12_FL Grocery.csv")
t12_AL = open("/Users/tomvdo29/Desktop/Consulting Project/Data/T12_Grocery_Visits/T12_AL Grocery.csv")
def cleaned_store_data(file):
    for line in file.readlines()[2:]:
        actual_line = line.strip('\n').split('"')
        add_n_store = actual_line[1]
        address = add_n_store.split(" / ")[1]
        print(address)
        
        Rank.append(int(actual_line[0].strip(",")))
        Address.append(address)
        Name.append(add_n_store.split(" / ")[0])
        
        state=address.split(",")[-2].strip(" ")
        if state=="Florida":
            State.append("FL")
        elif state=="Alabama":
            State.append("AL")
        elif state=="Tennesse":
            State.append("TN")
        else:
            State.append(state)
            
        other_info = actual_line[2].lstrip(",").split(",")
        Total_Visits.append(other_info[0])
        Lat.append(other_info[1])
        Long.append(other_info[2])
        Plotted.append(other_info[4])
        Percentile.append(other_info[5])
            
    output = pd.DataFrame(list(zip(Rank,Name,Address,State,Total_Visits,Lat,Long,Plotted,Percentile)),
                        columns = ["Rank","Name","Address","State","Total_Visits","Lat","Long","Plotted","Percentile"])
    file.close()
    return output

t12_TNdf = cleaned_store_data(t12_TN)
print(t12_TNdf)

t12_FLdf = cleaned_store_data(t12_FL)
print(t12_FLdf)

t12_ALdf = cleaned_store_data(t12_AL)
print(t12_ALdf)

#Mar_ALdf.to_csv("TJMaxData.csv")