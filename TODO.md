TO DO:
1) Questions for Jonathan: 

-> About the NB components:
1) Shall I use the Bernoulli NB?
  -> Also does it makes sense to classify the major class
  with NB based on all the 5 labels and then get the components 
  of a NB just rained on a dataset with no DS?


2) SO far I've run K-means with all the features.
Shall I use a rediced model based on the top 100 features given by RF? 

-> Best way to doing feat_reduction in my case (is it even wrth it?)
Use just the top 100 returned by a RF? 
The one that appear in there most of the time (runnong multiple times)?

-> I cant' run NMF with 5 features (it takes forever)

4) How can I use decision trees? I would like to leave it out for now.



Focus for the week:
Today: do whatever additional exploration of results with
diffrent reduced models

By wed: get even a simple web-up locally to work (with the bars as interactive 
some dynamic usggesitons of content)

Optional : Visualization of networks of skills focusing on the top 50 for each group
(Or the top 100 overall from my RF).
Maybe over the week end.



Presentation:
1 SLide: why , what?
2 Slide how (number of datapoints, pipeline, )
3 Some results -> tag cloud, skills network (educaiton network)
4) Screeshot webapp
5) Final remarks (links , ack , Next steps: )
===============

0) Get the ball rollin gwith the workflow for the app:
1) write code form the linkeidn public URL to 
-> I've got the features...


CalculatedL 
-> closest profiles
-> missing skills -> resources

-> Histogram of the 5 components (they aybe be 4 ...)
-> How to access for one value i predict the tree 


I want to return


Tonight:
- plot the notworks of skills (where the link came from , 0,1,2,3,4)
- If I want start playing with clustering visualization in D3
- Play with dinamic barplot

EC2 :
Mongodump -> to have the same DB to EC2.
Also install the gem




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

