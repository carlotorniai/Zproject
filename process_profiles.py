# Here I will have just methods that 
# WIll process the profiles and save them into a mondo DB

# For now I want to have a look at what I can 
# Get out of the files

# Store the row data in Mongo as well?
import utils
import pdb
import numpy as np
from collections import Counter

ed_type_list = []
ed_topic_list = []
skill_list= []
total_ed=0
total_unparsed=0
empty_education = 0
log = False
empty_skills = 0
total_skills = 0
person_skill_list = []
profile_list = utils.readpickle('./data/enhanced_profiles/enchanced_total_unique_profiles_2112013.pkl')
for profile in profile_list:
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



np_ed_type_list = np.array(ed_type_list)
np_ed_topic_list = np.array(ed_topic_list)

unique_ed_type = set(ed_type_list)
unique_ed_topic = set(ed_topic_list)
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
print Counter(skill_list)
print ("================")
print ("SKills")
print ("================")
print ("Total skills %d") %(total_skills)
print ("Empty skills %d") %(empty_skills)
print ("Unique skills %d") %(len(unique_skills))
print ("Average skills per person %d ") %(reduce(lambda x, y: x + y, person_skill_list) / len(person_skill_list))

# SOme more info that will allow me to choose the sets.
# print Counter(ed_type_list)
# print Counter(ed_topic_list)