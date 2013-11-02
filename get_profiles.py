from linkedin import linkedin
import json
import pickle
from time import sleep

user_name="me"
date="11_01"
log=True

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

def search(application):
	log = True
	search_results = application.search_profile(selectors=[{'people': ['first-name', 'last-name', 'id']}], params={'keywords': '"Data Scientist"', 'start':0, 'count':25})
	
	# Saves the results in pickle file
	if log:
		outfile = "./data/"+date+"/search_results_"+user_name+".pkl"
		savepickle(search_results, outfile)
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
			results = application.search_profile(selectors=[{'people': ['first-name', 'last-name', 'id']}], params={'keywords': '"Data Scientist"', 'start':start, 'count':count})
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
				outfile = "./data/"+date+"/"+user_name+"_profiles_"+str(start)+".pkl"
				savepickle(profile_details_list, outfile)
			
			# Increase the start point 
			start+=pagination
	
	# Save the full_list of results
	outfile = "./data/"+date+"/full/"+user_name+"_full_profile_list.pkl"
	savepickle(full_results, outfile)

def retrieve_connections(applicaiton):
	data_scienctist_connections = []
	outfile = "./data/"+date+"/full/"+user_name+"_connections_list.pkl"
	connections = applicaiton.get_connections(selectors=['id', 'first-name', 'last-name', 'headline', 'summary', \
						'location', 'distance', 'num-connections', 'skills',\
						'public-profile-url', 'date-of-birth', 'courses', 'specialties',\
						 'educations', 'positions'])
	print connections.keys()
	
	# Save the file first and in case do the processing later
	savepickle(connections, outfile)

	connections = readpickle(outfile)
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
		if found:
			data_scienctist_connections.append(connection)
	# Save the data scientist connections
	outfile_conn = "./data/"+date+"/full/"+user_name+"_data_science_connections.pkl"
	savepickle(data_scienctist_connections, outfile_conn)

def main():
	credential_filename = 'credentials_mine.json'
	application  = authenticate(credential_filename)
	# search(application)
	retrieve_connections(application)

if __name__ == "__main__":
	main()