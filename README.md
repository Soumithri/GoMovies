# GoMovies
GoMovies is a movie recommendation system that uses TF IDF to rank the results and VADER sentiment analyzer to compute the sentiment scores.
To Run this application, please do the following steps:
1) Download the Flask library into the root folder of the application ("../GoMovies/")
2) Copy and paste your dataset into the corpus directory. Note that the data set should be a csv file seperated by '|' pipe symbol. Change the delimiter for other files if needed.
3) Change the appropriate absolute file paths of the created indices and data file in the python files: build_Index.py , search.py, views.py 
4) Run the build_Index.py
5) Run the search.py
6) Run the views.py
7) A basic web UI appears. Enter the query and click submit button. It returns the list of top most relevant document.
8) HAPPY SEARCHING :)
