# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 13:45:07 2017

@author: soumi
"""

def get_data(string):
    
    ''' Get the original string and convert it into a list'''
    inputfile = open("Movies_&_TV.txt","r")
    data_list = []
    for line in inputfile:
        if string in line:

                data_list.append(line[line.index(':')+1:])        
    inputfile.close()
    return data_list
    
def main():
    
    ''' main method to parse the data'''
    productId = []
    title = []
    price = []
    userId = []
    profilename = []
    helpfullness = []
    score = []
    time = []
    summary = []
    text = []
    
    productId = get_data('product/productId')
    title = get_data('product/title')
    price = get_data('product/price:')
    userId = get_data('review/userId')
    profilename = get_data(str('review/profileName'))
    helpfullness = get_data(str('review/helpfulness'))
    score = get_data(str('review/score'))
    time = get_data(str('review/time'))
    summary = get_data(str('review/summary'))
    text = get_data(str('review/text'))
    
    ### WRITING INTO FILES #####
    print(productId[0][1:-1])
    print(len(productId),len(title),len(price),len(userId),len(profilename),len(helpfullness),len(score),len(time),len(summary),len(text))
    outfile = open("data.txt",'w')
    outfile1 = open("data_without_review.txt",'w')
    outfile.write((str("productId")+"|"+str("title")+"|"+str("price")+"|"+str("userId")+"|"+str("profileName")+"|"+str("helpfulness")+"|"+str("score")+"|"+str("time")+"|"+str("summary")+"|"+str("text")+"\n"))
    outfile1.write((str("productId")+"|"+str("title")+"|"+str("price")+"|"+str("userId")+"|"+str("profileName")+"|"+str("helpfulness")+"|"+str("score")+"|"+str("time")+"\n"))
                   
    for i in range(0,len(productId)):
        outfile.write((str((productId[i])[1:-1])+"|"+str((title[i])[1:-1])+"|"+str((price[i])[1:-1])+"|"+str((userId[i])[1:-1])+"|"+str((profilename[i])[1:-1])+"|"+str((helpfullness[i])[1:-1])+"|"+str((score[i])[1:-1])+"|"+str((time[i])[1:-1])+"|"+str((summary[i])[1:-1])+"|"+str((text[i])[1:-1])+"\n"))
        outfile1.write((str((productId[i])[1:-1])+"|"+str((title[i])[1:-1])+"|"+str((price[i])[1:-1])+"|"+str((userId[i])[1:-1])+"|"+str((profilename[i])[1:-1])+"|"+str((helpfullness[i])[1:-1])+"|"+str((score[i])[1:-1])+"|"+str((time[i])[1:-1])+"\n"))
    outfile.close()
    outfile1.close()
main()
    
