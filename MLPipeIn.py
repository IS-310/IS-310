from os import sep
import pickle
import sys
import numpy as np


# load the model from disk
loaded_model = pickle.load(open('finalized_model.sav', 'rb'))

for line in sys.stdin:
    y_present = np.fromstring(line[1:-1],dtype=float,sep=',')

print(y_present)
print(type(y_present))



#predict WDR penetration based on current conditions(y_present)
y_present = y_present.reshape(1, -1)
print(y_present)
print(type(y_present))

pred = loaded_model.predict(y_present)


#implement threshold value
def deploy(predicted_value):
  threshold_value = 1.5
  if (predicted_value > threshold_value):
    print('1')
    return 1
  else:
    print('0')
    return 0

deploy(pred)
