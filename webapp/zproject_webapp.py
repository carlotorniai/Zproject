import json
from flask import Flask, request, Response, redirect, url_for
import pickle
import web_utils as wu
import pdb
from urllib2 import urlopen

app = Flask(__name__)

# Here I will need to load all the models i need
# This cell contains all the things that need to be loaded
# At bootstrap and global variables

# All the things below can be doen ONE TIME at the boostrap of the app

# Feature Matrix for the Naive Bayes
print ("Loading required resources....")
print ("Loading feature matrix for NB and KM ....")
feature_matrix = wu.readpickle('./models/full-features_no_zeros_for_classification.pkl')

#Naive Bayes Model
print ("Loading NB model....")
mnb = wu.readpickle('./models/NB_with_full_features_with_labels.pkl')

# # Load feature Matrix for K-Means
# print ("Loading feature matrix for KM....")
# feature_matrix_km = wu.readpickle('./models/full-features_no_zeros_for_classification.pkl')

# Load k-Means model
print ("Loading KM model....")
km = wu.readpickle('./models/kmean_model_with_full_features_no_zeros.pkl')

# DB info
print ("Accessing DB....")
db, collection = wu.initializeDb("zproject" , "final_full_profiles")

# Get top skills for the clusters 
print ("Computing top skills for clusters...")
top_features = wu.get_top_features(feature_matrix, km, 20)

# Retrieve user_clusters and most representative users for each cluster
print ("Getting clusters representatives...")
users_clusters, ordered_user_clusters = wu.get_cluster_representatitve(feature_matrix, db , collection, km , 5)

# Global Vars
lables_dict = {0 : "Computer Scientist", 1 : "Data Scientist", 2 : "Statistician",\
                   3 : "Business Analyst", 4 : "Mathematician"}

top_ds_skills = ['Data Mining', 'Machine Learning', 'R', 'Data Analysis', 'Python',\
                 'Statistical Modeling', 'Hadoop', 'Big Data', 'Statistics', \
                 'SQL', 'Predictive Analytics', 'Pig', 'Hive', 'MapReduce']

fields_response = {"error" : '', "header" : '', "text_classification" : '', "profile_components" : [],
"close_ds_profiles" : [], "close_non_ds_profiles" : [], "recomm_skills" :[]} 


@app.route("/getldinfo", methods=['POST'])
def execute_text():
    public_profile_url = request.form['text']
    if request.method == 'POST':
        if public_profile_url=='':
            fields_response['error'] = "Please paste your Linkedin Public Profile URL in the input area"
        else:
            code = urlopen(public_profile_url).code
            if (code / 100 >= 4):
                fields_response['error'] =  "The URL cannot be opened. Please double check you've pasted a correct URL"
            else:
                print "Extracting features and profile"
                print feature_matrix.shape
                # pdb.set_trace()
                profile, feature_vector = wu.extractfeatures(public_profile_url, feature_matrix, log = False)
                print feature_matrix.shape
                string_header = "<br>This is the profile of %s %s </br>" %(profile['first_name'], profile['last_name'])
                string_header  = string_header + "<br>Currently %s</br>" %(profile['title'])
                fields_response['header'] = string_header
                print string_header
                js = json.dumps(fields_response)
            # I want to send back a json with all I need.
        return Response(js, status=200,  mimetype='text/json')
    else:
        return "Need POST request!!"

# Order of routes matters
@app.route("/<name>")
def hello(name):
    return "Hello " + name + "!\nWelcome to my NYT article section Predictor! )"

@app.route("/")
def index():
    return redirect(url_for('static', filename='index.html'))
   

if __name__ == "__main__":
    # Debug mode on 
    app.debug = True
    app.run(host='0.0.0.0')