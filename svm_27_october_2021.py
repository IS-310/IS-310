# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from numpy import nan
from sklearn import svm
import numpy as np; np.random.seed(0)
import pickle 

name = 'RainData_FINAL_DATASET.csv'

RAIN_DATA = pd.read_csv(name)
RAIN_DATA = RAIN_DATA[::-1].reset_index(drop = True)




#a = RAIN_DATA.drop(['a', 'b','c'], axis=1)
a = RAIN_DATA
a = a.astype(float)
print(type(a))

#our dataset, a is already a numpy array
a = a.to_numpy()
np.random.shuffle(a) 

all_x = a[:,2:6]
all_y = a[:,0].reshape(-1,1)
print(all_x)

x_train_1 = all_x[0:47,:]
y_train_1 = all_y[0:47,:]

x_val_1 = all_x[47:,:]
y_val_1 =all_y[47:,:]

print(x_val_1)
print(y_val_1)


regr = svm.SVR()
regr.fit(x_train_1, y_train_1)
pred_SVM = regr.predict(x_val_1)


# save the model to disk
filename = 'SVM_27_October_2021'
pickle.dump(regr, open(filename, 'wb'))


