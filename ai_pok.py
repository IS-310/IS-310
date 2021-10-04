

import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from numpy import nan
import io
import pickle 
import numpy as np; np.random.seed(0)
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error


name = 'RainData - ML - Trial Present and Past data.csv'

RAIN_DATA = pd.read_csv(name)
RAIN_DATA = RAIN_DATA[::-1].reset_index(drop = True)

#df_EUSOFF_WEATHER_DATA
RAIN_DATA.info()  #Checking for missing data
RAIN_DATA.head(10)

"""**Clean data**"""


#mport seaborn as sns; sns.set_theme()
#import matplotlib.pyplot as plt

#a = RAIN_DATA.drop(['Class', 'Wind dir', 'Wind speed std', 'Wind speed average', 'Amount of rain', 'Rain duration'], axis=1)
a = RAIN_DATA
a = a.astype(float)
#print(type(a))

'''
"""**Plot Heat Map**"""
fig, ax = plt.subplots(figsize=(15,15))         # Sample figsize in inches
ax = sns.heatmap(a.corr(), annot=True, fmt='.2f')
print(a.corr())
'''
"""**Split dataset**"""

#our dataset, a is already a numpy array
a = a.to_numpy()
np.random.shuffle(a) 

all_x = a[:,1:4]
all_y = a[:,0].reshape(-1,1)
#print(all_x)

#Create train test 1
x_train_1 = all_x[0:20,:]
y_train_1 = all_y[0:20,:]

x_val_1 = all_x[20:36,:]
y_val_1 =all_y[20:36,:]

#Create train test 3
#x_train_3 = 
#y_train_3 = 

#x_val_3 = 
#y_val_3 =
#print(x_val_1)
#print(y_val_1)

"""**Implement KNN**"""


#from matplotlib import pyplot as plt

#TRYING WITH BEST MODEL
############################################################################

best_model = KNeighborsRegressor(n_neighbors=6)
best_model.fit(all_x, all_y)
KNeighborsRegressor(...)

"""**PICKLE**"""


# save the model to disk
filename = 'KNN_latest_model.sav'
pickle.dump(best_model, open(filename, 'wb'))
