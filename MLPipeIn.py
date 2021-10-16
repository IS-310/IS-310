from os import sep
import pickle
import sys
import numpy as np
from warnings import simplefilter
from datetime import datetime 
from pandas.core.base import IndexOpsMixin
'''
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
'''
simplefilter(action='ignore', category=DeprecationWarning)

# load the model from disk
loaded_model = pickle.load(open('KNN_latest_model.sav', 'rb'))

def deploy(predicted_value, corridor_width):
  threshold_value = corridor_width/2
  if (predicted_value > threshold_value):
    print('1')
    return 1
  else:
    print('0')
    return 0

now = datetime.now()
current_time = now.strftime('%H:%M:%S')
print(f'The current time is {current_time}')

for line in sys.stdin:

    if line.rstrip() == '[-1,-1,-1,-1]':
        print('Retract flag detected')
        cmd = 2

    else:
        y_present = np.fromstring(line[1:-1],dtype=float,sep=',')
        y_present = y_present.reshape(1, -1)
        pred = loaded_model.predict(y_present)
        print('Predicted value is:', pred)
        cmd = deploy(pred)

'''
ser.write(b'%d'%cmd)
print(cmd, 'completed')
ser.flush()
'''
#line = ser.readline().decode('utf-8')
#line = ser.readline().decode('utf-8')
#parsed = [x.rstrip() for x in line]
#print(line)
