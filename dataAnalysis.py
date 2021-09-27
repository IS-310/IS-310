import numpy as np
import pandas as pd
import sys

'''
Remember to ensure RTData is running for suitable duration so we collect > 5 data sets before we run this script 
else there may be indexing error.
'''
def moving_average(x,w):
    return np.convolve(x, np.ones(w),'valid') / w

def calcDiffNegative(x,y):
    z = x - y
    return z 

def obtainLastValue(array):
    return array[-1]

def calcDiff(x,y):
    z = x - y
    if (z >= 0):
        return z
    else:
        return 0

df = pd.read_csv('history.csv') 
if df.shape[0] < 10:
    sys.exit('Less than 10 values in dataframe. Unable to analyse data yet!')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)


internalFeelsLike = df['feelsLikein']
windSpeed = df['windspeedmph']
windDirection = df['winddir']
dailyRain = df['dailyrainin']

internalFeelsLike = internalFeelsLike.to_numpy()
#print('Type: ',type(internalFeelsLike))
windSpeed = windSpeed.to_numpy()
windDirection = windDirection.to_numpy()

#internalFeelsLike_MA = moving_average(internalFeelsLike,10)
windSpeed_MA = moving_average(windSpeed,10)
windDirection_MA = moving_average(windDirection,10)

latestRainValue = df.loc[df.index[-1],'dailyrainin']
tenMinutesPriorRain = df.loc[df.index[-10],'dailyrainin'] #Remember must have minimally 5 datasets to run else index error
rainDifference = calcDiff(latestRainValue,tenMinutesPriorRain)

latestFeelsLike = df.loc[df.index[-1],'feelsLikein']
tenMinutesPriorFeelsLike = df.loc[df.index[-10],'feelsLikein']
tempDifference = calcDiffNegative(tenMinutesPriorFeelsLike,latestFeelsLike)

print('Your rain difference: ', rainDifference)
print('Feels-like difference: ', tempDifference)
print('windDirection MA: ', obtainLastValue(windDirection_MA) )
print('WindSpeed MA: ',obtainLastValue(windSpeed_MA))





#print('Type: ', type(internalFeelsLike_MA))
#print('Type: ', type(windSpeed_MA))
#print('Type: ', type(windDirection_MA))
#print('Type: ', type(rainDifference))



#myList = [internalFeelsLike_MA,windSpeed_MA,windDirection_MA,rainDifference]
#print('Whole list: ', myList)
#print(type(myList))