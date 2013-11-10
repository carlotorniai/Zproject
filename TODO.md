TO DO:
1) Questions fro Jonathan: so the classes ordered arithmetically .. what does it mean?
jsut increasing number? Make sense of the BN values.

0) Get the ball rollin gwith the workflow for the app:
1) write code form the linkeidn public URL to 
-> I've got the features...

Need to cehck the serialized models.

CalculatedL 
-> closest profiles
-> missing skills -> resources

-> Histogram of the 5 components
-> How to access for one value i predict the tree 


I want to return
1) Closetst profiles on Linkedin
1) The idea is the aone classify itself.
If is in the database -> i update the label
I extract the features and I adde it t my feature matrix.

Problems: LIt takes a long time to prune out values and run the model how do you do?

git filter-branch --index-filter '!git rm --cached --ignore-unmatch models/full_features_with_labels_for_RF.pkl' merge-point..HEAD

git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch models/full_features_with_labels_for_RF.pkl' \
  --prune-empty --tag-name-filter cat -- --all



TOnight:
- Plot some other statistics (education for groups)
- If I want start playing with clustering visualization in D3
- Play with dinamic barplot



================
FINAL IDEA:
1) Klout for data scientists.
How do you score in:

Computer Science  (Software Engineering)
Business Analyst
Statistician
Mathematician

Data Scientist
-> Have as an example: the bars
http://columbiadatascience.com/2012/09/08/data-scientist-profiles/

Or the star:
http://columbiadatascience.com/2012/12/08/the-stars-of-data-science/


2) With a decision three also whos 

3) Closests Linkedin profiles:

Things to show:
- Top skills as lists / D3
- Top education
- COmparing top skills form K-menans, NMF , Decision tree
- Show that labels returned from Linkedin or self asserted
arent' really meaningful: (as out assumption)



OLD Notes on approach
==========

SOme ideas of approach.





2) Approach is the exploratory cluster analysis 
and have the user experiment with it

3) The ohter approach can be more of a classification 
You are a 75% of a statistician.

Use random forest for a new user.
You have a strong math background
st
Mathematician

And then run random forest.

For random forest don't drop anything.
The cool thing would I come to an app
and I would say : based on your skills you are most a "Engineer"
And you have these skills in commons ->
The finish app is something like...
What is a value and what they can't get:

4) A recommender approach:
DO you know these top things?
-> like a list of the top skills
I'm going to recommend resources to a person on how to 

Based on the diagnostics you can have an app to collect
you own metrics. WHich links they clicked on 
based on their classificaiton?



Quetions for jon:

-> epliminating all the zeros values in my case folks I didn't
have skills or education or persons for which after features reduciotn
i het all zeros (just top skills)


-> K-means = 2 for now and tell whcih cluster I belong

-> Build a random forest


2) Gather all the data I need 
   -> format the dat nicely

	lunch

3) Run a kmeans with k = 2 with
   education and skills to see if I can tell people
   apart 

   -> training set / tests sets testing 





Tonight:
- If I have time try to compute some more features to get stats
- look at perers video again and figure out some searches that will give me
some good results

For later:
==============
- Do some more NMF and SVD analysis on clustering

- Add the multiindex search on the skills
http://docs.mongodb.org/manual/tutorial/model-data-for-keyword-search/
How to do that:
db.ext_profiles_education_ds.ensureIndex( { skills: 1 } )


- Get linkedin premium and try to get more data
- Change the location of the DB under the project (this can wait)
- Try to explore all the connections for the people I have (once I've got t)
- Think about the best way to maintain Old information with the enhanced one in a persistent way
	-> separate mongo xollections
	-> pandas dataframe
	-> For now just separate mongoDB collections
- refactor and strealine all the pipeline (and generalize)


IMPORTANT:
Once I have the skills I want to create the multikeys 
http://docs.mongodb.org/manual/tutorial/model-data-for-keyword-search/

===============================================

