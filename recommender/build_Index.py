# -*- coding: utf-8 -*-
"""
Created on Thu May  4 23:08:02 2017

@author: soumi
"""
from __future__ import print_function
from __future__ import division
import sqlite3
from sqlite3 import Error
from nltk import word_tokenize,tokenize
import timeit
import numpy as np
import json
import pandas as pd
import re    
from nltk.sentiment.vader import SentimentIntensityAnalyzer    
from nltk.stem.porter import PorterStemmer
import os


class build_Index:
    ''' This class builds all the index for the application'''

    OUTPUT_DIRECTORY = 'D:\\csc849\\Project\\GoMovies\\Index\\'
    
    def __init__(self):
        
        ''' initiliase functions and parameters'''
        self.stemmer = PorterStemmer()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.pos_inv_index = {}
        self.main_index = {}
        self.term_index={}
        self.input = ""
        
        if not os.path.exists(build_Index.OUTPUT_DIRECTORY):
            os.makedirs(build_Index.OUTPUT_DIRECTORY)
            
    def build_Indexes(self):
        ''' This function does the corresponding API calls for all the indexes'''
        
        data_frame = self.build_data_frame()
                        
        sentiment_frame = self.build_sentiment_scores(data_frame)
        
        df2 = self.search(sentiment_frame)
        
        self.build_query_index(df2)
        
        self.sql_schema(df2)
    
        
        
    def build_query_index(self, data_frame):
    
        ''' This API creates the positional inverted index for the corpus data by using
            PANDA's data frame. The data needs to be pre-processed first'''
        title_list = []
        for i in range(0,len(data_frame.title[:])):
            title_list.append(data_frame.title[i])
        
        normalized_list = build_Index.pre_processing(title_list,data_frame) # Pre-process the title index for the movies
    
        df = pd.DataFrame.from_records(normalized_list)

        for i in range(0,len(df)):
         
            for term in (df.loc[i]):
                
              if(term!=None):
                if term not in self.pos_inv_index.keys():
                    doc_freq = 1
                    
                    term_positions = [pos for pos, x in enumerate(normalized_list[i]) if x == term]
                    self.term_index[len(term_positions)] = term_positions 
                    self.pos_inv_index[term] =  [doc_freq,[i,len(term_positions),term_positions]]
              
                else:
                 
                   doc_freq=int(self.pos_inv_index.get(term)[0])+1
                   
                   term_positions = [pos for pos, x in enumerate(normalized_list[i]) if x == term]
                   self.term_index[len(term_positions)] = term_positions 
                   
                   if [i,len(term_positions),term_positions] not in self.pos_inv_index[term]:
                       
                       posting_list = self.pos_inv_index[term] + [[i,len(term_positions),term_positions]]
            
                       posting_list[0] = doc_freq
                       self.pos_inv_index[term] = posting_list
                
            
         #### WRITING THE POSITIONAL INVERTED INDEX ####       
       
      
        with open(build_Index.OUTPUT_DIRECTORY + 'positional_inverted_index', 'w') as outfile:
            json.dump(self.pos_inv_index, outfile)
            
        print("***positional_inverted_index created***")
    
    def build_sentiment_scores(self, data_frame):
        
        ''' This API computes the sentiment score of the reviews by passing it into
        VADER Sentiment analyzer. The noisy reviews are filtered within this fucntion'''
        self.reviews = []
        self.movie_id_list = data_frame.productId.unique()
        self.score = 0
        self.pos_list = []
        self.neg_list = []
        self.neutral_list = []
        self.compound_list = []
        self.compound_mean_list = []
        self.compound_sd_list = []
        self.compound_mean = float(0)
        self.compound_sd = float(0)

        df1 = data_frame.groupby('productId', as_index=False).agg(lambda x: x.tolist())
        df1['lexical_list'] = ''
        for i in df1.text:
            if str(i) == str('nan'):
                print(i,'***')
        i = 0
        for reviews in df1.text:
                self.compound_mean_list = []
                self.compound_sd_list = []
              
                normalized_para = build_Index.pre_process_reviews(reviews)

                for para in normalized_para:

                    self.compound_list = []
                    for sentence in para:
                        self.score = self.get_sentiment_value(sentence)                 # FUCNTION CALL to get sentiment values
                        for sentiment, s_score in self.score.items():
                            if sentiment==str('compound') and s_score != float(0):      # Filtering step to remove reviews whose compound score = 0
                                self.compound_list.append(s_score)
                    self.compound_mean = np.mean(self.compound_list)
                    self.compound_sd = np.std(self.compound_list)
                    
                    '''for i in self.compound_list:
                        if float(self.compound_mean - (2*self.compound_sd))<= float(i) <= float(self.compound_mean + (2*self.compound_sd)):
                            print('\n',self.compound_mean,'---',i,'---',self.compound_sd,'\n')
                            self.compound_mean_list.append(self.compound_mean)
                            self.compound_sd_list.append(self.compound_sd)'''
                            
                    self.compound_mean_list.append(self.compound_mean)
                df1.lexical_list[i] = self.compound_mean_list                   # lexical_list contains the sentimetn scores for the reviews
                i+=1         
        return df1
        
    def build_data_frame(self):
        
        ''' This API builds the PANDA data frame by loading the corpus'''
        
        start_time = timeit.default_timer()
        print("start time : ",start_time)
        infile = open('D:\csc849\Project\GoMovies\corpus\data.txt','r')
        data_frame = pd.read_csv(infile, sep = "|", header=None, names=["productId", "title", "price","userId","profileName","helpfulness","score","time","summary","text"],encoding="utf-8")
        elapsed = timeit.default_timer() - start_time
        print("Time taken in milliseconds: ",elapsed)
        return data_frame

    def pre_processing(self, title_list, data_frame):
    
        ''' This is a preprocessing step for the build_query_index API.'''
        movie_token_list = []
        term = ""
        
        with open("D:\\csc849\\Project\\GoMovies\\corpus\\movie_titles.txt",'w') as outfile:
            for title in data_frame.title:
                outfile.write(str(''.join(title)+'\n'))
        for title in (data_frame.title):
            title = ''.join(title)
            print(title)
            temp_list1 = []
            temp_list2 = []
            title_token_list = word_tokenize(title)
            for token in title_token_list:
                term = self.stemming_process(token)
                temp_list1.append(term)
            for token in temp_list1:
                term = self.lowercase(token)
                term = self.tokenize_non_alpha(term)
                if term != ' ':
                    temp_list2.append(term)

            movie_token_list.append(temp_list2)
        return movie_token_list
    
    ################           HELPER FUCNTIONS START ##########    
    def lowercase(self, text):
        
        return text.lower()
        
    def stemming_process(self, term):
        return self.stemmer.stem(term)
    
    def tokenize_non_alpha(self, term):
        return re.sub('[^0-9a-zA-Z]+', ' ', term)
    
    def tokenize_text_non_alpha(self, term):
        return re.sub("'[^0-9a-zA-Z]+", ' ', term)
    
    ###############        HELPER FUNCTIONS END ##############
    
    def pre_process_reviews(self,text):    
        
        ''' Pre-process the reviews by converting paras to sentences and implement
        case normalization'''
        main_list = []
        normalized_text = []
        para_list = []
        
        for para in text:
            para_list = [] 
            for sentence in [para]:
                main_list  =[]
                try:
                    string_list = tokenize.sent_tokenize(sentence)
                except TypeError as e:
                    continue
                for sentence in string_list: 
                    sentence = self.tokenize_text_non_alpha(sentence)
                    if sentence != ' ':
                        main_list.append(sentence)  
                normalized_text.append(main_list)
       
            para_list.append(normalized_text)
        return normalized_text
    
    ### VADER SENTIMENT ANALYZER ####
    
    def get_sentiment_value(self,sentence):
        
        score = self.sentiment_analyzer.polarity_scores(sentence)      # API TO GET SENTIMENT VALUE_ VADER
        return score
      
    ####                      ##########
    
    def search(self, df2):
        
        '''checks for the lexical_list in dataframe'''
        df2['sentiment_score'] = ''
        df2['title_norm'] = ''
            
        for i in range(0,len(df2)):
            df2.title[i] = set(df2.title[i])
        
        for i in range(0,len(df2)):
   
            df2.sentiment_score[i] = sum(df2.lexical_list[i])/len(df2.lexical_list[i])
           
            df2.title_norm[i] = set(x.lower() for x in df2.title[i])         
        return df2
        
        
    def get_tfidf_score(self,term):
        
        ''' function to obtain tfidf score'''
        self.file = open('positional_inverted_index','r')
        self.data = json.load(self.file)
        
        if term in self.data.keys():
            for posting_list in self.data[term]:
                self.df = posting_list[0]
       
        
        
    ####################### DATABASE FUNCTIONS ########################    
       
    def create_connection(self,db_file):
        
        ''' start the SQLITE database '''
        try:
            
            self.conn = sqlite3.connect(db_file)
            return self.conn
        except Error as e:
            print(e)
        
        return None    
            
    def create_table(self,conn, create_table_sql):
        ''' create the table'''

        try:
            self.c = conn.cursor()
            self.c.execute(create_table_sql)
        except Error as e:
            print(e)
            
    def create_movie_db(self,conn,movie):        
        
        ''' create teh movies table in database'''
            
        self.sql =  """ INSERT INTO movies(productId, title_norm, title, summary, sentiment_score,dId,tfidf_score)
                                VALUES(?,?,?,?,?,?,?)"""
                                
        cur = conn.cursor() 
        try:
            cur.execute(self.sql, movie) 
        except Error as e:    
            print(movie)
            print(e)
        return cur.lastrowid            
            
    def sql_schema(self,df2):
        
        ''' Database Schema definition and function calls are made in this API'''
        
        df2['dId']=0
        df2.dId = df2.index 
        
        df2['tfidf_score'] = float(0)
        df2.tfidf_score = float(0)   
        
        self.database = build_Index.OUTPUT_DIRECTORY+"chinook_corpus.db"
        
        sql_movie_table= """ CREATE TABLE IF NOT EXISTS 
                                                movies(
                                                        productId varchar[50] NOT NULL,
                                                        title_norm text NOT NULL,
                                                        title text NOT NULL,
                                                        summary text,
                                                        sentiment_score float,
                                                        dId text PRIMARY KEY,
                                                        tfidf_score float);"""
                                                
        sql_tweet_table = """ CREATE TABLE IF NOT EXISTS 
                                               tweets(
                                                        tweetId integer NOT NULL,
                                                        productId text NOT NULL,
                                                        title text NOT NULL,
                                                        tweet text,
                                                        FOREIGN KEY (tweetId) REFERENCES movies (docId));"""
                                               
                                                
        self.conn = self.create_connection(self.database)
        
        if self.conn is not None:
            # create movies table
            self.create_table(self.conn, sql_movie_table)
            # create tweet table
            self.create_table(self.conn, sql_tweet_table)
            
        
        else:
            print("Error! cannot create the database connection.")    

                                            
        
        with self.conn:
            for i in range(0,len(df2)):
                self.movie = (df2.productId[i],str(list(df2.title_norm[i])[0]),str(list(df2.title[i])[0]),str(list(df2.summary[i])[0]),df2.sentiment_score[i],str(df2.dId[i]),df2.tfidf_score[i])            
                #self.movie = (df2.dId[i],df2.productId[i],str(list(df2.title_norm[i])[0]),str(list(df2.title[i])[0]),str(list(df2.summary[i])[0]),str(list(df2.score[i])[0]),df2.sentiment_score[i])  
                self.create_movie_db(self.conn, self.movie)
            
        self.conn.close()  
        
        ############# DATABASE FUCNTIONS ENDS ##################
        
def main():
    
    print("YO")
    
if __name__ == '__main__':
    
    build_Index = build_Index()
    build_Index.build_Indexes()
    