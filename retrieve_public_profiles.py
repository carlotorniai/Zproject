# TO DO: add parameters:
# input_file
# output_dir
# db, colelction
# search_label, data_scientist_label

import pymongo
import utils
import subprocess
from time import sleep
import datetime
import json



now = datetime.datetime.now()
day=str(now.day)
month=str(now.month)
year=str(now.year)

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

def enhance_profiles(profile_file, search_label, data_scientist_label):
	''' Add the infromation missing in the profile retrieved form the API
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
				
				# Add the additional labels information
				profile['search_label'] = search_label
				profile['label'] = data_scientist_label

				print profile
		except:
			print("Public proifle file not found")


		# Add the profile to the new profilesle
		enhanced_profiles.append(profile)
	# Save the pickle with new profile
	out_file_enh_profiles = './data/enhanced_profiles/STAT_enchanced_total_unique_profiles_'+day+month+year+'.pkl'
	utils.savepickle(enhanced_profiles, out_file_enh_profiles)

def download_public_profiles(profile_file):
	''' Save scraped public URL pages for the profiles missing
	education or skills and save them in json files
	INPUT: str (pickle file name contaning list of profiles'''

	full_list_profiles = utils.readpickle(profile_file)
	for profile in full_list_profiles:
		user_id = profile['id']
		
		if 'publicProfileUrl' in profile:
			print "Downloading data for user ", user_id
			public_profile_url = profile['publicProfileUrl']
			save_public_profile_info(user_id, public_profile_url)			

def main():
	
	# Download public profiles using a list of profiles
	# download_public_profiles('data/total_uniqe_profile_statistician_list.pkl')
	
	# Enhance the profiles  
	enhance_profiles('data/total_uniqe_profile_statistician_list.pkl', 'statistician', '0')
	

if __name__ == "__main__":
	main()
