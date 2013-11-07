from linkedin import linkedin
import json
from time import sleep
import utils
import datetime

now = datetime.datetime.now()
day=str(now.day)
month=str(now.month)
year=str(now.year)
log=False



def authenticate(credential_filename):
	''' Parses the credentials, authenticates on Linkedin and return the
	LinkedinApplication object '''
	credentials = json.loads(open(credential_filename, 'r').read())
	API_KEY = credentials['api_key']
	API_SECRET = credentials['api_secret']
	USER_TOKEN = credentials['user_token']
	USER_SECRET = credentials['user_secret']
	CONSUMER_KEY =  credentials['api_key']
	CONSUMER_SECRET = credentials['api_secret']
	RETURN_URL = 'http://localhost:8000'
	name = credentials['name']
	authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
	                                                          USER_TOKEN, USER_SECRET, 
	                                                          RETURN_URL, linkedin.PERMISSIONS.enums.values())
	application = linkedin.LinkedInApplication(authentication)
	print application.get_profile()
	return application


def parse_search_results(results):
	''' Parses the content of a search results and returns a list 
	of dict with firstName, LastName and person_id information
	'''
	person_details_list=[]
	for person in results['people']['values']:
		print person 
		person_details_dict=dict()
		person_details_dict['lastName'] = person['lastName']  
		person_details_dict['firstName'] = person['firstName']
		person_details_dict['id'] = person['id']
		person_details_list.append(person_details_dict)
	return person_details_list

def get_person_details(last_name, first_name, person_id=None):
	''' It returns all the personal details for a person search '''
	person_details_dict=dict()
	field_selector='people::(id='+person_id+'):(headline,summary,industry,specialties,educations,skills,positions,public-profile-url,date-of-birth,courses)?format=json'
	person_details_query_string = api_version_string+field_selector
	resp, content = client.request(person_details_query_string)
	person_details = json.loads(content)
	return person_details['values'][0]

def search(application, name, keywords):
	''' Retrieves the profiles cotnaing keywords using the credetial of a user '''
	log = True
	search_results = application.search_profile(selectors=[{'people': ['first-name', 'last-name', 'id']}], params={'keywords': keywords, 'start':0, 'count':25})
	
	# Saves the results in pickle file
	if log:
		outfile = "./data/search_results_"+name+"_"+month+day+year+".pkl"
		utils.savepickle(search_results, outfile)
	total_people_count = int(search_results['people']['_total'])
	pagination =  int(search_results['people']['_count'])
	start = int(search_results['people']['_start'])
	print "Found %d results" %total_people_count, pagination
	
	# Computes the number of loops to be executed 
	if total_people_count % pagination==0:
		calls = total_people_count/pagination
	else:
		calls = total_people_count/pagination+1
	print calls
	full_results=[]
	for i in range(calls):
			# Slowdown the requests
			# Just in case
			sleep(0.5)
			profile_list=[]
			count = pagination
			results = application.search_profile(selectors=[{'people': ['first-name', 'last-name', 'id']}], params={'keywords': keywords , 'start':start, 'count':count})
			profile_list = parse_search_results(results)
			profile_details_list=[]
			for profile in profile_list:
				profile_id = profile['id']
				if profile_id != 'private':
					print profile_id 
					# TO DO: add all the possible fields
					profile_details = application.get_profile(member_id = profile_id, \
						selectors=['id', 'first-name', 'last-name', 'headline', 'summary', \
						'location', 'distance', 'num-connections', 'skills',\
						'public-profile-url', 'date-of-birth', 'courses', 'specialties',\
						 'educations', 'positions'])
					print profile_details
					profile_details_list.append(profile_details)
					full_results.append(profile_details)
				outfile = "./data/"+name+"_profiles_"+str(start)+"_"+month+day+year+".pkl"
				utils.savepickle(profile_details_list, outfile)
			
			# Increase the start point 
			start+=pagination
	
	# Save the full_list of results
	outfile = "./data/"+name+"_full_profile_list"+month+day+year+".pkl"
	utils.savepickle(full_results, outfile)
	return full_results

def retrieve_connections(applicaiton, name):
	data_scienctist_connections = []
	outfile = "./data/"+name+"_connections_list.pkl"
	connections = applicaiton.get_connections(selectors=['id', 'first-name', 'last-name', 'headline', 'summary', \
						'location', 'distance', 'num-connections', 'skills',\
						'public-profile-url', 'date-of-birth', 'courses', 'specialties',\
						 'educations', 'positions'])
	print connections.keys()
	# Save the file first and in case do the processing later
	utils.savepickle(connections, outfile)

	connections = utils.readpickle(outfile)
	for connection in connections['values']:
		found = False
		# Here I have the single value in the connection
		# Now I want just to return the connection if it has "data scient"

		if 'headline' in connection:
			if 'data scientist' in connection['headline'].lower():
					found = True
					print connection['firstName'] , connection['lastName']
					print "Data Scientist in Headline"
		
		if 'positions' in connection:
			# print connection['positions']
			positions_num = connection['positions']['_total']
			for i in range(int (positions_num)):
				position = connection['positions']['values'][i]
				if 'data scientist' in position['title'].lower():
					found = True
					print connection['firstName'] , connection['lastName']
					print "Data Scientist in a position"

		if 'summary' in connection:
			if 'data scientist' in connection['summary'].lower():
				found = True
				print connection['firstName'] , connection['lastName']
				print "Data Scientist in Summary"

		if found:
			data_scienctist_connections.append(connection)
	# Save the data scientist connections
	outfile_conn = "./data/"+name+"_data_science_connections"+month+day+year+".pkl"
	utils.savepickle(data_scienctist_connections, outfile_conn)
	return data_scienctist_connections

def main():
	''' Here I'm looping through the verious credential files and 
	retrieve results for each credentail '''
	cred = [ 'mine', 'amanuel', 'motoki', 'henry', 'rob', 'paul']

	connections_dict = dict()
	total_profiles_list =[]
	for name in cred:
		credential_filename = "credentials_"+name+".json"
		application= authenticate(credential_filename)
		
		# Search the Results
		profile_results = search(application, name, 'Software Engineer')
		
		# Append the results to the total_profiles
		total_profiles_list.append(profile_results)
		
		# Get the connection
		# ds_connections = retrieve_connections(application, name)
		
		# Add to the dictionary
		# connections_dict[name] = ds_connections

	# Save all the profiels retrieved
	total_out_file = "./data/total_profiles_se"+month+day+year+".pkl"
	utils.savepickle(total_profiles_list, total_out_file)

	# Save all the connections for each user retrieved.
	# total_conn_file = "./data/connections/total_ds_conn"+month+day+year+".pkl"
	# utils.savepickle(connections_dict, total_conn_file)

if __name__ == "__main__":
	main()