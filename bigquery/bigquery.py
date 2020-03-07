# Query data from BigQuery in python

import pandas as pd
from google.cloud import bigquery
from google.cloud import bigquery_storage_v1beta1
from google.cloud import storage
import google.auth
import os

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
	def user_data(self, users):

		query_string = """
		SELECT birth_year, latest_location_obj.city, latest_location_obj.continent_name, latest_location_obj.location.capital, gender, action_counter
		FROM `inwords-2ac82.firestore_data.MUsers`
		WHERE uid = '00Ea0e5amtX8E2cJY0RvP9jGTuv2'
		"""

		dataframe = (
	    self.bqclient.query(query_string)
	    .result()
	    .to_dataframe(bqstorage_client=self.bqstorageclient)
		)
		print(df.head())

		return df


# Test

bq = BigQuery()
bq.user_data("test")

