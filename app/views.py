from flask import Flask, redirect, url_for, request, render_template
import sqlite3 as sql
import json
import re
from nltk.stem.porter import PorterStemmer
from math import log10
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name


############## RESULTS PAGE FUNCTION TO GENERATE THE MOVIE TITLES ##########
@app.route('/result/<term>')
def result(term):
           
           norm_query= term.split()
           norm_query1 = []
           for data in norm_query:
               data = lowercase(data)
               data = tokenize_non_alpha(data)
               data = stemming_process(data)
               norm_query1.append(data)
           score_dict = get_score(norm_query1)  
           
           con = sql.connect('D:\\csc849\\Project\\GoMovies\\Index\\chinook_corpus.db')
           con.row_factory = sql.Row
           cur = con.cursor()
           
           for key,value in score_dict.items():
               cur.execute( """ UPDATE movies SET tfidf_score = ? WHERE dId = ?""",(value,str(key),))
           
           cur.execute('SELECT * FROM movies  WHERE tfidf_score > 0 ORDER BY tfidf_score DESC')
           rows = cur.fetchall();   
           return render_template("results.html",rows=rows)
    

#########   INDEX PAGE FOR THE APPLICATION ###################
@app.route('/index',methods = ['POST', 'GET'])
def login():
   
   initialise_db()
   
   if request.method == 'POST':
      query = request.form['search']
      return redirect(url_for('result',term = query))
   else:
      query = request.args.get('search')
      return redirect(url_for('result',term = query))

################# HELPER FUNCTIONS START ##############
def lowercase(text):
    return text.lower()
        
def stemming_process(term):
    stemmer = PorterStemmer()
    return stemmer.stem(term)
    
def tokenize_non_alpha( term):
    return re.sub('[^0-9a-zA-Z]+', '', term)

############## HELPER FUNCTIONS END  ############
    
def get_score(query):
    
     ''' computes the tfidf score for the query'''
    
     file = open('D:\\csc849\\Project\\GoMovies\\Index\\positional_inverted_index','r')      
     data = json.load(file)
      
     #tfidf_file = open('tfidf_index','r')      
     #tfidf_data = json.load(tfidf_file)
     
     ranking_dict = {}
     for term in query:
        df = 0
        tf = 0
                
        if term in data.keys():
            
                df =data[term][0]
                idf = log10(len(data)/df)
                for i in data[term][1:]:                
                    tf = i[1]
                    if i[0] not in ranking_dict.keys():
                        ranking_dict[str(i[0])] = tf*idf
                    else:
                        ranking_dict[str(i[0])] += tf*idf 
     return ranking_dict
     
def initialise_db():
        ''' initialise the database so that the initially the tfidf values should be 0'''
    
         con = sql.connect('D:\\csc849\\Project\\GoMovies\\Index\\chinook_corpus.db')
         query = """ UPDATE movies SET tfidf_score = 0"""                                
         cur = con.cursor()
         cur.execute(query)
         
if __name__ == '__main__':
   app.run(debug = True)
