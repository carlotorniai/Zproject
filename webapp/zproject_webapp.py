import json
from flask import Flask, request, Response, redirect, url_for
import pickle
import web_utils as wu
import pdb
from urllib2 import urlopen
import re 

app = Flask(__name__)

# Here I will need to load all the models i need
# This cell contains all the things that need to be loaded
# At bootstrap and global variables

# All the things below can be doen ONE TIME at the boostrap of the app

# Feature Matrix for the Naive Bayes
print ("Loading required resources....")
print ("Loading feature matrix for NB and KM ....")
feature_matrix = wu.readpickle('./models/full-features_no_zeros_for_classification.pkl')

#Naive Bayes Model for classification
print ("Loading NB model for classification....")
mnb = wu.readpickle('./models/NB_with_full_features_with_labels.pkl')

# Naive Bayse Model for components
print ("Loading NB model for components....")
mnb_no_ds = wu.readpickle("./models/all_but_ds_NB_with_full_features_with_labels.pkl")
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

# Here have a list of the top from ML
top_ds_skills = ['Data Mining', 'Machine Learning', 'R', 'Data Analysis', 'Python',\
                 'Statistical Modeling', 'Hadoop', 'Big Data', 'Statistics', \
                 'SQL', 'Predictive Analytics', 'Pig', 'Hive', 'MapReduce']

# Here define the json file for vega response
plot_json = json.load(open('./plot.json'))
print plot_json
print ("Ready...")

# Add regular expression to check URL
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

@app.route("/getldinfo", methods=['POST'])
def execute_text():
    # Neet to initialize the json file
    # At this point better to write it down to minimize the access time
    # But for now i read it from file
    # plot_json = json.load(open('./plot.json'))
    fields_response = {"error" : '', "header" : '', "text_classification" : '', "profile_components" : {},
"close_ds_profiles" : [], "close_non_ds_profiles" : [], "recomm_skills" :[], "component_plot" : plot_json} 
    
    # Clear the data of plot_json
    fields_response['component_plot']['data'][0]['values']=[]
    public_profile_url = request.form['text']
    if request.method == 'POST':
        # If I post an empty URL return the erro rmessage
        if public_profile_url=='':
            fields_response['error'] = "Please paste a valid Linkedin Public Profile URL"\
            " in the input area above"
            js = json.dumps(fields_response)
            return Response(js, status=200,  mimetype='text/json')
        else:
            # Add the http:// if is not there"
            if 'http://' not in public_profile_url:
                public_profile_url = 'http://' + public_profile_url
                print public_profile_url
            # At this point I want to check if it's a valid URL
            # using the 
            if re.match(regex, public_profile_url) != None:
                code = urlopen(public_profile_url).code
                if (code / 100 >= 4):
                    fields_response['error'] =  "The URL cannot be opened. Please double "\
                    "check you've pasted a valid Linkedin Public Profile URL in the input area above."\
                    "Error code: " +str(code)
                    js = json.dumps(fields_response)
                    return Response(js, status=200,  mimetype='text/json')
                else:
                    # We have a valid URL and hopefully we have extractet 
                    print "Extracting features and profile"
                    print feature_matrix.shape
                    # pdb.set_trace()
                    
                    # Do try catch
                    try: 
                        profile, feature_vector = wu.extractfeatures(public_profile_url, feature_matrix, log = False)
                    # Here check if I was able to retrieve the 
                    # Education and Skills 
                    except:
                        fields_response['error'] = "<p>Education and skills are nort available for this Linkedin Profile.</p>"\
                        "<p>Please make available this information if this is your profile. Or try a different one.</p>"
                        js = json.dumps(fields_response)
                        return Response(js, status=200,  mimetype='text/json')

                    print feature_matrix.shape
                    # string_header = "<br>This is the profile of %s %s </br>" %(profile['first_name'], profile['last_name'])
                    # string_header  = string_header + "<br>Currently %s</br>" %(profile['title'])
                    
                    # fields_response['header'] = string_header
                    fields_response['header'] =  {"first_name" : profile['first_name'], "last_name" : profile['last_name'], \
                    "title" : profile['title']}
                    
                    # Here computes the classification
                    class_label_key = mnb.predict(feature_vector)
                    print ("User classified as %s") %lables_dict[int(class_label_key)]
                    
                    # Set the classification fiels
                    fields_response['text_classification'] = lables_dict[int(class_label_key)]
                    
                    # Retrieve the components
                    other_labels_prob = mnb_no_ds.predict_proba(feature_vector)
                    print "Probability vectors other cells" , other_labels_prob[0]
                    tot_sum = other_labels_prob[0].sum()
                    percentage = [x/tot_sum for x in other_labels_prob[0]]
                    # Below actually return the one float point

                    # fields_response['profile_components']['CS'] = "%.1f" %(percentage[0]*100)
                    # fields_response['profile_components']['ST'] = "%.1f" %(percentage[1]*100)
                    # fields_response['profile_components']['BA'] = "%.1f" %(percentage[2]*100)
                    # fields_response['profile_components']['MT'] = "%.1f" %(percentage[3]*100)
                 
                    # Here I'm going to add the proper values
                    # to the plot_json and then send it
                    fields_response['component_plot']['data'][0]['values'].append({"x": "CS", "y": float("%.1f" %(percentage[0]*100))})
                    fields_response['component_plot']['data'][0]['values'].append({"x": "ST", "y": float("%.1f" %(percentage[1]*100))})
                    fields_response['component_plot']['data'][0]['values'].append({"x": "BA", "y": float("%.1f" %(percentage[2]*100))})
                    fields_response['component_plot']['data'][0]['values'].append({"x": "MT", "y": float("%.1f" %(percentage[3]*100))})
                                
                    suggested_skills = set(top_ds_skills) - set(profile['skills'])
                    for skill in suggested_skills:
                        print skill
                        # Here have a set of links to that in the future
                        fields_response['recomm_skills'].append(skill)

                    # Here assign the user to a cluster
                    closest_cluster = km.predict(feature_vector)
                    #Compute the closest DS
                    closest_ds, closest_all = wu.get_closest_datascientists(feature_vector, feature_matrix, users_clusters[str(closest_cluster[0])])
                    if len(closest_ds)>0:
                        if len(closest_ds)>=3:
                            num_item = 3
                        else:
                            num_item = len(closest_ds)
                        for elem in closest_ds[:num_item]:
                        # Make sure not to present the user itself
                            if profile['last_name']!= elem [0][2]:
                                # Add the element to the tuple 
                                ds_tuple = (elem[0][1], elem [0][2], elem [0][3])
                                # print elem[0][1], elem [0][2], elem [0][3]
                                # Add the element to the response field
                                fields_response['close_ds_profiles'].append(ds_tuple)
                            else:
                                if profile['first_name']!= elem [0][1]:
                                    ds_tuple = (elem[0][1], elem [0][2], elem [0][3])
                                    # print elem[0][1], elem [0][2], elem [0][3]
                                    fields_response['close_ds_profiles'].append(ds_tuple)
                    
                    # Compute close non_ds
                    if len(closest_all)>0:
                        if len(closest_all)>=3:
                            num_similar = 3
                        else:
                            num_similar = len(closest_all)
                        for elem in closest_all[:num_similar]:
                        # Make sure not to present the user itself
                            if profile['last_name']!= elem [0][2]:
                                # Add the element to the tuple 
                                ds_tuple = (elem[0][1], elem [0][2], elem [0][3])
                                # print elem[0][1], elem [0][2], elem [0][3]
                                # Add the element to the response field
                                fields_response['close_non_ds_profiles'].append(ds_tuple)
                            else:
                                if profile['first_name']!= elem [0][1]:
                                    ds_tuple = (elem[0][1], elem [0][2], elem [0][3])
                                    # print elem[0][1], elem [0][2], elem [0][3]
                                    fields_response['close_non_ds_profiles'].append(ds_tuple)

                    # Print the response on the console
                    print fields_response
                    js = json.dumps(fields_response)
                # I want to send back a json with all I need.
                return Response(js, status=200,  mimetype='text/json')
            else:
                # The URL is not a valid URL
            
                fields_response['error'] =  "The URL is malformed. Please paste"\
                " a valid Linkedin Public Profile URL in the input area above."
                js = json.dumps(fields_response)
                return Response(js, status=200,  mimetype='text/json')
                
    else:
        return "Need POST request!!"

# Order of routes matters
@app.route("/<name>")
def hello(name):
    return "Hello " + name + "!\nWelcome to Quantified Data Scientists! )"

@app.route("/")
def index():
    return redirect(url_for('static', filename='index.html'))
   

if __name__ == "__main__":
    # Debug mode on 
    app.debug = True
    app.run(host='0.0.0.0')