import json
import pdb
log = False
from datetime import datetime
import pickle 

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