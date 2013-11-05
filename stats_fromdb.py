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
	index= []
	# Build columns and index to create the dataframe
	cursor  = collection.find({}, {"_id":0, "skills":1, "id":1})
	for results in cursor:
		# pdb.set_trace()
		if "skills" in results:
			for skill in (results['skills']):
				skill_set.add(skill)
		index.append(results['id'])
	print len(skill_set)


	df_skills = pd.DataFrame(index=index, columns=skill_set).fillna(0)
	print df_skills

	cursor_profile = collection.find({})
		# Here I will set the calue of
	for profile in cursor_profile:
		if 'skills' in profile:
			user_id = profile['id']
			skill_list = profile['skills']
			# Parse the skill list:
			for skill in skill_list:
				df_skills.ix[user_id, skill] = 1
	# Save the matrix in a pickle
	date_string = utils.get_date_string()
	out_file = './results/skills_matrix_'+date_string+'.pkl'
	utils.savepickle(df_skills, out_file)
	return df_skills

def main():
	print "Main"
	db, collection = utils.initializeDb("zproject", "ext_profiles_processed")
	
	# df_ds_education = build_education_df(db, collection)
	
	build_skills_ds(db, collection)

if __name__ == '__main__':
	main()


