# Methods for creating and saving a DB
import pymongo
from pymongo import MongoClient
import pickle
import datetime
import utils
import json 
import pdb

def initializeDb(db_name, collection_name):
	''' Returns dbname and collection '''
	# connect to the hosted MongoDB instance
	client = MongoClient('mongodb://localhost:27017/')
	db = client[db_name]
	collection = db[collection_name]
	return db, collection


def store_profile(collection, profile):
	''' Store a collection into a DB
	INPUT dict'''
	profile_id = profile['id']
	profile['date'] = datetime.datetime.utcnow()
	# I'd rather find a wai to update the date withn
	# the expression below.. but still.
	collection.update(
			{ "id" : profile_id },
				profile ,
				True
			)

def get_profile_data(profile_id):
	''' retrieves the data for a profile_id '''



def main():
	# CUrrently capping the 
	counter = 0
	# Initializes the db
	db, collection = initializeDb("zproject", "math_orig_profiles")
	# Store one profile
	profile_lists  = utils.readpickle('./data/total_unique_profile_math_list.pkl')
	for profile  in profile_lists:
		# print profile['id']
		# Here let's try to store the profile 
		if counter <=330:
			store_profile(collection, profile)
			counter +=1
		else:
			print ("limit reached")
			break
	# print collection.find_one()

	counter = 0
	db, collection = initializeDb("zproject", "new_math_ba_stat_se_ds_full_labels_good")
	# Store one profile
	profile_lists  = utils.readpickle('./data/enhanced_profiles/math_enchanced_total_unique_profiles_9112013.pkl')
	for profile  in profile_lists:
		 # print profile['id']
		# Here let's try to store the profile 
		if counter <=330:
			store_profile(collection, profile)
			counter +=1
		else:
			print ("limit reached")
			break
		
	# print collection.find_one()

	# print db.collection_names()
	
	

if __name__ == "__main__":
	main()