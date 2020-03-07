
import pandas as pd 
import re
import numpy as np 

# Load user data as pandas dataframe
def load_csv(path):
	df = pd.read_csv(path) 
	return df 

# Preprocess user response column in pandas dataframe
def pre_process(df, output_path):
	# Drop duplicate responses
	df = df.drop_duplicates(subset="text_value")
	# Remove white space, quotation marks
	df.text_value = df.text_value.apply(lambda x: re.sub('\s+',' ',x))
	df.text_value = df.text_value.apply(lambda x: x.replace('"', ''))
	# Write to text file
	df.to_csv(output_path, sep='\t', index=False, header=True)


path = 'raw_data/30-03-05-user-responses.csv'
df = load_csv(path)
output_path = 'raw_data/user_responses.txt'
pre_process(df, output_path)