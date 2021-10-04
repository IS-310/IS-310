import pandas as pd

df = pd.read_csv('history.csv')
df = df.round(3)

df.index = range(len(df))

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)

df.to_csv('reindexedHistory.csv')