import json
import utils

# Combines several lists of profiles into one 
# Lists just keeping the uniqe user_id


cred = ['mine', 'rob', 'motoki', 'henry', 'paul']
total_unique_profiles = [] 
unique_users = set()
total_profiles = 0;

for name in cred:
	profile_filename = "./data/"+name+"_full_profile_list1182013.pkl"
	profile_list = utils.readpickle(profile_filename)
	for profile in profile_list:
		total_profiles+=1
		user_id = profile['id']
		firstName = profile['firstName']
		lastName = profile['lastName']
		user = (firstName, lastName)
		# print user_id
		if user not in unique_users:
			# Add to unqie profiles
			unique_users.add(user)
			total_unique_profiles.append(profile)
		else:
			print "user  exists" 
			print user
			
# Save the pickle
out_tot_profiles = 'data/total_uniqe_profile_Business_an_list.pkl'
utils.savepickle(total_unique_profiles, out_tot_profiles)
print "Total Profiles: %d, Unique profiles %d, %d" %(total_profiles, len(unique_users) , len(total_unique_profiles))