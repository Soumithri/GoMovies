# -*- coding: utf-8 -*-
"""
Created on Mon May  8 22:48:34 2017

@author: soumi
"""
import json
from nltk.stem.porter import PorterStemmer 
import re
from math import log10
import os

def create_vocabulary():
    
    ''' Creates the vocabulary list for the application '''
    infile = open('D:\csc849\Project\GoMovies\\Index\positional_inverted_index','r')
    DIRECTORY = 'D:\\csc849\\Project\\GoMovies\\corpus\\'

    if not os.path.exists(DIRECTORY):
      os.makedirs(DIRECTORY)
    with open(DIRECTORY + 'vocab.txt', 'w') as outfile:  
        data = json.load(infile)
        for key in data.keys():
            outfile.write(str(key+"\n"))
    print('vocab.txt created in corpus folder...')
    infile.close()
    outfile.close()
    
def query():
    
    ''' Main method that writes vocabulary into a file and creates the tf idf index'''
    
    OUTPUT_DIRECTORY = "D:\\csc849\\Project\\GoMovies\\Index\\"
    
    if not os.path.exists(OUTPUT_DIRECTORY):
      os.makedirs(OUTPUT_DIRECTORY)
    create_vocabulary()
    inputfile = open('D:\\csc849\\Project\\GoMovies\\corpus\\vocab.txt','r')
    vocab_list = []
    tfidf_dict = {}
    for i in inputfile:
        vocab_list.append(i.strip())
    inputfile.close()
    for term in vocab_list:
        tfidf_dict[term]= get_tf_idf_score(term)
        
    with open(OUTPUT_DIRECTORY+ 'tfidf_index', 'w') as outfile:
            json.dump(tfidf_dict, outfile)
    outfile.close()
    print('*** tfidf index created ***')   

###  NOT IMPLEMENTED YET #####      
def check_proximity(query_list):
    
    print()
    
#### HELPER FUNCTIONs START #########    

def lowercase(text):
    return text.lower()
        
def stemming_process(term):
    stemmer = PorterStemmer()
    return stemmer.stem(term)
    
def tokenize_non_alpha( term):
    return re.sub('[^0-9a-zA-Z]+', '', term)

##### HELPER FUNCTIONS END ######

def get_tf_idf_score(term):
    
    ''' compute the tf-idf score for the vocabulalry'''
    file = open('D:\\csc849\\Project\\GoMovies\\Index\\positional_inverted_index','r')
    data = json.load(file)
    ranking_dict = {}
    df = 0
    tf = 0
    doc_list = []
        
    if term in data.keys():
            for p in data[term][1:]:
                doc_list.append(p)            
    if term in data.keys():            
                doc_list = []
                df = data[term][0]
                idf = log10(len(data)/df)                
                for i in data[term][1:]:                
                    tf = i[1]
                    if i[0] not in ranking_dict.keys():
                        ranking_dict[i[0]] = tf*idf
                    else:
                        ranking_dict[i[0]] += tf*idf        
    for k in range(1,len(data)):
             if k not in ranking_dict.keys():
                 ranking_dict[k] = float(0)    
    return ranking_dict

query()