import numpy as np
import pandas as pd
import sys

'''
Remember to ensure RTData is running for suitable duration so we collect > 5 data sets before we run this script 
else there may be indexing error.
'''
#def moving_average(x,w):
 #   return np.convolve(x, np.ones(w),'valid') / w

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

def calcEastVelocity(windSpeed, direction):
    directionRadian = np.deg2rad(direction)
    #print(directionRadian)
    #print(windSpeed * np.sin(directionRadian))
    return windSpeed * np.sin(directionRadian)

def calcNorthVelocity(windSpeed, direction):
    directionRadian = np.deg2rad(direction)
    #print(directionRadian)
    #print(windSpeed * np.cos(directionRadian))
    return windSpeed * np.cos(directionRadian)

def summation(df, windowSize):
    summationEast = 0
    summationNorth = 0
    windowSize = -windowSize
    for rowNum in range(windowSize,0):
        windSpeed = df.loc[df.index[rowNum],'windspeedmph']
        windDirection = df.loc[df.index[rowNum],'winddir']
        summationEast += calcEastVelocity(windSpeed,windDirection)
        summationNorth += calcNorthVelocity(windSpeed,windDirection)
    return summationEast, summationNorth

def calcAverageWindVelocity(windowSize, summationEast, summationNorth):
    summationEastAverage = summationEast / windowSize
    summationNorthAverage = summationNorth / windowSize
    averageWindVelocity = np.sqrt(np.square(summationEastAverage) + np.square(summationNorthAverage))
    return averageWindVelocity
    
def calcAverageWindDirection(windowSize, summationEast, summationNorth):
    summationEastAverage = summationEast / windowSize
    summationNorthAverage = summationNorth / windowSize
    if (summationEastAverage == 0 and summationNorthAverage == 0):
        return -2
    elif (summationEastAverage == 0 and summationNorthAverage > 0):
        return np.pi
    elif (summationEastAverage == 0 and summationNorthAverage < 0):
        return 0
    elif (summationEastAverage < 0 and summationNorthAverage == 0):
        return (np.pi)/2
    elif (summationEastAverage > 0 and summationNorthAverage == 0):
        return (3/4)*2*np.pi
    elif (summationEastAverage > 0 and summationNorthAverage > 0):
        windDirRad = np.arctan(summationEastAverage/summationNorthAverage)
        return windDirRad
    elif (summationEastAverage < 0 and summationNorthAverage < 0):
        windDirRad = np.arctan(summationEastAverage/summationNorthAverage) + np.pi
        return windDirRad
    elif (summationEastAverage > 0 and summationNorthAverage < 0):
        windDirRad = np.arctan(summationEastAverage/summationNorthAverage) + np.pi
        return windDirRad
    elif(summationEastAverage < 0 and summationNorthAverage > 0):
        windDirRad = np.arctan(summationEastAverage/summationNorthAverage) + 2*np.pi
        return windDirRad


def retract(df):
    rainSum = df['hourlyrainin'].tail(10).sum()
    if (rainSum == 0):
        return 1
    else:
        return 0

df = pd.read_csv('history.csv') 
if df.shape[0] < 10:
    sys.exit('Less than 10 values in dataframe. Unable to analyse data yet!')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)


internalFeelsLike = df['feelsLikein']
#windSpeed = df['windspeedmph']
windDirection = df['winddir']
dailyRain = df['dailyrainin']

internalFeelsLike = internalFeelsLike.to_numpy()
#print('Type: ',type(internalFeelsLike))
#windSpeed = windSpeed.to_numpy()
windDirection = windDirection.to_numpy()

#internalFeelsLike_MA = moving_average(internalFeelsLike,10)
tuple_EastNorthVelocitySummation = summation(df,10)
#print(tuple_EastNorthVelocitySummation)
windSpeedAverage = calcAverageWindVelocity(10,*tuple_EastNorthVelocitySummation)
windSpeedMax = df['windspeedmph'].tail(10).max()
windDirectionAverage = calcAverageWindDirection(10,*tuple_EastNorthVelocitySummation)


latestRainValue = df.loc[df.index[-1],'dailyrainin']
tenMinutesPriorRain = df.loc[df.index[-10],'dailyrainin'] #Remember must have minimally 5 datasets to run else index error
rainDifference = calcDiff(latestRainValue,tenMinutesPriorRain)

latestFeelsLike = df.loc[df.index[-1],'feelsLikein']
tenMinutesPriorFeelsLike = df.loc[df.index[-10],'feelsLikein']
tempDifference = calcDiffNegative(tenMinutesPriorFeelsLike,latestFeelsLike)
#print(rainDifference)
#print('Your rain difference: ', rainDifference)
#print('Feels-like difference: ', tempDifference)
#print('windDirection MA: ', obtainLastValue(windDirection_MA) )
#print('WindSpeed MA: ',type(obtainLastValue(windSpeed_MA)))


toRetract = retract(df)
myArr = [windDirectionAverage,windSpeedMax*rainDifference, windSpeedAverage*rainDifference] #removed 'tempdifference' and 'obtainLastValue(windDirection_MA)'
#print(type(myArr))
#print(myArr)

if toRetract:
    print('[-1,-1,-1]')
    
else:
    print(myArr)



#print('Type: ', type(internalFeelsLike_MA))
#print('Type: ', type(windSpeed_MA))
#print('Type: ', type(windDirection_MA))
#print('Type: ', type(rainDifference))



#myList = [internalFeelsLike_MA,windSpeed_MA,windDirection_MA,rainDifference]
#print('Whole list: ', myList)
#print(type(myList))