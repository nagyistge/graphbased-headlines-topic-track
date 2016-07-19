#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
######################################
# Author: Nguyen Duc Duy - UNITN
#	BUILD A MODEL FOR NODE MERGING
######################################
import pymongo;
import nltk;
import pickle;
from nltk.stem.lancaster import LancasterStemmer;
from random import shuffle;

lancaster_stemmer = LancasterStemmer();

train_ratio = 0.9; # percentage to take as train set from dev set
"""
def feature_extract_w1w2(w1,w2):	# Extraction feature with simply two word itself
    return {"word1": w1, "word2": w2};
	
def feature_extract_w1s1w2s2(w1,w2):	# Extraction feature with simply two word itself with their suffix
    return {"word1": w1, 'w1suf': w1[-2:], "word2": w2, 'w2suf': w2[-2:]};
	
def feature_extract_w1t1w2t2(w1,w2): # Extraction feature with two words itself with indicator if their first character is capitalized
    return {"word1": w1, "word1_title" : w1.istitle(), "word2": w2, "word2_title" : w2.istitle()};
"""
def feature_extract_w1t1stem1w2t2stem2_true(w1,w2): # Extraction feature with two words itself with indicator if their first character is capitalized
    return {"word1": w1, "word1_title" : w1.istitle(), "stem1" : lancaster_stemmer.stem(w1) ,"word2": w2, "word2_title" : w2.istitle(),"stem2" : lancaster_stemmer.stem(w2), "tag" : True};

def feature_extract_w1t1stem1w2t2stem2_false(w1,w2): # Extraction feature with two words itself with indicator if their first character is capitalized
    return {"word1": w1, "word1_title" : w1.istitle(), "stem1" : lancaster_stemmer.stem(w1) ,"word2": w2, "word2_title" : w2.istitle(),"stem2" : lancaster_stemmer.stem(w2), "tag" : False};
	
from pymongo import MongoClient;
######################################
#	CONST DECLARATION
HOST = 'localhost';			# Host name
PORT = 27017;				# Port
DB_NAME = 'rskills';			# Name of the database
COLLECTION_NAME	 = 'crawleddata';	# Name of the collection
RESULT_COLLECTION_NAME	 = 'modeldata';	# Name of the collection

######################################
#	BODY OF THE PROGRAM
client = MongoClient(HOST, PORT);
db = client[DB_NAME];
col = db[COLLECTION_NAME];
recol = db[RESULT_COLLECTION_NAME];
recol.remove( { } ); #Clear eveything inside result to write new thing...
count = 0;

exceptionsWords = ['a','the','aboard','about','above','across','after','against','along','amid','among','anti','around','as','of','on','at','before','behind','below','beneath','beside','besides','between','beyond','but','by','concerning','considering','despite','down','during','except','excepting','excluding','following','for','from','in','inside','into','like','minus','near','of','off','on','onto','opposite','outside','over','past','per','plus','regarding','round','save','since','than','through','to','toward','towards','under','underneath','unlike','until','up','upon','versus','via','with','within','without'] + nltk.corpus.stopwords.words('english');
stopwords = nltk.corpus.stopwords.words('english');
# get the pointer to all database

for record in col.find(no_cursor_timeout=True):
	count = count + 1;
	words = nltk.word_tokenize(record['content'].encode('ascii', 'ignore'));
	if (len(words)<2): 
		#print "Number of words <2:" + 	str(words);
		continue;
	bigrams = nltk.bigrams(words);
	gramtuples= set([]);
	positive_count=0;
	for gram in bigrams:
		if not(len(gram[0])<6 or len(gram[1])<6 or (gram[0].lower() in exceptionsWords) or (gram[1].lower() in exceptionsWords) or ((gram[0].lower(),gram[1].lower()) in gramtuples)): 
			#print gram[0],str(len(gram[0])),gram[1],str(len(gram[1]));
			recol.insert_one(feature_extract_w1t1stem1w2t2stem2_true(gram[0],gram[1]));
			gramtuples.add((gram[0].lower(),gram[1].lower()));
			positive_count+=1;
	negative_count=0;		
	
	shuffle(words);
	for w1 in words:
		for w2 in words:
			if (w1!=w2 and not((w1,w2) in gramtuples) and not (len(w2)<4 or len(w1)<4 or (w2.lower() in exceptionsWords) or (w1.lower() in exceptionsWords))):
				if ((w1.lower() in exceptionsWords) or (w2.lower() in exceptionsWords)): continue;
				recol.insert_one(feature_extract_w1t1stem1w2t2stem2_false(gram[0],gram[1]));
				negative_count+=1;
				if (positive_count==negative_count): break;
	if (count % 1000) ==0: print str(count) + " items proccessed!"

#print 'Positive: '+ str(count_positive) + '. Negative: ' + str(count_negative);








