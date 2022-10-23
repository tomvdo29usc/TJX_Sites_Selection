#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 15:47:55 2022

@author: tomvdo29, Chris
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

os.chdir("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data")

def nearby_supermarkets_analysis(client_file,grocery_file,state):
    
    # Read client_file and filter state
    clientDF = pd.read_csv(client_file)
    clientDF = clientDF[["Rank","Name","State","Lat","Long","Total_Visits"]]
    clientDF = clientDF[clientDF["State"].isin(state)].reset_index(drop=True)
    clientDF[['Lat','Long']] = clientDF[['Lat','Long']].astype(str)

    
    # Read grocery_file and filter state
    groceryDF = pd.read_csv(grocery_file)
    groceryDF = groceryDF[groceryDF.State.isin(state)].reset_index(drop=True)
    groceryDF[['Lat','Long']] = groceryDF[['Lat','Long']].astype(str)
    
    # Merge latitude and longitude into a string coords "lat,long"
    clientDF["client_coords"] = clientDF["Lat"]+","+clientDF["Long"]
    groceryDF["grocery_coords"] = groceryDF["Lat"]+","+groceryDF["Long"]
    
    # See what grocery stores are there in the data
    
    # Establish new variable name: "name num_stores_" + name of grocery store
    # to count how many of that grocery brand within the client radius
    numstore_col_names = ("num_stores_"+groceryDF.Name.unique())
    numstore_col_names = [name.replace(' ','_') for name in numstore_col_names]
    
    # Establish new variable name: "store_visit_" + name of grocery store
    # to store total visit of that grocery brand within the client radius
    storevisit_col_names = ("total_visit_"+groceryDF.Name.unique())
    storevisit_col_names = [name.replace(' ','_') for name in storevisit_col_names]


    numstore_list = [] # To keep track the total number of all grocery stores
    total_visit = [] # To keep track the total visit of all grocery stores
    
    # Put new variables name into a dataframe format
    df_num_store = pd.DataFrame(columns=numstore_col_names)
    df_store_visits = pd.DataFrame(columns=storevisit_col_names)
    
    # Loop through every client store
    for a in range(len(clientDF["client_coords"])):
        num_stores = 0 # Total number of grocery stores sets at 0
        visits = 0 # Total visit to all grocery stores sets at 0
        
        # Create dataframe to count whether number of grocery stores and append
        # the number of visit of that store if it is within the client radius
        df_num_store_running = pd.DataFrame(columns=numstore_col_names)
        df_store_visits_running = pd.DataFrame(columns=storevisit_col_names)
        
        for b in range(len(groceryDF["grocery_coords"])):
            
            dis = geopy.distance.geodesic(clientDF["client_coords"][a], groceryDF["grocery_coords"][b]).miles
            
            if dis <= 3: # Set radius equal 3 miles
            
                # Set 1 if the store is within the client radius or 0 otherwise
                # then append to the df_num_store_running
                index_numstore = list(numstore_col_names).index(("num_stores_"+groceryDF.Name[b]).replace(' ','_'))
                lst_numstore = [0]*len(numstore_col_names)
                lst_numstore[index_numstore] = 1
                num_store_dic = dict(zip(numstore_col_names,lst_numstore))
                df_num_store_running = pd.concat([df_num_store_running,pd.DataFrame(num_store_dic,index=[0])],ignore_index=True)
                
                # Update the grocery store visit if the grocery store is within
                # the client radius and NULL otherwise
                index_storevisits = list(storevisit_col_names).index(("total_visit_"+groceryDF.Name[b]).replace(' ','_'))
                lst_storevisits = [np.nan]*len(storevisit_col_names)
                lst_storevisits[index_storevisits] = groceryDF.Total_Visits[b]
                store_visit_dic = dict(zip(storevisit_col_names,lst_storevisits))
                df_store_visits_running= pd.concat([df_store_visits_running,pd.DataFrame(store_visit_dic,index=[0])],ignore_index=True)
                
                # Update the number of grocery store when it's within the client radius
                num_stores+=1
                
                # Update the number of grocery store visit if the store is within the client radius
                visits += groceryDF["Total_Visits"][b]
            
        # Append to the list 
        numstore_list.append(num_stores)
        total_visit.append(visits)
        
        # Find the total number and the total visit of each grocery brand and append
        # to the keep-trach dataframe
        df_num_store = df_num_store.append(df_num_store_running[numstore_col_names].sum(),ignore_index=True)#pd.concat([df_result,pd.DataFrame()df[col_names].sum()],axis = 0,ignore_index=True)
        df_store_visits = df_store_visits.append(df_store_visits_running[storevisit_col_names].sum(),ignore_index=True)
        #print(df_num_store)
        #print(df_result)
    
    # Merge all the keeping-trach result to the output dataframe 
    clientDF = pd.concat([clientDF,df_num_store],axis = 1)
    clientDF = pd.concat([clientDF,df_store_visits],axis = 1)
    clientDF["num_grocery_stores"] = np.array(numstore_list)
    clientDF["total_grocery_visit"] = np.array(total_visit)
    
    return clientDF
        
def nearby_properties_analysis(client_file,real_estate,state):
    
    # Read client_file and filter state
    clientDF = pd.read_csv(client_file)
    clientDF = clientDF[["Rank","Name","State","Lat","Long","Total_Visits"]]
    clientDF = clientDF[clientDF["State"].isin(state)].reset_index(drop=True)

    
    # Read Yardi data and filter out states
    propertyDF = pd.read_csv(real_estate)
    propertyDF = propertyDF[propertyDF.PROPERTY_STATE.isin(state)].reset_index()
    # propertyDF = propertyDF[propertyDF.PROPERTY_STATUS == "Completed"].reset_index() # Filter out completed properties
    propertyDF["Unit_size"] = propertyDF.PROPERTY_SQFT/propertyDF.PROPERTY_UNITS # Estimate unit size
    
    # Merge lat and long into a single coordinate for both file
    clientDF[['Lat','Long']] = clientDF[['Lat','Long']].astype(str)
    propertyDF[['PROPERTY_LATITUDE','PROPERTY_LONGITUDE']] = propertyDF[['PROPERTY_LATITUDE','PROPERTY_LONGITUDE']].astype(str)
    clientDF["client_coords"] = clientDF["Lat"]+","+clientDF["Long"]
    propertyDF["property_coords"] = propertyDF["PROPERTY_LATITUDE"]+","+propertyDF["PROPERTY_LONGITUDE"]
    # Make dictionaries to store results of number of properties, 
    # average sqft, and average rent by type of apartments
    numsproperty_dict = {"Discretionary":[], "High-Mid-Range":[],"Low-Mid-Range":[], "Workforce":[]}
    property_sqft = {"Discretionary":[], "High-Mid-Range":[],"Low-Mid-Range":[], "Workforce":[]}
    property_rent = {"Discretionary":[], "High-Mid-Range":[],"Low-Mid-Range":[], "Workforce":[]}
    
    # Make dataframe to store results of number of apartments by type of housing 
    # categories
    type_rent_dict = {"Student_Housing":[], "Affordable_Housing":[],"Military_Housing":[], 
                 "Senior_Housing":[], "Adaptive_Reuse":[], "Single_Family_Rental":[]}
    type_rent = pd.DataFrame.from_dict(type_rent_dict)
    
    property_status_dict = {"Completed":[], "Planned":[],"Prospective":[], "Under_Construction":[]}
    property_status = pd.DataFrame.from_dict(property_status_dict)
    # Loop through every client stores
    for a in range(len(clientDF["client_coords"])):
        # Make dictionaries and dataframe to keep track of properties that 
        # are within the the client store radius 
        num_prop_status = {"Completed":0, "Planned":0,"Prospective":0, "Under_Construction":0}
        num_prop = {"Discretionary":0, "High-Mid-Range":0,"Low-Mid-Range":0, "Workforce":0}
        running_sqft = {"Discretionary":[], "High-Mid-Range":[],"Low-Mid-Range":[], "Workforce":[]}
        running_rent = {"Discretionary":[], "High-Mid-Range":[],"Low-Mid-Range":[], "Workforce":[]}
        type_rent_df = pd.DataFrame(columns=type_rent_dict.keys())
        
        current_state = clientDF['State'][a]
        current_state_props = propertyDF[propertyDF.PROPERTY_STATE == current_state].reset_index(drop=True)
        
        # Loop through every property
        for b in range(len(current_state_props["property_coords"])):
            dis = geopy.distance.geodesic(clientDF["client_coords"][a], current_state_props["property_coords"][b]).miles
            if dis <= 3.5: # Set radius as 3 miles
                
                # Update 1 to each type of rent if the property satisfies conditions
                # to each type of rent: StudentHousing,...
                type_rent_df = type_rent_df.append(current_state_props.loc[b,'Student_Housing':'Single_Family_Rental'],ignore_index=True)
            
                if type(current_state_props["PROPERTY_STATUS"][b]) == str:
                    num_prop_status[current_state_props["PROPERTY_STATUS"][b].replace(" ","_")] += 1
                
                # Update number of properies and append the sqft and rent amount
                # according to its overall ratings if the property if within the radius 
                if "Discretionary" in [current_state_props.Impr_Rating[b],current_state_props.Loc_Rating[b]]:
                    num_prop["Discretionary"] += 1
                    running_sqft["Discretionary"].append(current_state_props["Unit_size"][b])
                    running_rent["Discretionary"].append(current_state_props["PROPERTY_CURRENT_RENT"][b])
                    
                elif "High Mid-Range" in [current_state_props.Impr_Rating[b],current_state_props.Loc_Rating[b]]:
                    num_prop["High-Mid-Range"] += 1
                    running_sqft["High-Mid-Range"].append(current_state_props["Unit_size"][b])
                    running_rent["High-Mid-Range"].append(current_state_props["PROPERTY_CURRENT_RENT"][b])
                    
                elif "Low Mid-Range" in [current_state_props.Impr_Rating[b],current_state_props.Loc_Rating[b]]:
                    num_prop["Low-Mid-Range"] += 1
                    running_sqft["Low-Mid-Range"].append(current_state_props["Unit_size"][b])
                    running_rent["Low-Mid-Range"].append(current_state_props["PROPERTY_CURRENT_RENT"][b])
                    
                elif "Workforce" in [current_state_props.Impr_Rating[b],current_state_props.Loc_Rating[b]]:
                    num_prop["Workforce"] += 1
                    running_sqft["Workforce"].append(current_state_props["Unit_size"][b])
                    running_rent["Workforce"].append(current_state_props["PROPERTY_CURRENT_RENT"][b])     
        property_status = property_status.append(pd.DataFrame([num_prop_status]),ignore_index=True)
        print(num_prop_status)
        type_rent = type_rent.append(type_rent_df.sum(),ignore_index=True)
        
        # Find mean of sqft and rent amount
        for i in ["Discretionary","High-Mid-Range","Low-Mid-Range","Workforce"]:
            numsproperty_dict[i].append(num_prop[i])
            
            
            sqft_arr = (np.array(running_sqft[i]))
            sqft_arr = sqft_arr[sqft_arr != 0]
            sqft_arr = sqft_arr[~np.isnan(sqft_arr)]
            property_sqft[i].append(np.mean(sqft_arr))
            
            rent_arr = (np.array(running_rent[i]))
            rent_arr = rent_arr[rent_arr != 0]
            rent_arr = rent_arr[~np.isnan(rent_arr)]
            property_rent[i].append(np.mean(rent_arr))
        
            
            
    # Update the final output
    clientDF["num_Discretionary"] = np.array(numsproperty_dict["Discretionary"])
    clientDF["num_High-Mid-Range"] = np.array(numsproperty_dict["High-Mid-Range"])
    clientDF["num_Low-Mid-Range"] = np.array(numsproperty_dict["Low-Mid-Range"])
    clientDF["num_Workforce"] = np.array(numsproperty_dict["Workforce"])
    
    clientDF["avg_sqft_Discretionary"] = np.array(property_sqft["Discretionary"])
    clientDF["avg_sqft_High_Mid-Range"] = np.array(property_sqft["High-Mid-Range"])
    clientDF["avg_sqft_Low-Mid-Range"] = np.array(property_sqft["Low-Mid-Range"])
    clientDF["avg_sqft_Workforce"] = np.array(property_sqft["Workforce"])
    
    clientDF["avg_rent_Discretionary"] = np.array(property_rent["Discretionary"])
    clientDF["avg_rent_High_Mid-Range"] = np.array(property_rent["High-Mid-Range"])
    clientDF["avg_rent_Low-Mid-Range"] = np.array(property_rent["Low-Mid-Range"])
    clientDF["avg_rent_Workforce"] = np.array(property_rent["Workforce"])
    
    
    
    clientDF = pd.concat([clientDF, type_rent], axis = 1)
    clientDF = pd.concat([clientDF, property_status], axis = 1)
    
    return clientDF        
    

def competitor_analysis(client_data,competing_data,state):
    # Read client data and filter state
    clientDF = pd.read_csv(client_data)
    clientDF = clientDF[["Rank","Name","State","Lat","Long","Total_Visits"]]
    clientDF = clientDF[clientDF["State"].isin(state)].reset_index(drop=True)
    clientDF[['Lat','Long']] = clientDF[['Lat','Long']].astype(str)
    clientDF["client_coords"] = clientDF["Lat"]+","+clientDF["Long"]
    
    
    # Create client self dataframe to map its stores to each self to 
    # find cannibalization patterns
    self_df = clientDF.loc[:,["Name","State","Total_Visits","client_coords"]].reset_index(drop=True)
    self_df = self_df.rename(columns={"client_coords": "competitor_coords","Name":"Comp_Name"})
    
    # Read competitor data and filter state
    competitorsDF = pd.read_csv(competing_data)
    competitorsDF = competitorsDF[competitorsDF["State"].isin(state)].reset_index(drop=True)
    competitorsDF = competitorsDF.loc[:,["Comp_Name","State","Total_Visits","competitor_coords"]].reset_index(drop=True)
    
    # Merge self stores data to competitor data into a big dataframe
    comp_self_DF = pd.concat([competitorsDF,self_df],ignore_index=True)
    
    # Find unique brand names in the data
    num_nearby_stores = ("num_nearby_"+comp_self_DF.Comp_Name.unique())
    num_nearby_stores = [name.replace(' ','_') for name in num_nearby_stores]
    visits_nearby_stores = ("tot_visits_nearby_"+comp_self_DF.Comp_Name.unique())
    visits_nearby_stores = [name.replace(' ','_') for name in visits_nearby_stores]
    
    # Make dataframe that stores the number and total visit of TJX brands and 
    # competitor brands within radius from each TJX brand store
    num_nearby_stores_output = pd.DataFrame(columns=num_nearby_stores)
    visits_nearby_stores_output = pd.DataFrame(columns=visits_nearby_stores)
    
    # Loop through every client store
    for a in range(len(clientDF["client_coords"])):
        df_num_nearby_stores = pd.DataFrame(columns=num_nearby_stores)
        df_visits_nearby_stores = pd.DataFrame(columns=visits_nearby_stores)
        
        
        # Loop through every competitor and self store data
        for b in range(len(comp_self_DF["competitor_coords"])):
            dis = geopy.distance.geodesic(clientDF["client_coords"][a], comp_self_DF["competitor_coords"][b]).miles
            if dis>0 and dis < 10: # Radius within 10 miles
                
                # Set 1 if the store is within the client radius or 0 otherwise
                # then append to the df_num_nearby_stores
                index_nearby_stores = list(num_nearby_stores).index(("num_nearby_"+comp_self_DF.Comp_Name[b]).replace(' ','_'))
                lst_nearby_stores = [0]*len(num_nearby_stores)
                lst_nearby_stores[index_nearby_stores] = 1
                num_nearby_stores_dic = dict(zip(num_nearby_stores,lst_nearby_stores))
                df_num_nearby_stores = pd.concat([df_num_nearby_stores,pd.DataFrame(num_nearby_stores_dic,index=[0])],ignore_index=True) 
                
                # Set store visit amount if the competitor is within the client radius 
                # radius or NULL otherwise then append to the df_num_nearby_stores
                index_visits_nearby_stores = list(visits_nearby_stores).index(("tot_visits_nearby_"+comp_self_DF.Comp_Name[b]).replace(' ','_'))
                lst_visits_nearby_stores = [np.nan]*len(visits_nearby_stores)
                lst_visits_nearby_stores[index_visits_nearby_stores] = comp_self_DF.Total_Visits[b]
                visits_nearby_stores_dic = dict(zip(visits_nearby_stores,lst_visits_nearby_stores))
                df_visits_nearby_stores = pd.concat([df_visits_nearby_stores,pd.DataFrame(visits_nearby_stores_dic,index=[0])],ignore_index=True) 
        
        # Sum all number of nearby competitor store and its visit
        num_nearby_stores_output = num_nearby_stores_output.append(df_num_nearby_stores[num_nearby_stores].sum(),ignore_index=True)
        visits_nearby_stores_output = visits_nearby_stores_output.append(df_visits_nearby_stores[visits_nearby_stores].sum(min_count=1),ignore_index=True)
        print(visits_nearby_stores_output)
        
    # Update the final output
    clientDF = pd.concat([clientDF,num_nearby_stores_output],axis = 1)
    clientDF = pd.concat([clientDF,visits_nearby_stores_output],axis = 1)
    
    return clientDF

def starbucks_analysis(client_data,starbucks_data,state):
    # Read client data and filter state
    clientDF = pd.read_csv(client_data)
    clientDF = clientDF[["Rank","Name","State","Lat","Long","Total_Visits"]]
    clientDF = clientDF[clientDF["State"].isin(state)].reset_index(drop=True)
    clientDF[['Lat','Long']] = clientDF[['Lat','Long']].astype(str)
    clientDF["client_coords"] = clientDF["Lat"]+","+clientDF["Long"]
    
    # Read client data and filter state
    starbucksDF = pd.read_csv(starbucks_data)
    starbucksDF = starbucksDF[starbucksDF["State.Province"].isin(state)].reset_index(drop=True)
    starbucksDF[['Latitude','Longitude']] = starbucksDF[['Latitude','Longitude']].astype(str)
    starbucksDF["starbucks_coords"] = starbucksDF["Latitude"]+","+starbucksDF["Longitude"]
    
    num_starbucks_list = [] # To keep track the total number of all starbucks stores
    
    
    # Loop through every client stores
    for a in range(len(clientDF["client_coords"])):
        
        num_starbucks = 0 # Total number of grocery stores sets at 0
        
        # Loop through every property
        for b in range(len(starbucksDF["starbucks_coords"])):
            dis = geopy.distance.geodesic(clientDF["client_coords"][a], starbucksDF["starbucks_coords"][b]).miles
            if dis <= 0.7: # Set radius as 3 miles
                num_starbucks += 1
        
        num_starbucks_list.append(num_starbucks)
        
    clientDF["num_starbucks"] = np.array(num_starbucks_list)
    clientDF["has_starbucks"] = np.where(clientDF["num_starbucks"] > 0,1,0)
            
    return clientDF

def mall_analysis(client_data,mall_data,state):
    # Read client data and filter state
    clientDF = pd.read_csv(client_data)
    clientDF = clientDF[["Rank","Name","State","Lat","Long","Total_Visits"]]
    clientDF = clientDF[clientDF["State"].isin(state)].reset_index(drop=True)
    clientDF[['Lat','Long']] = clientDF[['Lat','Long']].astype(str)
    clientDF["client_coords"] = clientDF["Lat"]+","+clientDF["Long"]
    
    # Read mall data and filter state
    mallsDF = pd.read_csv(mall_data)
    mallsDF = mallsDF[mallsDF["State"].isin(state)].reset_index(drop=True)
    
    num_malls_list = [] # To keep track the total number of all starbucks stores
    num_stores_list = []
    
    # Loop through every client stores
    for a in range(len(clientDF["client_coords"])):
        
        num_malls = 0 # Total number of grocery stores sets at 0
        num_stores = 0
        # Loop through every property
        for b in range(len(mallsDF["mall_coords"])):
            dis = geopy.distance.geodesic(clientDF["client_coords"][a], mallsDF["mall_coords"][b]).miles
            if dis <= 3: # Set radius as 3 miles
                num_malls += 1
                num_stores += mallsDF["Total_Stores"][b]
        
        num_malls_list.append(num_malls)
        num_stores_list.append(num_stores)
        
    clientDF["num_malls"] = np.array(num_malls_list)
    clientDF["tot_stores"] = np.array(num_stores_list)
    
            
    return clientDF

def census_analytics(client_data,census_data,state):
    # Read client data and filter state
        
    
    clientDF = pd.read_csv(client_data)
    clientDF = clientDF[["Rank","Name","State","Lat","Long","Total_Visits"]]
    clientDF = clientDF[clientDF["State"].isin(state)].reset_index(drop=True)
    clientDF[['Lat','Long']] = clientDF[['Lat','Long']].astype(str)
    clientDF["client_coords"] = clientDF["Lat"]+","+clientDF["Long"]

    for i in range(len(state)):
        if state[i] == "FL":
            state[i] = 12
        elif state[i] == "AL":
            state[i] = 1
        else:
            state[i] = 47
            
    # Read mall data and filter state
    censusDF = pd.read_csv(census_data)
    censusDF = censusDF[censusDF["STATEFP"].isin(state)].reset_index(drop=True)
    censusDF[['INTPTLAT','INTPTLON']] = censusDF[['INTPTLAT','INTPTLON']].astype(str)
    censusDF["tract_coords"] = censusDF["INTPTLAT"]+","+censusDF["INTPTLON"]
    
    income_cols = ["Household_Income_0-25K","Household_Income_25K-50K",
                   "Household_Income_50K-75K","Household_Income_75K-100K",
                   "Household_Income_100K-150K","Household_Income_150K+"]
    final_incomeDF = pd.DataFrame(columns=income_cols)
    # Loop through every client stores
    for a in range(len(clientDF["client_coords"])):
        running_income = pd.DataFrame(columns=income_cols)
        # Loop through every property
        for b in range(len(censusDF["tract_coords"])):
            dis = geopy.distance.geodesic(clientDF["client_coords"][a], censusDF["tract_coords"][b]).miles
            if dis <= 5: # Set radius as 3 miles
                census_income_record = censusDF.loc[[b],income_cols]
                running_income = pd.concat([running_income,census_income_record], ignore_index = True)
        final_incomeDF = pd.concat([final_incomeDF,running_income.agg(['sum'])], ignore_index = True)
        print(final_incomeDF)
    clientDF = pd.concat([clientDF,final_incomeDF],axis = 1)
    
            
    return clientDF

###############################################################################
client_file = 'Clients_Data.csv'
grocery_file = 'T12Data.csv'
real_estate = "Properties_Data_3States.csv"
competitor_data = "competing_data.csv"
starbucks_data = "Starbucks_Data.csv"
mall_data = "Mall_Data.csv"
census_data = "tract_income.csv"
states = ["FL","TN","AL"]
groceries_var=nearby_supermarkets_analysis(client_file, grocery_file,states)
#groceries_var.to_csv("groceries_output<3miles.csv",index=False)

properties_var = nearby_properties_analysis(client_file, real_estate,states)
#properties_var.to_csv("properties_output<3miles.csv", index=False)

competitors_var = competitor_analysis(client_file, competitor_data,states)
#competitors_var.to_csv("competing_output<10miles.csv", index=False)

starbucks_var = starbucks_analysis(client_file, starbucks_data,states)
#starbucks_var.to_csv("starbucks_var<0.7miles.csv", index=False)

mall_var = mall_analysis(client_file, mall_data,states)
#mall_var.to_csv("mall<3miles.csv", index=False)

#census_var = census_analytics(client_file,census_data,["FL"])



#Joining all output:
final_data = groceries_var
for data in [properties_var,competitors_var,starbucks_var,mall_var]:
    col_names = data.columns[7:].values.tolist()
    col_names.append(data.columns[5])
    data = data.loc[:, col_names]
    
    final_data = final_data.merge(data,left_on='Total_Visits', right_on='Total_Visits',how='left')

Demographics10min_df = pd.read_csv("Demographics10min.csv")
Tapestry10min_df = pd.read_csv("Tapestry10min.csv")

demo_col_names = Demographics10min_df.columns[27:].values.tolist()
demo_col_names.append(Demographics10min_df.columns[2])

Tap_col_names = Tapestry10min_df.columns[26:].values.tolist()
Tap_col_names.append(Tapestry10min_df.columns[2])

Demographics10min_df = Demographics10min_df.loc[:, demo_col_names]
Tapestry10min_df = Tapestry10min_df.loc[:, Tap_col_names]

final_data = final_data.merge(Demographics10min_df,left_on='Total_Visits', right_on='Total_Visits',how='left')
final_data = final_data.merge(Tapestry10min_df,left_on='Total_Visits', right_on='Total_Visits',how='left')
if len(states) == 1:
    final_data.to_csv(states[0]+"_file.csv",index=False)
else:
    final_data.to_csv("3states_final.csv",index=False)





import statsmodels.api as sm
data = competitors_var
data = data[(data.Name == "T.J. Maxx")]
data = data.drop(["State","Lat","Long","client_coords","Rank"], axis=1).reset_index(drop=True)
data = data.fillna(0).drop(["Name"],axis=1)
Y = data.dropna().Total_Visits
X = data.dropna().drop("Total_Visits",axis=1)
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()
print(model.summary())

#ind = final_data.columns.get_loc("2022 Total Population")

