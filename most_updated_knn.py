# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from numpy import nan
from sklearn.neighbors import KNeighborsRegressor
import pickle 
import numpy as np; np.random.seed(0)

name = 'RainData - FINAL (5).csv'

RAIN_DATA = pd.read_csv(name)
RAIN_DATA = RAIN_DATA[::-1].reset_index(drop = True)


#import seaborn as sns; sns.set_theme()
#import matplotlib.pyplot as plt

#a = RAIN_DATA.drop(['a', 'b','c'], axis=1)
a = RAIN_DATA
a = a.astype(float)
print(type(a))

#our dataset, a is already a numpy array
a = a.to_numpy()
np.random.shuffle(a) 

all_x = a[:,2:]
all_y = a[:,0].reshape(-1,1)
print(all_x)

#Create train test 1
x_train_1 = all_x[0:85,:]
y_train_1 = all_y[0:85,:]

x_val_1 = all_x[85:,:]
y_val_1 =all_y[85:,:]

best_model_KNN = KNeighborsRegressor(n_neighbors=2) 
best_model_KNN.fit(x_train_1, y_train_1) 
KNeighborsRegressor(...)


# save the model to disk
filename = 'KNN_Updated_17OCT.sav'
pickle.dump(best_model_KNN, open(filename, 'wb'))





