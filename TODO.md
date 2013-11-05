TO DO:


- Add the multiindex search on the skills
http://docs.mongodb.org/manual/tutorial/model-data-for-keyword-search/
How to do that:
db.ext_profiles_education_ds.ensureIndex( { skills: 1 } )


- Do some data QA : testing on education comapred to the real data.

Write down a New iPython with stats and plot.
- Plot the top 40 Skills listed
- Plot the Phd . MS and TOpc 
- Plot the frequency of the Job title (for current positions)

- Tomorrow dive into ierarchical clustering.



Tonight:
- Read about Linkeidn and the social web.
http://nbviewer.ipython.org/urls/raw.github.com/ptwobrussell/Mining-the-Social-Web-2nd-Edition/master/ipynb/Chapter%203%20-%20Mining%20LinkedIn.ipynb




For later:
==============

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

