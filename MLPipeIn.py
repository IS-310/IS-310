from os import sep
import pickle
import sys
import numpy as np
from warnings import simplefilter

from pandas.core.base import IndexOpsMixin
#import serial

simplefilter(action='ignore', category=DeprecationWarning)


# load the model from disk
loaded_model = pickle.load(open('KNN_latest_model.sav', 'rb'))

def deploy(predicted_value):
  threshold_value = 1.5
  if (predicted_value > threshold_value):
    print('1')
    return 1
  else:
    print('0')
    return 0

for line in sys.stdin:

    if line.rstrip() == '[-1,-1,-1,-1]':
        print('Retracting')
        cmd = 2

    else:
        y_present = np.fromstring(line[1:-1],dtype=float,sep=',')
        y_present = y_present.reshape(1, -1)
        pred = loaded_model.predict(y_present)
        print('Predicted value is:',pred)
        cmd = deploy(pred)
  

#print(y_present)
#print(type(y_present))


#predict WDR penetration based on current conditions(y_present)

#print(y_present)
#print(type(y_present))

print(cmd)

#implement threshold value
'''

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.write(b'%d'%cmd)
print(cmd, 'completed')
'''