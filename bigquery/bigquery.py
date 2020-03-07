# Query data from BigQuery in python

import pandas as pd
from google.cloud import bigquery
from google.cloud import bigquery_storage_v1beta1
from google.cloud import storage
import google.auth
import os
import numpy as np

class BigQuery():

	# Initialize BigQuery client
	def __init__(self):
		# Make sure path is set to right credentials on your computer
		path = "/Users/soniajoseph/Downloads/inwords-2ac82-acf34abc95cb.json"
		os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=path
		# Check variable is set
		print('Credentials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))


		# Explicitly create a credentials object. This allows you to use the same
		# credentials for both the BigQuery and BigQuery Storage clients, avoiding
#		 unnecessary API calls to fetch duplicate authentication tokens.
		credentials, your_project_id = google.auth.default(
		    scopes=["https://www.googleapis.com/auth/cloud-platform"]
		)

		# Make clients.
		self.bqclient = bigquery.Client(
		    credentials=credentials,
		    project='inwords-2ac82',
		)
		self.bqstorageclient = bigquery_storage_v1beta1.BigQueryStorageClient(
		    credentials=credentials
		)


	# Get user birth year, city, continent, capital, gender
	# Note: append number of conversations from training data
	def user_data(self, users, embeddings):

		t = tuple(users)
		print("tuple length", len(t))

		query_string = """
		SELECT uid, birth_year, latest_location_obj.city, latest_location_obj.continent_name, latest_location_obj.location.capital, gender, action_counter
		FROM `inwords-2ac82.firestore_data.MUsers`
		WHERE uid IN {}
		""".format(t)


		df = (
	    self.bqclient.query(query_string)
	    .result()
	    .to_dataframe(bqstorage_client=self.bqstorageclient)
		)

		# Add embedding column to dataframe 
		print(len(df.index))
		print(len(embeddings))
		df["emb"] = embeddings

		return df

	# Takes uid and embeddings .txr file and splits uid and embeddings
	# Returns uids as array of strings and embeddings as array of floats
	def split_embedding(self, file):

		uids = []
		embeddings = []

		with open(file, 'r') as f:
			# Skip first two lines [header and irrelevant vector for 'uid']
			for _ in range(2):
				next(f)
			for line in f:
				line = line.split()
				user = line[0]
				vector = np.array(line[1:]).astype(np.float)
				uids.append(user)
				embeddings.append(vector)

		return uids, embeddings

	# Save df object with str name as pkl file
	def save_df(self, df, name):
		df.to_pickle('../processed_data/' + name + '.pkl')



# Test by creating a user data table from BigQuery,
# Turning it into a dataframe, then saving as pkl in 'preprocessed_data' folder

bq = BigQuery()
uids, embeddings = bq.split_embedding('../DATA/pkl/user_responses.txt')
df = bq.user_data(uids, embeddings)
bq.save_df(df, 'user_data')

print(df.keys())
print(df.head())
