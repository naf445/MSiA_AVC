import pandas as pd
import csv

names = pd.read_csv('names.txt', sep='\t', header=None)
names = names.iloc[:,1]
names.to_csv('names.csv', index=False)