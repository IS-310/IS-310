from ambient_api.ambientapi import AmbientAPI
import time
import pandas as pd
from pandas.core.algorithms import mode
import os
from datetime import datetime, timedelta

api = AmbientAPI(AMBIENT_API_KEY='a5113b72cb2149fa9ee6028865f6cebddfc1910cd6c94c3b99cb8eca8b4bb98c', AMBIENT_APPLICATION_KEY='a9f9a40d42a0494282936cd34bc7335e0a6a7a962c0a4a52aac650fd6752bdbb', AMBIENT_ENDPOINT='https://api.ambientweather.net/v1')

devices = api.get_devices()
#print(devices)

deviceIndoor = devices[0]
deviceOutdoor = devices[1]

time.sleep(1) #pause for a second to avoid API limits
#print('Device0: ', str(device))
myDictIndoor = deviceIndoor.last_data
myDictOutdoor = deviceOutdoor.last_data
#print([myDict])

def fahrenToCelsius(x):
        x = (x - 32) / 1.8
        return float(x) #No rounding off in intermediary steps

def mphToMps(x):
    x = x * 0.44704
    return float(x)        #No rounding off in intermediary steps

def inchToMm(x):
    x = x * 25.4
    return float(x)        #No rounding off in intermediary steps

def windDirConversion(x):
    if x >= 80:
        return (80 - x)
    else:
        return 360 - (80 - x)  #Formula is 360 - abs(x - 80)

df = pd.DataFrame([myDictIndoor])
dfOutdoor = pd.DataFrame([myDictOutdoor])

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)
df = df.astype({'windspeedmph':'float','windgustmph':'float','maxdailygust':'float'}) #Converting wind data to float just in case


#print('original wind spde: ', df['windspeedmph'])
#print('original wind spde1111: ', df['windgustmph'])
#print(type(df['tempf']))
df['tempf'] = df['tempf'].apply(fahrenToCelsius)
df['tempinf'] = df['tempinf'].apply(fahrenToCelsius)
df['feelsLike'] = df['feelsLike'].apply(fahrenToCelsius)
df['dewPoint'] = df['dewPoint'].apply(fahrenToCelsius)
df['feelsLikein'] = df['feelsLikein'].apply(fahrenToCelsius)
df['dewPointin'] = df['dewPointin'].apply(fahrenToCelsius)

df['windspeedmph'] = df['windspeedmph'].apply(mphToMps)
df['windgustmph'] = df['windgustmph'].apply(mphToMps)
df['maxdailygust'] = df['maxdailygust'].apply(mphToMps)
df['winddir'] = df['winddir'].apply(windDirConversion)


df['baromrelin'] = df['baromrelin'].apply(inchToMm)
df['baromabsin'] = df['baromabsin'].apply(inchToMm)
dfOutdoor['eventrainin'] = dfOutdoor['eventrainin'].apply(inchToMm)
dfOutdoor['weeklyrainin'] = dfOutdoor['weeklyrainin'].apply(inchToMm)
dfOutdoor['monthlyrainin'] = dfOutdoor['monthlyrainin'].apply(inchToMm)
dfOutdoor['totalrainin'] = dfOutdoor['totalrainin'].apply(inchToMm)
dfOutdoor['dailyrainin'] = dfOutdoor['dailyrainin'].apply(inchToMm)

df['eventrainin'] = dfOutdoor['eventrainin']
df['weeklyrainin'] = dfOutdoor['weeklyrainin']
df['monthlyrainin'] = dfOutdoor['monthlyrainin']
df['totalrainin'] = dfOutdoor['totalrainin']
df['dailyrainin'] = dfOutdoor['dailyrainin']
df['lastRain'] = dfOutdoor['lastRain']

#print(type(df['date']))
#print(df['date'])
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%dT%H:%M:%S.%fZ')
df['date'] = df['date'] + pd.Timedelta(hours=8)

df['lastRain'] = pd.to_datetime(df['lastRain'], format='%Y-%m-%dT%H:%M:%S.%fZ')
df['lastRain'] = df['lastRain'] + pd.Timedelta(hours=8)
#print(type(df['date']))
#print(df['date'])
#print('original wind spde: ', df['windspeedmph'])

if os.path.isfile('history.csv'):
    df.to_csv('history.csv', mode='a',header=False,index=False)

else:
    df.to_csv('history.csv',index=False)




