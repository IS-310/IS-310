import numpy as np
import pandas as pd

'''
Remember to ensure RTData is running for suitable duration so we collect > 5 data sets before we run this script 
else there may be indexing error.
'''
def moving_average(x,w):
    return np.convolve(x, np.ones(w),'valid') / w


def calcDiff(x,y):
    z = x - y
    if (z >= 0):
        return z
    else:
        return 0

df = pd.read_csv('history.csv') 

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)


internalFeelsLike = df['feelsLikein']
windSpeed = df['windspeedmph']
windDirection = df['winddir']
dailyRain = df['dailyrainin']

internalFeelsLike = internalFeelsLike.to_numpy()
windSpeed = windSpeed.to_numpy()
windDirection = windDirection.to_numpy()

internalFeelsLike_MA = moving_average(internalFeelsLike,5)
windSpeed_MA = moving_average(windSpeed,2)
windDirection_MA = moving_average(windDirection,2)

latestRainValue = df.loc[df.index[-1],'dailyrainin']
fiveMinutesPriorRain = df.loc[df.index[-5],'dailyrainin'] #Remember must have minimally 5 datasets to run else index error
rainDifference = calcDiff(latestRainValue,fiveMinutesPriorRain)

print('Internal temp MA: ', internalFeelsLike_MA)
print('WindSpeed MA: ',windSpeed_MA)
print('windDirection MA: ', windDirection_MA)
print('Your rain difference: ', rainDifference)

myList = [internalFeelsLike_MA,windSpeed_MA,windDirection_MA,rainDifference]
print(myList)