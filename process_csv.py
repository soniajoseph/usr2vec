
import pandas as pd 
import numpy as np 

# Load user data
path = 'raw_data/30-03-05-user-responses.csv'
df = pd.read_csv(path)

print(df.head())
print(len(df.index))

df = df.drop_duplicates(subset="text_value")
print(len(df.index))

# Write to text file
df.to_csv('raw_data/user_responses.txt', sep='\t', index=False, header=False)