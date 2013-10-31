import json
import pickle
import pandas as pd


def readpickle(filename):
	''' reads a pickle file and return its content'''
	infile = open(filename, "rb")
	content = pickle.load(infile)
	infile.close()
	return content


filename = "./data/10_30/full/me_full_profile_list.pkl"

full_list_profiles = readpickle(filename)

# Build a pandas dataframe with 0
columns = ('first', 'last', 'user_id', 'has_headline', 'has_summary', \
		'has_industry','has_specialties', 'has_educations', 'has_skills', \
		'has_positions', 'has_public_profile', 'has_courses', 'has_dob')
index = [i for i in range(len(full_list_profiles))]
print index
df_profiles = pd.DataFrame(index=index, columns=columns).fillna(0)
print df_profiles
#for i in range(len(full_list_profiles)):
for i in range(1):
	print full_list_profiles[i]
	# I have to check if the key exists first
	df_profiles.ix[i, 'first'] = full_list_profiles[i]['firstName']
	



