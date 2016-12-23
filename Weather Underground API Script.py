# Import necessary libraries     
import urllib2
import pandas as pd
import time
import numpy as np
import csv
from natsort import natsorted as ns

# Input Parameters:
# Put list of cities you want to query in locs
# Enter the number of days you would like to forecast for each city

# Insert unique key below
url_base = "http://api.wunderground.com/api/*INSERT YOUR UNIQUE KEY*/forecast10day/conditions/q/{}"

# List of locations
locs = ['GH/Accra.json','DE/Burghausen.json','AR/Buenos-Aires.json','IN/Chennai.json','PE/Lima.json']
num = len(locs)

# Input number of days to forecast
forecast_days = input('Enter the number of days you would like to forecast: ')

raw_data_list = []
count = 0

# Read and store JSON for each city in a dataframe 
for city in locs:
    if count == 10:
        time.sleep(60)
    url = url_base.format(city)
    try:
        raw_data = urllib2.urlopen(url).read()
        if raw_data != "":
            raw_data_list.append(raw_data)
    except:
        pass
    count += 1

data = "[" + (",".join(raw_data_list)) + "]" 
data = pd.read_json(data, orient='values')

# Extract full location
for record in data:
    city = data['current_observation']
    location = [rec['display_location']['full'] for rec in city]

location = pd.DataFrame(data=location) # Store the locations in a separate dataframe
location.columns = ['Location'] # Change the column name from gibberish to Location

# Create empty dicts for min and max temps
low = dict()
high = dict()

# Extract min and max temps for each city for each day
for item in data:
    for i in range(0,forecast_days):
        weather = data['forecast']
        forecast = [rec['simpleforecast']['forecastday'] for rec in weather]
        low[i] = [rec[i]['low']['celsius'] for rec in forecast]
        high[i] = [rec[i]['high']['celsius'] for rec in forecast]

# Store raw temp values in arrays. Transpose so each column represents a temp value for a particular day for each city
low_values = [v for v in low.values()]
high_values = [v for v in high.values()]
low2 = np.array(low_values)
low2 = low2.transpose()
high2 = np.array(high_values)
high2 = high2.transpose()

# Create keys for min and max variables
l = dict()
h = dict()
for x in range(1, forecast_days+1):
    l['min%d' % x] = []
    h['max%d' % x] = []

# Extract key values and sort
keys1 = list(l.keys())
keys1.sort()
keys2 = list(h.keys())
keys2.sort()

# Store min and max values in dataframes
min_values = pd.DataFrame(data=low2)
max_values = pd.DataFrame(data=high2)

# Sort keys via natsort
a = min_values.columns = keys1
c = max_values.columns = keys2
a = ns(a)
c = ns(c)

# Zip keys and flatten
d = zip(a,c)
d = np.array(d)
d.ravel()

# Create an array of min and max values 
t = dict()
for i in range(0,forecast_days):
    t[i] = [min_values.iloc[:,i],max_values.iloc[:,i]]
    
t = [v for v in t.values()]
t = np.array(t,dtype=np.int32)
t = t.transpose()

# Create 3 empty dictionaries
q = dict()
w = dict()
temp = dict()
for i in range(1,forecast_days+1):
    q[i] = []
    w[i] = []

# Store min and max values for each city for each day in a dataframe with the keys as the column names
for i in range(0,num):
    q[i] = t[i][0]
    w[i] = t[i][1]
    temp[i] = zip(q[i],w[i])
q = [v for v in q.values()]
w = [v for v in w.values()]
temp = [v for v in temp.values()]
temp = np.array(temp,dtype=np.int32)
temp = temp.ravel()
temp = temp.reshape((num,forecast_days*2))
temp = pd.DataFrame(data=temp)
temp.columns = d

# Concatenate the location and temp dataframes together and write to a csv file called temp.csv. 
table = pd.concat([location,temp],axis=1)
table.to_csv('temp.csv',index=False)

