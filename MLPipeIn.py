import os
import pickle
import sys
import numpy as np
from warnings import simplefilter
from datetime import datetime 
import pickle as serializer
import shelve
import csv 

'''
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
'''
simplefilter(action='ignore', category=DeprecationWarning)

# load the model from disk
loaded_model = pickle.load(open('SVM_27_October_2021', 'rb'))
sh = shelve.open('globals')

def deploy(predicted_value, threshold_value):

  if (predicted_value > threshold_value):
    print('1. Deploy command assigned.')
    
    if(sh['blindStatus'] == 1):
      print('Blind is already deployed')
      return 0
    else:
      print('Blind is deploying now!')
      sh['blindStatus'] = 1
      return 1
    
  else:
    print('0. Threshold not met. Standby command assigned.')
    return 0

now = datetime.now()
current_time = now.strftime('%d-%m-%y %H:%M:%S')
print(f'The current date/time is {current_time}')

def arrayExtractor(myLine):
    stripped = myLine[1:-1].strip()
    parsedLine = stripped.split(",") 
    return parsedLine

for line in sys.stdin:

    if line.rstrip() == '[-1,-1,-1]':
        print('2. Retract command assigned.')
        
        if(sh['blindStatus'] == 0):
          print('Blind is already retracted')
        else:
          print('Retracting blind now')
          sh['blindStatus'] = 0
          
        cmd = 2

    else:
        y_present = np.fromstring(line[1:-1],dtype=float,sep=',')
        y_present = y_present.reshape(1, -1)
        pred = 10**loaded_model.predict(y_present)
        print('Predicted value is:', pred)
        #print(arrayExtractor(line))
        
        cmd = deploy(pred,0.2)
        if os.path.isfile('logResults.csv'):
            arrayData = arrayExtractor(line)
            rain = arrayData[0]
            maxWind = arrayData[1]
            averageWind = arrayData[2]
            windDir = arrayData[3]
            parsedPred = str(pred)[1:-1]
            loggedResults = [current_time,rain,maxWind,averageWind,windDir,parsedPred]
            f = open('logResults.csv','a')
            csv_writer = csv.writer(f)
            csv_writer.writerow(loggedResults)
            f.close()

        else:
            arrayData = arrayExtractor(line)
            rain = arrayData[0]
            avgWindDir = arrayData[1]
            windMaxRainChange = arrayData[2]
            windAvgRainChange = arrayData[3]
            parsedPred = str(pred)[2:-2]
            header = ['Date/Time', 'Changes in Rain','Avg Wind Dir','WindMax * RainChange','WindAvg * RainChange', 'Predicted Depth']
            loggedResults = [current_time,rain,avgWindDir,windMaxRainChange,windAvgRainChange,parsedPred]
            
            f = open('logResults.csv','w')
            csv_writer = csv.writer(f)
            csv_writer.writerow(header)
            csv_writer.writerow(loggedResults)
            f.close()

        '''
        file = open('logResults.txt','a')
        file.write(current_time + ' Input array: ' + line + ' Predicted depth: ' + str(pred) + '\n\n')
        file.close()
        '''

sh.close()


'''
ser.write(b'%d'%cmd)
print(cmd, 'completed')
ser.flush()
'''
