# Process the profiles in MongoDB collection 
# Of extended profiles to get the feature I will use
# I will define the follwing differnet methods:
import utils
import json
log = True
import pdb

def compute_education_fields(profile):
	''' Returns the normalized values for educaiton '''
	
	parsed_ed_dict = {'phd_1': -1, 'phd_2': -1, "mas_1": -1, \
	 "mas_2" : -1, "bc_1": -1 , "bc_2": -1}
	# All lower
	phd_lookup =  ['phd', 'pd.d.', 'ph.d.', 'doctor of philosophy']
	master_lookup =  ['master', 'ms', "m.s.", "m.s", "ma", "m.a.", "msc"]
	bach_lookup = ['bachelor', 'bachelors', 'b.a.', 'bsc', 'b.s', 'b.sc', 'b.sc.', 'B.E.', 'b.a', 'b.tech', 'bs', 'ba']
	ed_type_lookup = [phd_lookup, master_lookup, bach_lookup]
	found_phd = 0
	found_master = 0
	found_bachelor = 0
	
	# First check if the field is there and is empty
	if len(profile['educations'])==0:
		return  parsed_ed_dict 
	else:
		for education in profile['educations']:
			if ',' in education['description']:
				ed_type = education['description'].split(',')[0]
				ed_topic = education['description'].split(',')[1]
				if log:
					print "Parsed education type: ", ed_type.lower()
					print "Parsed educaiton topic: ", ed_topic.lower()
				# pdb.set_trace()
				# TO DO just loop through the new list of ed lookup

				if ed_type.strip().lower() in phd_lookup:
					# Set the value of Phd_1 to 1
					
					found_phd+=1
					if found_phd==1:
						parsed_ed_dict['phd_1'] = 1
					if found_phd==2:
						parsed_ed_dict['phd_2'] = 1

					# Here check if I can parse the field 

				if ed_type.strip().lower() in master_lookup:
					# Set the value of Phd_1 to 1
					found_master+=1
					if found_master==1:
						parsed_ed_dict['mas_1'] = 1
					if found_master==2:
						parsed_ed_dict['ma_2'] = 1


				if ed_type.strip().lower() in bach_lookup:
					# Set the value of Phd_1 to 1
					found_bachelor+=1
					if found_bachelor==1:
						parsed_ed_dict['bc_1'] = 1
					if found_bachelor==2:
						parsed_ed_dict['bc_2'] = 1	
	pdb.set_trace()			
	return parsed_ed_dict

def compute_skills_fileds(profile):
	''' Returns the normalized vales for skills '''
	return None

def compute_ds_job_fileds(profile):
	''' Returns the values for the data scienits
	job related fields'''
	return None


def main():
	# Grab an example proifle from Mongo and worh with that
	
	# Get db and colleciton:
	db, collection = utils.initializeDb("zproject", "ld_profiles")

	# Get a sample profile form the extended profiles:
	profiles = db.ext_profiles.find()
	profile =  profiles[0]
	print profile
	computed_ed = compute_education_fields(profile)
	print computed_ed
	# At the end when i'm sure of the computation I may want to store it 
	# IN the processed_ext_profiles collection.


if __name__ == '__main__':
	main()

