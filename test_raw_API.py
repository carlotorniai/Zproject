import oauth2 as oauth
import httplib2
from urllib import urlencode
import pdb
import time, os, json


# Global vars
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
 
# Make call to LinkedIn to retrieve your own profile
resp,content = client.request("http://api.linkedin.com/v1/people/~?format=json", "GET", "")
 
print content



def get_person_details(person_id):
	pass

def parse_people(resp_content):
	for person in results['people']['values']:
		last_name = person['lastName']  
		first_name = person['firstName']
		person_id = person['id']
		print first_name, last_name, id
	# Store it somewere for now it can be a dict
		if person_id != 'private':
			get_person_details(person_id)

def serach_for_people(keywords, start=None, count=None):
	''' Search for people'''
	# TO DO fix the urlencode
	# urlib1 didnt' work
	string_query=api_version_string+"people-search?keywords="+keywords+query_format
	if start:
		string_query+="&start"+str(start)
	if count:
		strint_query+="&count"+str(count)
	# print urlencode(string_query)
	print string_query
	resp, content = client.request(string_query)
	results = json.loads(content)
	return results

#Search for Data scientist
results = serach_for_people('Data Scientist')
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

total_people_count = int(results['people']['_total'])
people_pagination =  int(results['people']['_count'])
print total_people_count, people_pagination

# Now I will need to call the  parse people total_people/people pagination 
if total_people_count % people_pagination==0:
	calls = total_people_count/people_pagination
else:
	calls = total_people_count/people_pagination+1

for i in range(calls):
	start = None
	pass

parse_people(results)

