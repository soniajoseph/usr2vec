
import pandas as pd 
import re
import numpy as np 

# Load user data
path = 'raw_data/30-03-05-user-responses.csv'
df = pd.read_csv(path)

print(df.head())
print(len(df.index))

df = df.drop_duplicates(subset="text_value")
print(len(df.index))

# Remove white space, quotation marks
# More preprocessing? 
df.text_value = df.text_value.apply(lambda x: re.sub('\s+',' ',x))
df.text_value = df.text_value.apply(lambda x: x.replace('"', ''))

# Write to text file
df.to_csv('raw_data/user_responses.txt', sep='\t', index=False, header=True)


