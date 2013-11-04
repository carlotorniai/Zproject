# A set of method used through the process
#  TO DO
# in get_stats_from_file include additional stats for educ and skills
# in the dict

import pickle
from collections import Counter


def readpickle(filename):
	''' reads a pickle file and return its content'''
	infile = open(filename, "rb")
	content = pickle.load(infile)
	infile.close()
	return content

def savepickle(content, filename):
	''' reads a pickle file and return its content'''
	outfile = open(filename, "wb")
	pickle.dump(content, outfile)
	outfile.close()


def get_stats_from_file(total_profile_file, log=False):
	''' Takes as an input a pickle file containing a list of profiles
	, outputs summary stats and returns the dict with the stats as well as lists of skills'''

	# Initialize the variables
	ed_type_list = []
	ed_topic_list = []
	skill_list= []
	total_ed=0
	total_unparsed=0
	empty_education = 0
	empty_skills = 0
	total_skills = 0
	person_skill_list = []

	# Summary stats dict
	dict_metrics = {'num_profiles': 0, 'has_headline':0, 'has_ds_head':0, 'has_summary':0, 
	'has_location':0, 'has_positions':0, 'has_educations':0, 'has_industry':0, 
	'has_ds_specialties':0, 'has_skills':0, 'has_public_profile':0, 'has_courses':0, 
	'has_ds_head':0, 'has_specialties':0, 'has_ds_summary':0, 'has_ds_skills':0}
	user_id_list = set()
	profile_list = readpickle(total_profile_file)
	for profile in profile_list:
		# Gathering general info
		user_id = profile['id']
		# print user_id
		if not user_id in user_id_list:
			user_id_list.add(user_id)
			# Check if all the fiels are there
			if 'headline' in profile:
				dict_metrics['has_headline']+=1
				# Here check if Data scientist in headline
				if 'data scientist' in profile['headline'].lower():
					dict_metrics['has_ds_head']+=1

			if 'summary' in profile:
				dict_metrics['has_summary']+=1
				if 'data scientist' in profile['summary'].lower():
					dict_metrics['has_ds_summary']+=1

			if 'location' in profile:
				dict_metrics['has_location']+=1

			if 'positions' in profile:
				dict_metrics['has_positions']+=1

			if 'publicProfileUrl' in profile:
				dict_metrics['has_public_profile']+=1

			if 'educations' in profile:
				dict_metrics['has_educations']+=1

			if 'industry' in profile:
				dict_metrics['has_industry']+=1

			if 'specialties' in profile:
				dict_metrics['has_specialties']+=1

				if ('data scientist' in profile['specialties'].lower()) or \
				('data science' in profile['specialties'].lower()):
					dict_metrics['has_ds_specialties']+=1

			if 'skills' in profile:
				dict_metrics['has_skills']+=1

				for skill in profile['skills']:
					if ('data scientist' in skill.lower()) or \
					('data science' in skill.lower()) :
						dict_metrics['has_ds_skills']+=1

			if 'courses' in profile:
				dict_metrics['has_courses']+=1
		
		dict_metrics['num_profiles'] = len(user_id_list)

		if 'educations' in profile:
			# print profile['educations']
			for education in profile['educations']:
				if log:
					print "Original", education
				# pdb.set_trace()
				# Here check if there is a comma, otherwise 
				# we will get the whole or manual curation
				if 'description' in education:
					total_ed+=1
					if ',' in education['description']:
						ed_type = education['description'].split(',')[0]
						ed_topic = education['description'].split(',')[1]
						if log:
							print "Parsed", ed_type, ed_topic
						ed_type_list.append(ed_type)
						ed_topic_list.append(ed_topic)
					else:
						if log:
							print ("Couldn't split")
						if len(education['description'])==0:
							empty_education += 1
						else:
							total_unparsed+=1
						# Here an alternative is to copy the filed
						# In both 			
		# Let's check skills and specialties here.
		if 'skills' in profile:
			person_skills=0
			if len(profile['skills'])>0:
				for skill in profile['skills']:
					skill_list.append(skill)
					total_skills+=1
					person_skills +=1
		else:
			empty_skills += 1
		person_skill_list.append(person_skills)

	# Cast set to get uniq items	
	unique_ed_type = set(ed_type_list)
	unique_ed_topic = set(ed_topic_list)

	# Output general stats
	print ("================")
	print ("General")
	print ("================")
	for k, v in dict_metrics.items():
		print k,v

	# Output Stat about education
	print ("================")
	print ("Education")
	print ("================")
	print ("Total educations: %d") %(total_ed)
	print ("Empty education description %d") %(empty_education)
	print ("Unparsable education %d") %(total_unparsed)
	print ("Number of  education type %d ") %(len(ed_type_list))
	print ("Number of  topics %d") %(len(ed_topic_list))
	print ("Number of unique education type %d") %len(unique_ed_type)
	print ("Number of unique topics %d") %len(unique_ed_topic)
	unique_skills = set(skill_list)
	
	# Output the counter of skills 
	if log:
		print Counter(skill_list)

	# Output the stats about skills
	print ("================")
	print ("Skills")
	print ("================")
	print ("Total skills %d") %(total_skills)
	print ("Empty skills %d") %(empty_skills)
	print ("Unique skills %d") %(len(unique_skills))
	print ("Average skills per person %d ") \
	%(reduce(lambda x, y: x + y, person_skill_list) / len(person_skill_list))
	return person_skill_list, dict_metrics