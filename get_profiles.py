from linkedin import linkedin
import json
from time import sleep

def authenticate():
	''' Parses the credentials, authenticates on Linkedin and return the
	LinkedinApplication object '''
	credentials = json.loads(open('credentials.json', 'r').read())
	API_KEY = credentials['api_key']
	API_SECRET = credentials['api_secret']
	USER_TOKEN = credentials['user_token']
	USER_SECRET = credentials['user_secret']
	CONSUMER_KEY =  credentials['consumer_key']
	CONSUMER_SECRET = credentials['consumer_secret']
	RETURN_URL = 'http://localhost:8000'

	authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
	                                                          USER_TOKEN, USER_SECRET, 
	                                                          RETURN_URL, linkedin.PERMISSIONS.enums.values())
	application = linkedin.LinkedInApplication(authentication)
	# Use the app....
	application.get_profile()
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
	# Here I hould just get back json and parse it as vocab
	person_details = json.loads(content)
	# Returns the person_details
	return person_details['values'][0]

def main():
	log = False
	verbose = False
	application  = authenticate()
	search_results = application.search_profile(selectors=[{'people': ['first-name', 'last-name']}], params={'keywords': '"Data Scientist"', 'start':0, 'count':25})
	# Saves the results in a json file
	if log:
		outfile = open("search_results.json", "wb")
		json.dump(search_results, outfile)
		outfile.close()
	total_people_count = int(search_results['people']['_total'])
	pagination =  int(search_results['people']['_count'])
	start = int(search_results['people']['_start'])
	print "Found %d results" %total_people_count, pagination
	# Computes the number of loops to be executed based on number of
	# results and paginantion
	if total_people_count % pagination==0:
		calls = total_people_count/pagination
	else:
		calls = total_people_count/pagination+1
	print calls
	for i in range(calls):
			# Slow down the requests
			sleep(0.5)
			profile_list=[]
			count = pagination
			results = application.search_profile(selectors=[{'people': ['first-name', 'last-name', 'id']}], params={'keywords': '"Data Scientist"', 'start':start, 'count':count})
			profile_list = parse_search_results(results)
			profile_details_list=[]
			for profile in profile_list:
				profile_id = profile['id']
				if profile_id != 'private':
					if verbose:
						print profile_id 
					profile_details = application.get_profile(member_id = profile_id, \
						selectors=['id', 'first-name', 'last-name', 'headline', 'summary', \
						'location', 'distance', 'num-connections', 'skills',\
						'public-profile-url', 'date-of-birth', 'courses', 'specialties',\
						'educations', 'positions'])
					if verbose:
						print profile_details
					profile_details_list.append(profile_details)
				if log:
					outfile = open("./data/pofiles_"+str(start)+".json", "wb")
					json.dump(profile_details_list, outfile)
					outfile.close()
			start+=pagination

if __name__ == "__main__":
	main()