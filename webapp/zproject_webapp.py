import json
from flask import Flask, request, Response, redirect, url_for
import pickle
import web_utils as wu
from nbpredictor import predict

app = Flask(__name__)


def readpickle(filename):
    ''' reads a pickle file and return its content
    INPUT string
    OUTPUT object'''
    infile = open(filename, "rb")
    content = pickle.load(infile)
    infile.close()
    return content

# Load the trained model and the vectorizer
trained_model = readpickle('trained_nb_model.pkl')
print type(trained_model)
vectorizer = readpickle('vectorizer.pkl')
print type(vectorizer)

@app.route("/predict", methods=['POST'])
def execute():
    #pdb.set_trace()
    url = request.form['url']
    print url
    # Here add also the check if the nytimes.comis in there.
    if url!="":
        # Here predict the label
        label = predict(trained_model, vectorizer, url)
        results = "Your article should belong in the " + label + " section of the NYT"
        print label
    else:
        results = "You should post a URL of a NYT article"
    if request.method == 'POST': 
        return Response(results, status=200,  mimetype='text/plain')
    else:
        return "You shoudl post a URL of a NYT article!!"

@app.route("/getldinfo", methods=['POST'])
def execute_text():
    text = request.form['text']
    print text
    if request.method == 'POST':
        if text=='':
            results = "Please paste your Linkedin Public Profile URL in the input area"
        else:
            label = predict(trained_model, vectorizer, text, True)
            print label
            results = "Your text belongs to the " + label + " section of the NYT"
        return Response(results, status=200,  mimetype='text/plain')
    else:
        return "Post a URL form a NYT article!!"

# Order of routes matters
@app.route("/<name>")
def hello(name):
    return "Hello " + name + "!\nWelcome to my NYT article section Predictor! )"

@app.route("/")
def index():
    return redirect(url_for('static', filename='index.html'))
   

if __name__ == "__main__":
    app.run(host='0.0.0.0')