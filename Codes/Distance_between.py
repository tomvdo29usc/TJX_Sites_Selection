#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 22:22:55 2022

@author: tomvdo29
"""
myAPIkey = "AIzaSyAfohcOe1MnbKdYNLgCr_6N2fTPJyTQIYw"
import googlemaps 
import math

gmaps = googlemaps.Client(key=myAPIkey)

# TJM_coor = (36.54900204,-82.49287999)
# Aldi = (36.54353673,-82.5164586)

# result = gmaps.distance_matrix(TJM_coor, Aldi, mode='driving')["rows"][0]["elements"][0]["duration"]["value"]
# result = result/3600

# dis = gmaps.distance_matrix(TJM_coor, Aldi, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]
# dis = dis/1000*0.621371

# print(str(round(dis,2))+ " miles")
# hr = math.floor(result)
# remain_min = (result - hr)*60
# print("{} hour(s) and {} mins".format(hr, round(remain_min)))
import os
import json
os.chdir("/Users/tomvdo29/Desktop/Consulting Project/Data/ALL_DATA")

# import openrouteservice
# """ - setup openrouteservice client with api key, you can signup https://openrouteservice.org 
#       if you don't have API key. Its totaly free😊
#     - After signup, you can see your API key available under the dashboard tab.
# """
# client = openrouteservice.Client(key='5b3ce3597851110001cf624889da1366290543c5a75d5ecec4e4d9d3')
# #set location coordinates in longitude,latitude order

TJM_coor = "28.2241309,-81.6424098"
Aldi = "28.2146974,-81.6879917"
result = gmaps.distance_matrix(TJM_coor, Aldi, mode='driving')["rows"][0]["elements"][0]["duration"]["value"]
result = result/60

print(result)

# coords = (TJM_coor,Aldi)
# #call API
# res = client.directions(coords)
# #test our response
# with(open('test.json','+w')) as f:
#  f.write(json.dumps(res,indent=4, sort_keys=True))
# import requests
# def calc(a,b):
#     url = 'http://router.project-osrm.org/route/v1/driving/'
#     url = url+a+";"+b
#     print(url)

# # call the OSMR API
#     r = requests.get(url)
# # then you load the response using the json libray
# # by default you get only one alternative so you access 0-th element of the `routes`
#     data = json.loads(r.content)
#     if data['code'] == "Ok":
#         return data['routes'][0]['distance']*0.000621371 #in miles
#     else:
#         return "shit"
# print(calc(TJM_coor,Aldi))
# "https://graphhopper.com/api/1/route?key=[YOUR_KEY]" -d '{"elevation":false,"points":[[-0.087891,51.534377],[-0.090637,51.467697]],"vehicle":"car""

# import requests
# from bs4 import BeautifulSoup
# url = 'https://graphhopper.com/maps/?point=34.039513%2C-118.264356&point=33.706056%2C-117.826675&locale=en-US&elevation=true&profile=car&use_miles=false&layer=Omniscale'
# r = requests.get(url)
  
# soup = BeautifulSoup(r.content, 'html.parser')
# print(soup)

