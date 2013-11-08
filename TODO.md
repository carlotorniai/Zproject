TO DO:

1) Add the new fields search_label and search in enchance profiles.
It's error prone to do it later on.

2) Get the data and build databases for complete with all.

3) Focus on the ds_sf db and run the random forest + the decision 
tree and check resutls.
(lunch)



0) Check with jonathan the results of NMF


1) Get more divers profiles and run NMF equals to the number 

2) Get more data and bins for 
Business Analyst
Statistician

3) Use the random forest and forget the labels and see what we get
(with all the kitchen sink)

4) Look at the features that chooses and run a decisoin tree
with just the features that uses


TOnight:

Download some business analyst data



================
SOme ideas of approach.


2) Approach is the exploratory cluster analysis 
and have the user experiment with it

3) The ohter approach can be mor a classification 
You are a 75% of a statistician.

Use random forest for a new user.
You have a strong math background

Some 

Statisticians
Business Analyst
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

