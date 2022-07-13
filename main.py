import os
import csv 
import sys
from datetime import datetime
from meteostat import Point, Daily, Stations
import pandas as pd
import requests


def getGeoCoord(address):
    params = {
        'key': API_KEY,
        'address': address.replace(' ', '+')
    }

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        result = data['results'][0]
        location = result['geometry']['location']
        return location['lat'], location['lng']
    
    else:
        return None,None

def weatherFinder(lati, longi, accur,in_year, in_month, in_day):  #using meteostat to get the average temp on the day
    
    # Set time period
    start = datetime(in_year, in_month, in_day)
    end = datetime(in_year, in_month, in_day)
    
    # Create Point for England, Location(Postcode)
    england = Point(float(lati), float(longi) , int(accur))

    # Get data for date
    data = Daily(england, start, end)
    data = data.fetch()
    if len(data) == 0:
        stations = Stations()
        stations = stations.nearby(lati, longi)
        station = stations.fetch(2)
        if len(station) > 0:
            return weatherFinder(station.iat[1,5],station.iat[1,6],station.iat[1,7],in_year, in_month, in_day )

        else:
            return None
    return data.iat[0,0]

    
#FORMAT POSTCODE
def postCodeFormat(address):
    if len(address) == 6:
        new_address = address[0:3] +' '+address[3:6]
    if len(address) == 7:
        new_address = address[0:4] +' '+address[4:]
    if len(address) == 5:
        new_address = address[0:2] +' '+address[2:5]
    return new_address


#get date in the format (year), (month)  & (day)
def convertDateFormat(i,df):
    
    date_used = df.iat[i,1]
    in_day = int(date_used[0:2])
    in_month = int(date_used[3:5])
    in_year = int(date_used[6:10])
    return in_year, in_month, in_day



#If Statements to select which temperature is required for which ice pack
def compareData(average_temp, p_code, df_3):
    if type(average_temp) != str:

        if ((df_3.iat[0,0]) <=  float(average_temp)) and (float(average_temp) <= (df_3.iat[0,1])):
            return [df_3.iat[0,2], df_3.iat[0,3], df_3.iat[0,4]]

        if (df_3.iat[1,0]) <=  float(average_temp) and float(average_temp) <= (df_3.iat[1,1]):
            return [df_3.iat[1,2], df_3.iat[1,3], df_3.iat[1,4]]
        
        if ((df_3.iat[2,0]) <=  float(average_temp)) and (float(average_temp) <= (df_3.iat[2,1])):
            return [df_3.iat[2,2], df_3.iat[2,3], df_3.iat[2,4]]

        if (df_3.iat[3,0]) <=  float(average_temp) and float(average_temp) <= (df_3.iat[3,1]):
            return [df_3.iat[3,2], df_3.iat[3,3], df_3.iat[3,4]]
        
        if ((df_3.iat[4,0]) <=  float(average_temp)) and (float(average_temp) <= (df_3.iat[4,1])):
            return [df_3.iat[4,2], df_3.iat[4,3], df_3.iat[4,4]]

        if (df_3.iat[5,0]) <=  float(average_temp) and float(average_temp) <= (df_3.iat[5,1]):
            return [df_3.iat[5,2], df_3.iat[5,3], df_3.iat[5,4]]

        if ((df_3.iat[6,0]) <=  float(average_temp)) and (float(average_temp) <= (df_3.iat[6,1])):
            return [df_3.iat[6,2], df_3.iat[6,3], df_3.iat[6,4]]
        else:
            return None
    else:
        return ['NaT','NaT','NaT']


API_KEY = 'AIzaSyAoa8Sc-qHIjprPR0Fy_ixUTWyVvhk8iA4'

df = pd.read_csv(str(sys.argv[1])) #convert main input csv to df

newDataArray = []
df_3 = pd.read_csv(str(sys.argv[2])) #convert secondary input csv to df



pd.options.display.max_rows = 9999
for i in range(int(len(df))):
    in_year, in_month, in_day = convertDateFormat(i,df)
    p_code = postCodeFormat(df.iat[i,4])
    lati, longi = getGeoCoord(p_code)
    if lati == None:
        
        average_temp = "Location Not Found in Meteostat"
        
    else:
        average_temp = weatherFinder(lati, longi, 70,in_year, in_month, in_day) #get the average temp on the day
    
    
    
    newDataArray.append(compareData(average_temp, p_code, df_3)) #use array to create df and join with original as a new df and convert to csv

df_2 = pd.DataFrame(newDataArray, columns =['S',	'M',	'L'])
df_final = (df.join(df_2))
df_final.to_csv(str(sys.argv[3]), index=False)  