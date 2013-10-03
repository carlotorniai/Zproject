import oauth2 as oauth
import httplib2	
from urllib import quote_plus, urlretrieve
from urllib2 import build_opener
import pdb
import time, os, json
from bs4 import BeautifulSoup
import json
import pickle

# Ok I want an object which is a linkedin_profile
# The object has a set of attributes which are the one of Linkedin
# I store them in a list of dict
# I instatioate each person for each result of the search using the unique ID if present or 
# Then I save the whole list in a pickle

# class ldprofile(id, profile_data):
# 	''' Represents a linkedin profile instance'''

# 	def __init__(self, id):
# 		self.id=id
# 		self.profile_data = profile_data
	


query_format = "&format=json"
api_version_string  ="http://api.linkedin.com/v1/"

# API specific vars
api_key = 'qpf6vb1wyseq'
api_secret = 'jacN5zyZQUiNT38I'
user_token = '225bcd53-48b7-4732-94da-d43b5048b710'
user_secret = '19585103-9899-4ce4-af6c-9e3f3c854976' 
consumer_key =  'qpf6vb1wyseq'
consumer_secret = 'jacN5zyZQUiNT38I'

# TO DO:
# below has to be a funciton
# Use your API key and secret to instantiate consumer object
consumer = oauth.Consumer(consumer_key, consumer_secret)
 
# Use your developer token and secret to instantiate access token object
access_token = oauth.Token(
            key=user_token,
            secret=user_secret)
 
client = oauth.Client(consumer, access_token)

# Test
# Make call to LinkedIn to retrieve your own profile
#resp,content = client.request("http://api.linkedin.com/v1/people/~?format=json", "GET", "")
 
#print content



def get_person_details(last_name, first_name, person_id=None):
	person_details_dict=dict()
	
	field_selector='people::(id='+person_id+'):(headline,summary,industry,specialties,educations,skills,positions,public-profile-url,date-of-birth,courses)?format=json'
	person_details_query_string = api_version_string+field_selector

	# Whenever I can get a public profile I can try to scrape thigns with beautiful soup

	# (headline,summary,industry,specialty,public-profile-url,positions,skills,date-of-birth,eductations,certifications)'
	#http://api.linkedin.com/v1/people::(~,id=12345,url=http%3A%2F%2Fwww.linkedin.com%2Fin%2Fadamnash):(id,first-name,last-name)
	# (headline,summary,industry,specialty,public-profile-url,positions,skills,date-of-birth,eductations,certifications)'
	print person_details_query_string
	# Let's try to call 
	# this url worked: http://api.linkedin.com/v1/people::(id=ZBR0CSkTK_):(headline,summary)
	resp, content = client.request(person_details_query_string)
	# Here I hould just get back json and parse it as vocab
	# print resp, content
	person_details = json.loads(content)
	#for fields in person_details['values']:
		# # each element in values represent one result if I ask for a person I have just one dict in here
		# print "Key:", field['_key']
		# person_details_dict['_key='] = person_details_dict['_key']
		# print "headline", field['headline']
		# person_details_dict['headline']= person_details_dict['headlines']
		# print "industry" , filed['industry'
		# person_details_dict['industry']
		# It is already a list of dict so i can jsu treturn it.
	return person_details['values'][0]

def parse_people(resp_content):
	# print "Content to be parsed in parse_people"
	# print resp_content
	''' returns a list of dict with the profile data
	INPUT: dict()
	OUTPUT: [dict()]'''
	person_details_list=[]
	for person in resp_content['people']['values']:
		#print person
		person_details_dict=dict()
		person_details_dict['lastName'] = person['lastName']  
		person_details_dict['firstName'] = person['firstName']
		person_details_dict['id'] = person['id']
		# Append to the list
		person_details_list.append(person_details_dict)
	return person_details_list
		


def serach_for_people(keywords, start=0, count=None):
	''' Search for people'''
	# TO DO fix the urlencode
	# urlib1 didnt' work
	string_query=api_version_string+"people-search?keywords="+keywords+query_format
	string_query+="&start="+str(start)
	if count:
		string_query+="&count="+str(count)
	# print urlencode(string_query)
	print string_query
	resp, content = client.request(string_query)
	results = json.loads(content)
	return results

#Search for Data scientist

# Now I need to cycle trough the 
# Now Let's ask about data scientests on my network
# resp, content = client.request("http://api.linkedin.com/v1/people-search?keywords=Data+Scientist&format=json")
# results = json.loads(content)
# Now I have the results in number of people 
# numResults": 5338,
#   "people": {
#     "_count": 10,
#     "_start": 0,
#     "_total": 110,
#     "values": [
#       {
# print results

def scrapeskills(profile_url):
	''' Scraping skills from a public profile page'''
	# get the public profiel page
	# Trying with urlib first i may not need full js and stuff...
	# the following commands saves a funky page
	# f = urlretrieve(profile_url,'profile.html')
	opener = build_opener()
	url_opener = opener.open(profile_url)
	page = url_opener.read()
	html = BeautifulSoup(page) 

	# I want to get all the 
	#<span class="skill-pill">
	# <a class="endorse-count" href="javascript:void(0)" role="button" title="See endorsers">
	# <span class="num-endorsements" data-count="7">7</span></a>
	# <span class="endorse-item-name "><span class="endorse-item-name-text">Git
	# </span></span></span>
	# Get all the span class "skill-pill" ... i dont' have it when retreived with urllib...
	# I just get a set of tabs and no ranking.. uhmm
	# for span in html.findAll('span'):
	#	if  span.find("span","kill-pill"):
	#		print span.find("span","d").string

	# How to embed all the info we need.. but not skills

def main():
	profile_list=[]
	results = serach_for_people('Data Scientist')
	# print results
	total_people_count = int(results['people']['_total'])
	people_pagination =  int(results['people']['_count'])
	print "Found:"
	print total_people_count, people_pagination

	# Now I will need to call the  parse people total_people/people pagination 
	if total_people_count % people_pagination==0:
		calls = total_people_count/people_pagination
	else:
		calls = total_people_count/people_pagination+1
	start_index=0
	#Change it later into range(calls)
	for i in range(calls):
		count = people_pagination
		people_results = serach_for_people('Data Scientist', start_index, count)
		people_list = parse_people(people_results)
		for person in people_list:
			#Start a new dict
			person_details=dict()
			person_details['lastName'] = person['lastName']  
			person_details['firstName'] = person['firstName']
			person_details['id'] = person['id']
			if person['id'] != 'private':
				print "Getting person details"
				person_details_dict = get_person_details(person_details['lastName'], person_details['firstName'] , person['id'])
				# Here I want to parse all the results
				person_details['_key'] = person_details_dict['_key']
				if 'headline' in person_details_dict.keys():
					person_details['headline'] = person_details_dict['headline']
				if 'industry' in person_details_dict.keys():
					person_details['industry'] = person_details_dict['industry']
				if 'specialties' in person_details_dict.keys():
					person_details['specialties'] = person_details_dict['specialties']
				if 'educations' in person_details_dict.keys():
					person_details['educations'] = person_details_dict['educations']
				if 'skills' in person_details_dict.keys():
					person_details['skills'] = person_details_dict['skills']
				if 'positions' in person_details_dict.keys():
					person_details['positions'] = person_details_dict['positions']
				if 'public-profile-url' in person_details_dict.keys():
					person_details['public-profile-url'] = person_details_dict['public-profile-url']
				if 'date-of-birth' in person_details_dict.keys():
					person_details['date-of-birth'] = person_details_dict['date-of-birth']
				if 'courses' in person_details_dict.keys():
					person_details['courses'] = person_details_dict['courses'] 
			profile_list.append(person_details)
		# person_details_dict['industry']
		# It is already a list of dict so i can jsu treturn it.
		start_index+=people_pagination
		
	# Done parsing I want to save the file with pickle
	outfile = open("pofiles.ld", "wb")
	pickle.dump(profile_list, outfile)
	outfile.close()
	infile = open("pofiles.ld", "rb")
	pickle.load(infile)



if __name__ == "__main__":
	main()
	# Here testing main
    #people_results = serach_for_people('Data Scientist', 0, 10)
    #person_details_dict = get_person_details('Levine', 'Thomas', 'ZBR0CSkTK_')
    #for k, v in person_details_dict.items():
    #print k , v
    # scrapeskills('http://www.linkedin.com/in/tlevine')

