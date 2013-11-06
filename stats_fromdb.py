import json
import pandas as pd
import utils
import pymongo
import pdb


def build_education_df(db, collection):
	''' Builds a matrix with the educaiton and the data scientist 
	position info for a given collection of profiles'''

	columns = ('first_name', 'last_name', 'user_id', 'bachelor_1', 'bachelor_2', \
			'master_1','master_2', 'phd_1', 'phd_2', 'current_ds_job',
			'past_ds_job', 'ds_in_header', 'ds_in_summary')
	index = [i for i in range(collection.count())]
	df_profiles = pd.DataFrame(index=index, columns=columns).fillna(0) 
	index = 0
	cursor = collection.find({}, {"_id":0, "id":1, "firstName":1, "lastName":1, \
		"bc_1" : 1 , "bc_2":1, "mas_1": 1, "mas_2":1 , "phd_1":1, "phd_2":1, \
		"ds_job_current":1, "ds_job_past":1, "ds_in_head":1, "ds_in_summary":1 })
	df = pd.DataFrame(list(cursor))
	return df

def get_education_features(db, collection):
	''' Builds a dataframe with educaiton information'''
	educations_list=[]
	index=[]
	columns = ( 'bc_1', 'bc_2', 'mas_1','mas_2', 'phd_1', 'phd_2')
	cursor = collection.find({}, {"_id":0, "id":1, "bc_1" : 1 , "bc_2":1, "mas_1": 1, \
		"mas_2":1 , "phd_1":1, "phd_2":1, })
	for results in cursor:
		index.append(results['id'])

	df_education = pd.DataFrame(index=index, columns=columns).fillna(0)
	# Here put the values in
	cursor_profile = collection.find({})
	for profile in cursor_profile:
		user_id = profile['id']
		# I knwo that every record has its columns
		for field in columns:
			if field in profile:
				if profile[field] == 1:
					df_education.ix[user_id, field] = "other_"+field
				elif  profile[field] == -1:
					df_education.ix[user_id, field] = "no_"+field	
				else:
					df_education.ix[user_id, field] = field+"_"+str(profile[field])
			else:
				df_education.ix[user_id, field] = "no_"+field
	return df_education

def build_skills_ds(db, collection):
	''' Builds a matrix with all the skills per profile'''
	print "Building skills Df"

	# The method below fails when it
	# comes to name the columns if it's nicer
	# skills_list= collection.distinct('skills')
	# columns = []
	# for i in range(len(skills_list)):
	# 	print skills_list[i]
	# 	columns.append(skills_list[i])
	# pdb.set_trace()
	
	skill_set = set()
	skill_full_list = []
	index= []
	# Build columns and index to create the dataframe
	cursor  = collection.find({}, {"_id":0, "skills":1, "id":1})
	for results in cursor:
		# pdb.set_trace()
		if "skills" in results:
			for skill in (results['skills']):
				skill_set.add(skill)
				skill_full_list.append(skill)
		index.append(results['id'])
	print len(skill_set)


	df_skills = pd.DataFrame(index=index, columns=skill_set).fillna(0)
	# print df_skills

	cursor_profile = collection.find({})
		# Here I will set the value of
	for profile in cursor_profile:
		if 'skills' in profile:
			user_id = profile['id']
			skill_list = profile['skills']
			# Parse the skill list:
			for skill in skill_list:
				df_skills.ix[user_id, skill] = 1
	# Save the matrix in a pickle
	date_string = utils.get_date_string()
	out_file_matrix = './results/skills_matrix_'+date_string+'.pkl'
	utils.savepickle(df_skills, out_file_matrix)
	# pdb.set_trace()
	return df_skills, skill_full_list

def main():
	print "Main"
	db, collection = utils.initializeDb("zproject", "ext_profiles_processed")
	
	# Return a set of general stats about education and
	# Data Scientists title appearence in the profile

	# df_ds_education = build_education_df(db, collection)
	
	# Build the skills feature dataframe
	
	# build_skills_ds(db, collection)

	df = get_education_features(db, collection )
if __name__ == '__main__':
	main()


