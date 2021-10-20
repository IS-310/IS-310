from os import sep
import pickle
import sys
import numpy as np
from warnings import simplefilter
from datetime import datetime 
import pickle as serializer
import shelve



import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

simplefilter(action='ignore', category=DeprecationWarning)

# load the model from disk
loaded_model = pickle.load(open('KNN_Updated_17OCT.sav', 'rb'))
sh = shelve.open('globals')

def deploy(predicted_value, corridor_width):
  threshold_value = corridor_width/2
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

for line in sys.stdin:

    if line.rstrip() == '[-1,-1,-1,-1]':
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
        
        cmd = deploy(pred,1.91)
        file = open('logResults.txt','a')
        file.write(current_time + ' Input array: ' + line + ' Predicted depth: ' + str(pred) + '\n')
        file.close()

sh.close()



ser.write(b'%d'%cmd)
print(cmd, 'completed')
ser.flush()

