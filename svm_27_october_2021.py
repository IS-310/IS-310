# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from numpy import nan
import io

name = 'RainData_FINAL_DATASET.csv'

RAIN_DATA = pd.read_csv(name)
RAIN_DATA = RAIN_DATA[::-1].reset_index(drop = True)


import numpy as np; np.random.seed(0)
#a = RAIN_DATA.drop(['a', 'b','c'], axis=1)
a = RAIN_DATA
a = a.astype(float)
print(type(a))

#our dataset, a is already a numpy array
a = a.to_numpy()
np.random.shuffle(a) 

all_x = a[:,3:7]
all_y = a[:,1].reshape(-1,1)
print(all_x)

x_train_1 = all_x[0:90,:]
y_train_1 = all_y[0:90,:]

x_val_1 = all_x[90:,:]
y_val_1 =all_y[90:,:]

print(x_val_1)
print(y_val_1)

from sklearn import svm
regr = svm.SVR()
regr.fit(x_train_1, y_train_1)
pred_SVM = regr.predict(x_val_1)

import pickle 
# save the model to disk
filename = 'SVM_27_October_2021'
pickle.dump(regr, open(filename, 'wb'))


