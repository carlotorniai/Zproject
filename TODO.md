TO DO:


0) Build my facility for getting the X closest
point to the centroids

DANG IT TOOK A LOT BUT I Built it.
The ontly thing is that i use eucliean distance.


1) THEN:
	1) Experiment clustering (k_means) with the log tenimoto distance
	it accounts for binary values

	2) Try NMF ->

	3) Try SVD

	Then stop and move on on colleting additional data
	-> look at peter clusters


- Finish the method to return the dummy feature matrixces
  -> in stats_fromDB.py
- DO hierarchical clustering (ok not really meaningful..)
	-> Ways to evaluate?

- Do some initial k-means and analysis
	-> ok done wiht a small set of features.
	-> WOrk on clusterign evaluation

	-> Top 3 close to centroid
	-> Top educations
	-> Top skills

	1) FInd the point closer to the center for each clusters.
	-> try to understand the difference in features.

	2) Try to find some meaninful "measure" of
	goodness
	-> Try http://stackoverflow.com/questions/12680038/validating-output-from-a-clustering-algorithm

-> Flag Zipfian folks

-> Add the DS_flag to the current data




Write down a New iPython with stats and plot.
- Plot the top 40 Skills listed
- Plot the Phd . MS and TOpc 
- Plot the frequency of the Job title (for current positions)


Tonight:
- Plot the frequency of the Job title (for current positions)
- read something, grab the screen shot for Peter talk to compare wiht my 
tagcloud	


For later:
==============
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

