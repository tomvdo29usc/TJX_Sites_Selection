#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 00:30:08 2022

@author: tomvdo29
"""
# This code cleans the Yardi Property Data
import os
import pandas as pd
import numpy as np
os.chdir("/Users/tomvdo29/Desktop/Consulting Project/Data/ALL_DATA")

def clean_property_data(FL_property_file,Southern_property_file):

    FL_PropertyData = pd.read_csv(FL_property_file)
    Southern_PropertyData = pd.read_csv(Southern_property_file)

    PropertyData = pd.concat([FL_PropertyData,Southern_PropertyData],axis=0)

    col_names = list(PropertyData.columns)
    print(col_names)
        
    FL_Complete_Property = FL_PropertyData[FL_PropertyData.PROPERTY_STATUS=="Completed"]
    
    print(FL_Complete_Property.PROPERTY_STUDENTHOUSING.unique())
    print(FL_Complete_Property.PROPERTY_AFFORDABLEHOUSING.unique())
    print(FL_Complete_Property.PROPERTY_MILITARYHOUSING.unique())
    print(FL_Complete_Property.PROPERTY_AGERESTRICTED.unique())
    print(FL_Complete_Property.PROPERTY_FRACTUREDCONDO.unique())
    print(FL_Complete_Property.PROPERTY_ADAPTIVEREUSE.unique())
    print(FL_Complete_Property.PROPERTY_SINGLEFAMILYRENTAL.unique())
    
    print((FL_Complete_Property.PROPERTY_STUDENTHOUSING.isnull()).sum())
    
    df = PropertyData.loc[:, ['PROPERTY_ID', 'PROPERTY_NAME','PROPERTY_ADDRESS',
                              'PROPERTY_CITY', 'COUNTY_NAME', 'PROPERTY_STATE', 'PROPERTY_ZIPCODE',
                              'PROPERTY_LATITUDE', 'PROPERTY_LONGITUDE', 'PROPERTY_UNITS', 
                              'PROPERTY_SQFT', 'PROPERTY_IMPRATING', 'PROPERTY_LOCRATING', 
                              'PROPERTY_STATUS', 'PROPERTY_STUDENTHOUSING', 'PROPERTY_AFFORDABLEHOUSING', 
                              'PROPERTY_MILITARYHOUSING', 'PROPERTY_AGERESTRICTED', 'PROPERTY_FRACTUREDCONDO', 
                              'PROPERTY_ADAPTIVEREUSE', 'PROPERTY_SINGLEFAMILYRENTAL', 
                              'PROPERTY_CURRENT_OCCUPANCY', 'PROPERTY_CURRENT_RENT','PROPERTY_MIXEDUSE',
                              'PROPERTY_MIXEDUSE_NOTES']]
    
    df = df[df.PROPERTY_STATE.isin(["FL","AL","TN"])]


    df["Impr_Rating"] = np.where(df.PROPERTY_IMPRATING == "A+",9,
                        np.where(df.PROPERTY_IMPRATING == "A",8,
                        np.where(df.PROPERTY_IMPRATING == "A-",7,
                        np.where(df.PROPERTY_IMPRATING == "B+",6,
                        np.where(df.PROPERTY_IMPRATING == "B",5,
                        np.where(df.PROPERTY_IMPRATING == "B-",4,
                        np.where(df.PROPERTY_IMPRATING == "C+",3,
                        np.where(df.PROPERTY_IMPRATING == "C",2,
                        np.where(df.PROPERTY_IMPRATING == "C-",1,
                        np.where(df.PROPERTY_IMPRATING == "D",0,np.nan)))))))))).astype(float)
    
    df["Loc_Rating"] =  np.where(df.PROPERTY_LOCRATING == "A+",9,
                        np.where(df.PROPERTY_LOCRATING == "A",8,
                        np.where(df.PROPERTY_LOCRATING == "A-",7,
                        np.where(df.PROPERTY_LOCRATING == "B+",6,
                        np.where(df.PROPERTY_LOCRATING == "B",5,
                        np.where(df.PROPERTY_LOCRATING == "B-",4,
                        np.where(df.PROPERTY_LOCRATING == "C+",3,
                        np.where(df.PROPERTY_LOCRATING == "C",2,
                        np.where(df.PROPERTY_LOCRATING == "C-",1,
                        np.where(df.PROPERTY_LOCRATING == "D",0,np.nan))))))))))
    
    df["Impr_Rating"] = np.where(df.Impr_Rating >= 8, "Discretionary",
                        np.where(df.Impr_Rating >= 6, "High Mid-Range",
                        np.where(df.Impr_Rating >= 4, "Low Mid-Range",
                        np.where(df.Impr_Rating >= 0, "Workforce", ""))))
    df["Loc_Rating"] =  np.where(df.Loc_Rating >= 8, "Discretionary",
                        np.where(df.Loc_Rating >= 6, "High Mid-Range",
                        np.where(df.Loc_Rating >= 4, "Low Mid-Range",
                        np.where(df.Loc_Rating >= 0, "Workforce", ""))))
    
    
    df["Property_Overall_Rating"] = df.loc[:,['Impr_Rating','Loc_Rating']].mean(axis=1,skipna = float)
    df["Property_Overall_Rating"] = np.where(df.Property_Overall_Rating >= 8, "Discretionary",
                                    np.where(df.Property_Overall_Rating >= 6, "High Mid-Range",
                                    np.where(df.Property_Overall_Rating >= 4, "Low Mid-Range",
                                    np.where(df.Property_Overall_Rating >= 0, "Workforce", ""))))
    
    df["Student_Housing"] = np.where(df.PROPERTY_STUDENTHOUSING == "N", 0,
                            np.where(df.PROPERTY_STUDENTHOUSING.isin(["A","P"]), 1, np.nan))
    
    df["Affordable_Housing"] = np.where(df.PROPERTY_AFFORDABLEHOUSING == "N", 0,
                            np.where(df.PROPERTY_AFFORDABLEHOUSING.isin(["A","P"]), 1, np.nan))
    
    df["Military_Housing"] = np.where(df.PROPERTY_MILITARYHOUSING == "N", 0,
                            np.where(df.PROPERTY_MILITARYHOUSING.isin(["A","P"]), 1, np.nan))
    
    df["Senior_Housing"] = np.where(df.PROPERTY_AGERESTRICTED == "N", 0,
                            np.where(df.PROPERTY_AGERESTRICTED.isin(["A","P"]), 1, np.nan))
    
    df["Fractured_Condo"] = np.where(df.PROPERTY_FRACTUREDCONDO == "N", 0,
                            np.where(df.PROPERTY_FRACTUREDCONDO.isin(["A","P"]), 1, np.nan))
    
    df["Adaptive_Reuse"] = np.where(df.PROPERTY_ADAPTIVEREUSE == True, 1,
                            np.where(df.PROPERTY_ADAPTIVEREUSE == False, 0, np.nan))
    
    df["Single_Family_Rental"] = np.where(df.PROPERTY_SINGLEFAMILYRENTAL == True, 1,
                            np.where(df.PROPERTY_SINGLEFAMILYRENTAL == False, 0, np.nan))
    
    df["Mixed_Use"] = np.where(df.PROPERTY_MIXEDUSE == True, 1,
                            np.where(df.PROPERTY_MIXEDUSE == False, 0, np.nan))
    
    sqft_mixed_use = []
    for note in df['PROPERTY_MIXEDUSE_NOTES']:
        if type(note) == str:
            numbers = np.array([float(num) for num in note.replace(",","").split(" ") if num.isdigit()])
            sqft_mixed_use.append(sum(numbers))
        else:
            sqft_mixed_use.append(0)
    
    sqft_mixed_use = np.array(sqft_mixed_use)
    
    df["sqft_mixed_use"] = sqft_mixed_use
    
    
    return df

if __name__ == '__main__':
    FL_property_file = "/Users/tomvdo29/Desktop/Consulting Project/Data/FL_Property_Data/FloridaPropertyData.csv"
    Southern_property_file = "/Users/tomvdo29/Desktop/Consulting Project/Data/South_Property_Data/SouthPropertyData.csv"
    all_property_data = clean_property_data(FL_property_file,Southern_property_file)
    
    os.chdir("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data")
    all_property_data.to_csv("Properties_Data_3States.csv")

# df.to_csv("all_property.csv")