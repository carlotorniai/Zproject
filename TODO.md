TO DO:

- Finish the method to return the dummy feature matrixces
  -> in stats_fromDB.py
- DO hierarchical clustering (ok not really meaningful..)
	-> Ways to evaluate?

- Do some initial k-means and analysis
	-> ok done wiht a small set of features.
	-> WOrk on clusterign evaluation

	1) FInd the point closer to the center for each clusters.
	-> try to understand the difference in features.

	2) Try to find some meaninful "measure" of
	goodness
	-> Try http://stackoverflow.com/questions/12680038/validating-output-from-a-clustering-algorithm




- If there is time do the plotting for the data and
	-> Do some data QA : testing on education comapred to the real data

Write down a New iPython with stats and plot.
- Plot the top 40 Skills listed
- Plot the Phd . MS and TOpc 
- Plot the frequency of the Job title (for current positions)


Tonight:
- Just plot the data AND do the bag of works as a
tag cloud and see hwo similar is to Peter one.



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

