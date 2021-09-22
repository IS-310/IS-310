
import pandas as pd


df = pd.read_csv('history.csv')

num_Rows = df.shape[0]

if num_Rows > 5:     #Number to be edited based on the rolling basis we want
    df = df.iloc[1:]   #Only first row deleted. To be edited as desired
    df.to_csv('history.csv',index=False)
