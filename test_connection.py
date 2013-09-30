from linkedin import linkedin
import json


    # Playing with authentication
API_KEY = 'qpf6vb1wyseq'
API_SECRET = 'jacN5zyZQUiNT38I'
RETURN_URL = 'http://localhost:8000'

CONSUMER_KEY = 'qpf6vb1wyseq'     # This is api_key
CONSUMER_SECRET = 'jacN5zyZQUiNT38I'   # This is secret_key

USER_TOKEN = '225bcd53-48b7-4732-94da-d43b5048b710'   # This is oauth_token
USER_SECRET = '19585103-9899-4ce4-af6c-9e3f3c854976'   # This is oauth_secret
RETURN_URL = 'http://localhost:8000'


# Define CONSUMER_KEY, CONSUMER_SECRET,  
# USER_TOKEN, and USER_SECRET from the credentials 
# provided in your LinkedIn application

# Instantiate the developer authentication class
# Below there is the annoying errors about the enum
# it has been documented in : https://jira.appcelerator.org/browse/APSTUD-7502
# See also for solution: http://stackoverflow.com/questions/13424565/using-enums-in-jython
# But this doens't work in my editor... freaking Eclipse 

authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
                                                      USER_TOKEN, USER_SECRET, 
                                                      RETURN_URL, linkedin.PERMISSIONS.enums.values())

# Pass it in to the app...

application = linkedin.LinkedInApplication(authentication)

# Testign my auth. It actually works

g= application.get_profile()
print g

# Let's try search for people
data_scientists = application.search_profile(selectors=[{'people': ['first-name', 'last-name']}], params={'keywords': 'data scientist'})
# Search URL is https://api.linkedin.com/v1/people-search:(people:(first-name,last-name))?keywords=apple%20microsoft
print data_scientists

# Need to aprse with JSON
