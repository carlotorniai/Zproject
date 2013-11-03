# Reads my full proifle and create a mongo DB
# Retrieeve the missign fields of 
# poisitions, educations, specialties and skills if missing
# Flag , for which profiles i retrieve what form teh public profile
# Flag Zipfian Students

# TO DO: downlaod_public_profile should take just profile file
# And user Id and return the content of the 
# Public profile

import pymongo
import utils
import subprocess
from time import sleep
import datetime
import json

# For now le'ts try to entich the json / dict I have and store it in new files
# Then I will deal with Mongo for the storage


now = datetime.datetime.now()
day=str(now.day)
month=str(now.month)
year=str(now.year)

def get_raw_profiles_stats(profile_file):
	''' Return basic statistics for a list of Linkedin profiles information '''

	full_list_profiles = utils.readpickle(profile_file)
	user_id_list = set()
	
	dict_metrics = {'num_profiles': 0, 'has_headline':0, 'has_ds_head':0, 'has_summary':0, 
	'has_location':0, 'has_positions':0, 'has_educations':0, 'has_industry':0, 
	'has_ds_specialties':0, 'has_skills':0, 'has_public_profile':0, 'has_courses':0, 
	'has_ds_head':0, 'has_specialties':0, 'has_ds_summary':0, 'has_ds_skills':0}
	
	for profile in full_list_profiles:
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

				if 'data scientist' in profile['specialties'].lower():
					dict_metrics['has_ds_specialties']+=1

			if 'skills' in profile:
				dict_metrics['has_skills']+=1

				for skill in profile['skills']:
					if 'data scientist' in skill.lower():
						dict_metrics['has_ds_skills']+=1

			if 'courses' in profile:
				dict_metrics['has_courses']+=1
		
	dict_metrics['num_profiles'] = len(user_id_list)
	return dict_metrics

def save_public_profile_info(user_id, public_profile_url):
	p = subprocess.Popen(["./linkedin-scraper",  public_profile_url], stdout=subprocess.PIPE)
	out, err = p.communicate()
	json_profile =  json.loads(out)
	profile_out_file = './data/full_profiles/'+user_id+"_profile.json"
	with open(profile_out_file, "wb") as outfile:
		json.dump(json_profile, outfile)
	saved_file = json.load(open(profile_out_file))
	print "Saved public profile for %s" %(user_id)
	# print saved_file

def enhance_profiles(profile_file):
	''' Add the infromation missingin the profile retrieved form the API
	and stores the new profiles in a new list'''

	enhanced_profiles=[]
	profile_list = utils.readpickle(profile_file)
	for profile in profile_list:
		processed = False
		user_id = profile['id']
		pub_profile_file = './data/full_profiles/'+user_id+"_profile.json"
		# Check if file exists
		try:
			with open(pub_profile_file):
				pub_profile = json.load(open(pub_profile_file))
				if  'educations' not in profile:
					print "Missing education"
					# Open the json file and look for education
					if 'education' in pub_profile:
						print "Found education in pub profile file"
						# Add education
						profile['educations'] = pub_profile['education']
						profile['added_education'] = True
					else:
						print "Education not found in public profile"
				
				if  'skills' not in profile:
					print "Missing skills"
					# Open the json file and look for education
					if 'skills' in pub_profile:
						print "Found skills in pub profile file"
						# Add education
						profile['skills'] = pub_profile['skills']
						profile['added_skills'] = True
					else:
						print "Skills not found in public profile"

				if  'specialties' not in profile:
					print "Missing specialties"
					# Open the json file and look for education
					if 'specialties' in pub_profile:
						print "Found specialties in pub profile file"
						# Add education
						profile['specialties'] = pub_profile['specialties']
						profile['added_specialties'] = True
					else:
						print "Specialties not found in public profile"
				
				print profile
		except:
			print("Publice proifle file not found")


		# Add the profile to the new profilesle
		enhanced_profiles.append(profile)
	# Save the pickle with new profile
	out_file_enh_profiles = './data/enhanced_profiles/enchanced_total_unique_profiles_'+day+month+year+'.pkl'
	utils.savepickle(enhanced_profiles, out_file_enh_profiles)

def download_public_profiles(profile_file):
	''' Save scraped public URL pages for the profiles missing
	education or skills and save them in json files'''

	full_list_profiles = utils.readpickle(profile_file)
	for profile in full_list_profiles:
		user_id = profile['id']
		
		if 'publicProfileUrl' in profile:
			print "Downloading data for user ", user_id
			public_profile_url = profile['publicProfileUrl']
			save_public_profile_info(user_id, public_profile_url)

		# if 'publicProfileUrl' in profile:
		# 	public_profile_url = profile['publicProfileUrl']
		# 	print public_profile_url
		# 	print "Profile:"
		# 	# print profile
		# 	retreived=False
		# 	if not 'educations' in profile:
		# 		print 'Missing Education for %s' %(user_id)
		# 		# Retrieve the full profile  
		# 		# Add  the delay required not ot get rejection from the server

		# 		sleep(10)
		# 		download_public_profile_info(user_id, public_profile_url)
				
		# 		retrieved= True
		# 	if (not 'skills' in profile) and not retrieved:
		# 		print 'Missing Skills for %s' %(user_id)
				
		# 		sleep(10)
		# 		download_public_profile_info(user_id, public_profile_url)
				

def main():
	# download_public_profiles('data/total_unique_profile_list.pkl')
	enhance_profiles('data/total_unique_profile_list.pkl')
	metrics  = get_raw_profiles_stats('data/total_unique_profile_list.pkl')
	print "============"
	print "Total profiles:" , len 
	for k, v in metrics.items():
		print k,v
	metrics_enhanced = get_raw_profiles_stats('data/enhanced_profiles/enchanced_total_unique_profiles_2112013.pkl')
	print "=====Enhanced===="
	for k, v in metrics_enhanced.items():
		print k,v
if __name__ == "__main__":
	main()
