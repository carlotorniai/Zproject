# Reads my full proifle and create a mongo DB
# Retrieeve the missign fields of 
# poisitions, educations, specialties and skills if missing
# Flag , for which profiles i retrieve what form teh public profile
# Flag Zipfian Students

# Loads data into MongoDB from a pickle contaiing json files
import pymongo
import utils
import subprocess
from time import sleep
import json

# For now le'ts try to entich the json / dict I have and store it in new files
# Then I will deal with Mongo for the storage
# Idea: collect the general stats while I go through here.
# Have a set with the ID


def get_raw_profiles_stats(profile_file):
	''' Return basic statistics for a list of Linkedin profiles information '''

	full_list_profiles = utils.readpickle(profile_file)
	user_id_list = set()
	dict_metrics = {'num_profiles': 0, 'has_headline':0, 'has_ds_head':0, 'has_summary':0, 
	'has_location':0, 'has_positions':0, 'has_educations':0, 'has_industry':0, 
	'has_ds_specialties':0, 'has_skills':0, 'has_public_profile':0, 'has_courses':0, 
	'has_ds_head':0, 'has_specialties':0, 'has_ds_summary':0, 'has_ds_skills':0}
	for profile in full_list_profiles:
		print profile
		# Get the id 
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
				# Let's print the profile that doesn't have the education
				# Get the education part from the scraper

			if 'industry' in profile:
				dict_metrics['has_industry']+=1

			if 'specialties' in profile:
				dict_metrics['has_specialties']+=1

				if 'data scientist' in profile['specialties'].lower():
					dict_metrics['has_ds_specialties']+=1

			if 'skills' in profile:
				dict_metrics['has_skills']+=1

				for skill in profile['skills']:
					if 'data scientist' in skill.lower():
						dict_metrics['has_ds_skills']+=1

			if 'courses' in profile:
				dict_metrics['has_courses']+=1
		# Add the total number of unique profiles
	dict_metrics['num_profiles'] = len(user_id_list)
	return dict_metrics

def download_public_profile_info(user_id, public_profile_url):
	p = subprocess.Popen(["./linkedin-scraper",  public_profile_url], stdout=subprocess.PIPE)
	out, err = p.communicate()
	json_profile =  json.loads(out)
	profile_out_file = './data/full_profiles/'+user_id+"_profile.json"
	with open(profile_out_file, "wb") as outfile:
		json.dump(json_profile, outfile)
	saved_file = json.load(open(profile_out_file))
	print "Saved public profile for %s" %(user_id)
	# print saved_file

def enrich_profiles(profile_file):
	''' Retrieve education and skill information from pulic profile URLS 
	and store the enhanced profi'''
	enhanced_profile_list=[]
	full_list_profiles = utils.readpickle(profile_file)
	for profile in full_list_profiles:
		user_id = profile['id']
		if 'publicProfileUrl' in profile:
			public_profile_url = profile['publicProfileUrl']
			print public_profile_url
			print "Profile:"
			print profile
			retreived=False
			if not 'educations' in profile:
				print 'missing Education for %s' %(user_id)
				# Retrieve the full profile  
				# Add he sleep time required not ot get rejection from the server
				sleep(11)
				download_public_profile_info(user_id, public_profile_url)
				retrieved= True
			
			if (not 'skills' in profile) and not retrieved:
				print 'missing Skills for %s' %(user_id)
				download_public_profile_info(user_id, public_profile_url)

def main():
	# metrics  = get_raw_profiles_stats('./data/carlo_full_profile_list1122013.pkl')
	# for k, v in metrics.items():
	# 	print k,v
	enrich_profiles('./data/carlo_full_profile_list1122013.pkl')

if __name__ == "__main__":
	main()
