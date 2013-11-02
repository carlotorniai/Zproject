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
		'has_industry','has_specialties', 'has_educations', 'has_skills', 'loc_country',
		'loc_name', 'has_positions', 'has_public_profile', 'has_courses', 'has_dob', 'num_connections')
index = [i for i in range(len(full_list_profiles))]
print index
df_profiles = pd.DataFrame(index=index, columns=columns).fillna(0)
print df_profiles
for i in range(len(full_list_profiles)):
	print full_list_profiles[0]
	if 'firstName' in full_list_profiles[i]:
		df_profiles.ix[i, 'first'] = full_list_profiles[i]['firstName']
	if 'lastName' in full_list_profiles[i]:
		df_profiles.ix[i, 'last'] = full_list_profiles[i]['lastName']
	if 'headline' in full_list_profiles[i]:
		df_profiles.ix[i, 'has_headline'] = 1
	if 'summary' in full_list_profiles[i]:
		df_profiles.ix[i, 'has_summary'] = 1
	if 'location' in full_list_profiles[i]:
		df_profiles.ix[i, 'loc_name'] = full_list_profiles[i]['location']['name']
		df_profiles.ix[i, 'loc_country'] = full_list_profiles[i]['location']['country']['code']
	if 'positions' in full_list_profiles[i]:
		df_profiles.ix[i, 'has_positions'] = full_list_profiles[i]['positions']['_total']
	if 'publicProfileUrl' in full_list_profiles[i]:
		df_profiles.ix[i, 'has_public_profile'] = full_list_profiles[i]['publicProfileUrl']
	if 'numConnections' in full_list_profiles[i]:
		df_profiles.ix[i, 'num_connections'] = full_list_profiles[i]['numConnections']
	if 'educations' in full_list_profiles[i]:
		df_profiles.ix[i, 'has_educations'] = 1
	if 'industry' in full_list_profiles[i]:
		df_profiles.ix[i, 'has_industry'] = full_list_profiles[i]['industry']
	if 'specialties' in full_list_profiles[i]:
		df_profiles.ix[i, 'has_specialties'] = 1
	if 'skills' in full_list_profiles[i]:
		df_profiles.ix[i, 'has_skills'] = 1
	if 'courses' in full_list_profiles[i]:
		df_profiles.ix[i, 'has_courses'] = 1

