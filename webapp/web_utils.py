import json
import pdb
from datetime import datetime
import pickle 
import subprocess
import pymongo
from pymongo import MongoClient
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import pdist, cdist , squareform, euclidean
from operator import itemgetter

log = False

# File read and write methods
def readpickle(filename):
	''' reads a pickle file and return its content'''
	infile = open(filename, "rb")
	content = pickle.load(infile)
	infile.close()
	return content

def compute_education_fields(profile):
	''' Returns the normalized values for educaiton '''
	
	parsed_ed_dict = {'phd_1': -1, 'phd_2': -1, "mas_1": -1, \
	 "mas_2" : -1, "bc_1": -1 , "bc_2": -1, "mba_1": -1, "mba_2": -1}
	# All lower
	mba_lookup = ['mba', 'm.b.a']
	phd_lookup =  ['phd', 'pd.d.', 'ph.d.', 'doctor of philosophy']
	master_lookup =  ['master', "ms", "m.s.", "m.s", "ma", "m.a.", "msc", 'm.sc.', 'meng']
	# Not sure if I want to add diploma
	bach_lookup = ['bachelor', 'bachelors', 'b.a.', 'bsc', 'b.s', 'b.sc',\
	 'b.sc.', 'B.E.', 'b.a', 'b.tech', 'bs', 'ba', 'b.sself.', 'b.s.']
	ed_fields = ['computer science', 'computer engineering', 'mathematics', 'physics', \
	'statistics', 'economics', 'psychology', 'engineering', 'bioinformatics', \
	'neuroscience', 'biology', 'astronomy', 'linguistics', 'electronics']

	# ed_type_lookup = [phd_lookup, master_lookup, bach_lookup]
	found_phd = 0
	found_master = 0
	found_bachelor = 0
	found_mba = 0
	# First check if the field is there and is empty
	# The step below parse the fields for 
	if len(profile['education'])==0:
		return  parsed_ed_dict 
	else:
		for education in profile['education']:
			if ',' in education['description']:
				# I may want to construct an array of topics 
				is_phd = False
				is_mas = False
				is_bac = False
				is_mba = False
				ed_topic_list=[]
				ed_type = education['description'].split(',')[0].strip().lower()
				if len(education['description'].split(','))>2:
					for i in range(1, len(education['description'].split(','))):
						ed_topic_list.append(education['description'].split(',')[i].strip().lower())
				else:
						ed_topic_list.append(education['description'].split(',')[1].strip().lower())
				if log:
					print "Parsed education type: ", ed_type
					print "Parsed education topic: ", ed_topic_list
				
				# Refactor code below.
				# Check if is an MBA
				if ed_type in mba_lookup:
					is_mba = True
					found_mba+=1
				else:
					for mba in mba_lookup:
						if mba in ed_type:
							found_mba+=1
							is_mba = True
							break

				# Check if is a Phd
				if ed_type in phd_lookup:
					is_phd = True
					found_phd+=1
				else:
					for phd in phd_lookup:
						if phd in ed_type:
							found_phd+=1
							is_phd = True
							break
					
				# Checks if is a master
				if ed_type in master_lookup:
					is_mas = True
					found_master+=1
				else:
					for mas in master_lookup:
						if mas in ed_type.split(' '):
							found_master+=1
							is_mas = True
							break

				# Checks if is a Bachelor
				if ed_type in bach_lookup:
					is_bac = True
					found_bachelor+=1
				else:
					for bac in bach_lookup:
						if bac in ed_type.split(' '):
							found_bachelor+=1
							is_bac = True
							break
				
				# Parse the educaiton field for MBA 
				if is_mba:
					if found_mba==1:
						parsed_ed_dict['mba_1'] = 1
						for field in ed_fields:
							for topic in ed_topic_list:
								if field in topic:
									parsed_ed_dict['mba_1'] = field
									break

					if found_mba==2:
						parsed_ed_dict['mba_2'] = 1
						for field in ed_fields:
							for topic in ed_topic_list:
								if field in topic:
									parsed_ed_dict['mba_2'] = field
									break
				
				# Parse the educaiton fiels for Phd
				# pdb.set_trace()
				if is_phd:
					if found_phd==1:
						parsed_ed_dict['phd_1'] = 1
						for field in ed_fields:
							for topic in ed_topic_list:
								if field in topic:
									parsed_ed_dict['phd_1'] = field
									break

					if found_phd==2:
						parsed_ed_dict['phd_2'] = 1
						for field in ed_fields:
							for topic in ed_topic_list:
								if field in topic:
									parsed_ed_dict['phd_1'] = field
									break

				# Parse the educaiton fiels for Master
				if is_mas:
					if found_master==1:
						parsed_ed_dict['mas_1'] = 1
						for field in ed_fields:
							for topic in ed_topic_list:
								if field in topic:
									parsed_ed_dict['mas_1'] = field
									break

					if found_master==2:
						parsed_ed_dict['mas_2'] = 1
						for field in ed_fields:
							for topic in ed_topic_list:
								if field in topic:
									parsed_ed_dict['mas_2'] = field
									break

				# Parse the educaiton fiels for Bachelor
				if is_bac:			
					if found_bachelor==1:
						parsed_ed_dict['bc_1'] = 1
						for field in ed_fields:
							for topic in ed_topic_list:
								if field in topic:
									parsed_ed_dict['bc_1'] = field
									break

					if found_bachelor==2:
						parsed_ed_dict['bc_2'] = 1	
						for field in ed_fields:
							for topic in ed_topic_list:
								if field in topic:
									parsed_ed_dict['bc_2'] = field
									break	
	return parsed_ed_dict


def get_education_features(education_dict):
	''' Returns a categorized dict of the education '''
	processed_education = dict()

	for k,v  in education_dict.items():
		if v == 1:
			# processed_education[k] = "other_"+k
			processed_education["other_"+k] = 1
		elif  v == -1:
			pass	

		else:
			#processed_education[k] = k+"_"+v
			processed_education[k+"_"+v] = 1
	return processed_education

def extractfeatures(public_profile_url, feature_matrix, log = False):
    ''' it takes as input an URL of a Linkedin public Profile
    extract features. It returns the json file of the profiles and the feature vector '''

    feature_vector = []
    found_skills = False
    found_education = False
    
    # './models/full-features_no_zeros_for_classification.pkl'
    # Load the feature_matrix
   
    
    # Initialize the dict for the features
    features_dict = dict()
    for elem in feature_matrix.columns:
        features_dict[elem] = 0
        
    # Here need to hanle better all the possible errors
    # For now just a dummy one
    if 'http://' not in public_profile_url and public_profile_url[0] == 'w':
        public_profile_url = 'http://' + public_profile_url
    
    # Retrieve the public profile
    p = subprocess.Popen(["./linkedin-scraper",  public_profile_url], stdout=subprocess.PIPE)
    out, err = p.communicate()
    # Here handle the errors if I put a non existing profile
    if log:
        print "Error" , err
    
    profile = json.loads(out)
    
    # Check if skills and education are in the profile
    # Otherwise Classification can't really be extracted
    
    if 'skills' in profile:
        if len(profile['skills']) > 1:
            found_skills = True
    
    if 'education' in profile:
        if len(profile['education']) > 1:
            found_education = True
    
    if not found_skills and not found_education:
        print "I can't find education and skills information in your profile"
        return 
    
    if found_skills:
    	skills = profile['skills']

    if found_education:
    	educations = compute_education_fields(profile)

    # Now let's process the skills
    for skill in skills:
        if skill in features_dict:
            features_dict[skill] = 1
    
    # Sanity check
    if log:
        for k, v in features_dict.items():
            if v ==1:
                print k
    
    # Check if education is availabel feo
    # Get educations
    if found_education:
	    ed_features = get_education_features(educations)
	    
	    if log:
	        print ed_features
	    
	    # Add educations to the feature dict
	    for k, v in features_dict.items():
	        if k in ed_features:
	            features_dict[k] = 1
    
    #Sanity check
    if log:
        for k, v in features_dict.items():
            if v ==1:
                print k
    # Build just a vector of zeroe and ones
    for elem in feature_matrix.columns:
        if features_dict[elem] == 1:
            # print elem 
            feature_vector.append(1)
        else:
            feature_vector.append(0)
    
    return profile, feature_vector

def get_top_features(feature_matrix, km, n):
    ''' Returns top n features for clusters'''
    top_features = dict()
    
    for clust_num in range(km.n_clusters):
        top_num_skills = 0
        if str(clust_num) in top_features:
            pass
        else:
            top_features[str(clust_num)] = []
        centroid = km.cluster_centers_[clust_num]
        ordered_centroid = [i[0] for i in sorted(enumerate(centroid), key=lambda x:x[1], reverse = True)]
        for i in range(len(ordered_centroid)):
             if top_num_skills<=n:
                 top_features[str(clust_num)].append(feature_matrix.columns.tolist()[ordered_centroid[i]])
                 top_num_skills +=1   
    return top_features

def get_cluster_members(feature_matrix, db, collection, km):
    ''' Returns a dict containing for each cluster the 
        user ID and public URLS for each membember '''
    
    # Initialize the dict
    users_clusters = dict()
    
    # Initizlize DB
    db, collection = initializeDb("zproject", "ext_profiles_processed")
    
    # Create dict keys
    for clust_num in range(km.n_clusters):
        if str(clust_num) in users_clusters:
            pass
        else:
            users_clusters[str(clust_num)] = []

    # Populate the Dict wtih profiles information
    for i in range(len(km.labels_)):
        public_url = ""
        user_id = features_dummy.index[i]
        cursor = collection.find({"id":user_id}, {"_id" : 0, \
        "lastName" :1 , "firstName" :1, "publicProfileUrl" : 1})
        for result in cursor:
            if 'publicProfileUrl' in result:
                public_url = result['publicProfileUrl']
            # Add firstname and lastname
            fname = result['firstName']
            lname = result['lastName']
        value = (user_id, fname, lname, public_url)
        #print user_id, public_url, km.labels_[i]
        users_clusters[str(km.labels_[i])].append(value)
    return users_clusters


def get_cluster_representatitve(feature_matrix, db, collection, km, n):
    ''' Returns a list of the closest n profiles to each 
    cluster centroids '''
    
    # Initialize the dict
    users_clusters = dict()
    ordered_user_clusters = dict()
    
    # Create dict keys
    for clust_num in range(km.n_clusters):
        if str(clust_num) in users_clusters:
            pass
        else:
            users_clusters[str(clust_num)] = []
            ordered_user_clusters[str(clust_num)] = []
            
    # Populate the Dict wtih profiles information
    for i in range(len(km.labels_)):
        public_url = ""
        user_id = feature_matrix.index[i]
        cursor = collection.find({"id":user_id}, {"_id" : 0, \
        "lastName" :1 , "firstName" :1, "publicProfileUrl" : 1, "ds_in_head": 1,
        "ds_in_summary": 1, "ds_job_current":1, "ds_job_past" :1 })
        for result in cursor:
            if 'publicProfileUrl' in result:
                public_url = result['publicProfileUrl']
            # Add firstname and lastname
            fname = result['firstName']
            lname = result['lastName']
            ds_in_summary = result['ds_in_summary']
            ds_in_head = result["ds_in_head"]
            ds_job_current = result["ds_job_current"]
            ds_job_past = result["ds_job_past"]

        # Here get the euclidean distance between the 
        # element and the centroid 
        current_centroid = km.cluster_centers_[km.labels_[i]]
        # print current_centroid, km.labels_[i]
        # pdb.set_trace()
        current_user_features = feature_matrix.loc[user_id]
        # centroid_distance =  cdist(current_centroid, current_user_features, 'euclidean')
        # pdb.set_trace()
        if ds_in_summary or ds_in_head or ds_job_current or ds_job_past:
        	is_ds = 1
        else:
        	is_ds = 0
        centroid_distance = euclidean(current_centroid, current_user_features)
        value = (user_id, fname, lname, public_url, centroid_distance, is_ds)
        #print user_id, public_url, km.labels_[i]
        users_clusters[str(km.labels_[i])].append(value)
        # print users_clusters
        ordered_users_clust = dict()
    for key in users_clusters.keys():
        if n < len(users_clusters[key]):
            ordered_user_clusters[key] = sorted(users_clusters[key],\
                                            key = lambda element : element[4], reverse=False)[:n]
        else:
            ordered_user_clusters[key] = sorted(users_clusters[key],\
                                            key = lambda element : element[4], reverse=False)
        
    return users_clusters, ordered_user_clusters

def get_closest_datascientists(user_feature_vector, feature_matrix, cluster_members):
    ''' Returns , if any the closest data scientist to the user profiles '''
    closest_ds_found = 0
    users_in_cluster = []
    closest_ds = []
    closest_no_ds = []
    for member in cluster_members:
        member_id = member[0]
        # Retrieve the feature vector 
        member_feature_vector = feature_matrix.loc[member_id]
        distance = euclidean(user_feature_vector, member_feature_vector)
        # Add the member and the distance to the list
        value = (member, distance)
        users_in_cluster.append(value)
    # Computes the ordered list
    closest_users_in_cluster = sorted(users_in_cluster,key=itemgetter(1))
    #print closest_users_in_cluster
    for user in closest_users_in_cluster:
    	# Here add the control of distance = 0 so 
    	# The same user isn't ret
        if user[0][5]==1:
            closest_ds.append(user)
        else:
        	closest_no_ds.append(user)
    return closest_ds, closest_no_ds

def initializeDb(db_name, collection_name):
	''' Returns dbname and collection '''
	# connect to the hosted MongoDB instance
	client = MongoClient('mongodb://localhost:27017/')
	db = client[db_name]
	collection = db[collection_name]
	return db, collection
