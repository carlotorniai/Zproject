import json
import pandas as pd
import utils
import pymongo
import pdb
import datetime

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

def get_experience(db, collection):
	return 0

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

def get_cat_ed_features(db, collection):
	''' Extracts all the ed information, build a dataframes
	and reurned the transformed dataframes with dummy columns 
	for categorical variables'''
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
	
	# Create the dataframe adding columns for each categroical
	# Value of Education
	df_education_cat = df_education
	for ed_elem in columns:
	    dummy = pd.get_dummies(df_education[ed_elem])
	    del df_education_cat[ed_elem]
	    # Drop the old column
	    df_education_cat =  pd.merge(df_education_cat, dummy, left_index=True, right_index=True)
	
	return df_education_cat

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

def get_full_feature_matrix(db, collection):
    ''' Returns the aggretgated feature matrix 
    for skills and education '''
    ed_features = get_education_features(db, collection)
    skills_features, skills_list = build_skills_ds(db, collection)
    # Merge the featues
    full_features = skills_features.join(ed_features, how='outer')
    # Now 
    return full_features

def get_full_feature_matrix_with_labels(db, collection):
    ''' Returns the aggretgated feature matrix 
    for skills and education plus lables with no zero rows and 
    all values as float '''
    
    full_features_zeros = get_full_feature_matrix_cat(db, collection)
    full_features_nz = utils.drop_zero_rows(full_features_zeros)
    labels = utils.generate_labels_df(full_features_nz, collection)
    full_features_lab = full_features_nz.join(labels, how='outer') 
    full_features = full_features_lab.applymap(float)
    return full_features

def get_full_feature_matrix_cat(db, collection):
    ''' Returns the aggretgated categorized feature matrix 
    for skills and education with no menaingful infor for eduncation
    dropped'''
    full_features = get_full_feature_matrix(db, collection)
    full_features_cat = utils.get_dummy(full_features)
    # Here Drop the no_educaiton fields
    del full_features_cat['no_phd_1']
    del full_features_cat['no_phd_2']
    del full_features_cat['no_mas_1']
    del full_features_cat['no_mas_2']
    del full_features_cat['no_bc_1']
    del full_features_cat['no_bc_2']
    return full_features_cat

def get_clusters_stats(users_clusters, db, collection):
	''' Given user clusters it returns two dicts containing
	the occurences of skills and educaiton per cluster '''
	education_stats = dict()
	skills_stats = dict()
	for k, v in users_clusters.items():
		# Build the dict
		if str(k) in education_stats:
			pass
		else:
			education_stats[k] = []
			skills_stats[k] =  []
	ed_field_list = [ 'bc_1', 'bc_2', 'mas_1','mas_2', 'phd_1', 'phd_2']
	# Now let's fill the values 
	for k, v in users_clusters.items():
		for profile in v:
			# Get the skills and educaiton information
			user_id = profile[0]
			cursor = collection.find({"id": user_id})
			for result in cursor:
				if 'skills' in result:
					for elem in result['skills']:
						skills_stats[k].append(elem)
				for ed_field in ed_field_list:
					if ed_field in result:
						if ed_field != -1:
							education_stats[k].append(result[ed_field])
	return education_stats, skills_stats
    
        

# def main():
# 	print "Main"
# 	# db, collection = utils.initializeDb("zproject", "ext_profiles_processed")
	
# 	# Return a set of general stats about education and
# 	# Data Scientists title appearence in the profile

# 	# df_ds_education = build_education_df(db, collection)
	
# 	# Build the skills feature dataframe
	
# 	# build_skills_ds(db, collection)

# 	# Build the row dataframe for educaiton

# 	# df = get_education_features(db, collection)

# 	# Build the dummy matrix for education
# 	# df = get_cat_ed_features(db, collection)

# if __name__ == '__main__':
# 	main()
