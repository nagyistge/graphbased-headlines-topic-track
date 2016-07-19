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

def feature_extract_w1w2(w1,w2):	# Extraction feature with simply two word itself
    return {"word1": w1, "word2": w2};
	
def feature_extract_w1s1w2s2(w1,w2):	# Extraction feature with simply two word itself with their suffix
    return {"word1": w1, 'w1suf': w1[-2:], "word2": w2, 'w2suf': w2[-2:]};
	
def feature_extract_w1t1w2t2(w1,w2): # Extraction feature with two words itself with indicator if their first character is capitalized
    return {"word1": w1, "word1_title" : w1.istitle(), "word2": w2, "word2_title" : w2.istitle()};

def feature_extract_w1t1stem1w2t2stem2(w1,w2): # Extraction feature with two words itself with indicator if their first character is capitalized
    return {"word1": w1, "word1_title" : w1.istitle(), "stem1" : lancaster_stemmer.stem(w1) ,"word2": w2, "word2_title" : w2.istitle(),"stem2" : lancaster_stemmer.stem(w2)};

	
from pymongo import MongoClient;
######################################
#	CONST DECLARATION
HOST = 'localhost';			# Host name
PORT = 27017;				# Port
DB_NAME = 'rskills';			# Name of the database
COLLECTION_NAME	 = 'crawleddata';	# Name of the collection
RESULT_LOG_COLLECTION_NAME	 = 'resultlog';	# Name of the result log collection
######################################
#	BODY OF THE PROGRAM
client = MongoClient(HOST, PORT);
db = client[DB_NAME];
col = db[COLLECTION_NAME];
# get the pointer to all database
devSetw1w2 = [];
devSetw1s1w2s2 = [];
devSetw1t1w2t2 = [];
devSetw1t1stem1w2t2stem2 = [];
dataSet=[];
count = 0;

# All feature extraction
f_extracted = open('f_extracted.pickle', 'wb'); # File to samve the classifier with word1, word2
f_w1w2 = open('classifierw1w2.pickle', 'wb'); # File to samve the classifier with word1, word2
f_w1t1w2t2 = open('classifierw1s1w2s2.pickle', 'wb'); # File to samve the classifier with word1, suffix of word1, word2, suffix of word2ss
f_w1t1w2t2 = open('classifierw1t1w2t2.pickle', 'wb'); # File to samve the classifier with word1, title of word1, word2, titile of word2ss
f_w1t1stem2w2t2stem2 = open('classifierw1t1stem1w2t2stem2.pickle', 'wb'); # File to samve the classifier with word1, title of word1, stem of word1, word2, titile of word2 and stem of word2
exceptionsWords = ['a','the','aboard','about','above','across','after','against','along','amid','among','anti','around','as','at','before','behind','below','beneath','beside','besides','between','beyond','but','by','concerning','considering','despite','down','during','except','excepting','excluding','following','for','from','in','inside','into','like','minus','near','of','off','on','onto','opposite','outside','over','past','per','plus','regarding','round','save','since','than','through','to','toward','towards','under','underneath','unlike','until','up','upon','versus','via','with','within','without'] + nltk.corpus.stopwords.words('english');
for record in col.find(no_cursor_timeout=True):
	if (len(dataSet) == 536870912) : break;
	count = count + 1;
	words = nltk.word_tokenize(record['content'].encode('ascii', 'ignore'));
	if (len(words)<2): 
		#print "Number of words <2:" + 	str(words);
		continue;
	bigrams = nltk.bigrams(words);
	
	count_positive = 0;
	gramtuples= set([]);
	for gram in bigrams:
		if ((gram[0].lower() in exceptionsWords) or (gram[1].lower() in exceptionsWords)): continue;
		dataSet.append((gram[0],gram[1],True));
		gramtuples.add((gram[0],gram[1]));
		count_positive +=1;
	
	k = int(count_positive/len(words)-1);
	count_negative = 0;
	stop_flag = False;
	for w1 in words:
		if (stop_flag):
			break;
		member_negative = 0;
		for w2 in words:
			if (stop_flag):
				break;
			if (w1!=w2 and not((w1,w2) in gramtuples)):
				if ((w1.lower() in exceptionsWords) or (w2.lower() in exceptionsWords)): continue;
				dataSet.append((w1,w2,False));
				count_negative +=1;
				member_negative +=1;
				if (member_negative == k): break; 
				if (count_negative == count_positive): 
					#stop_flag= True;
					break;
	
	if (count % 1000) ==0: print str(count) + " items proccessed!"

#print 'Positive: '+ str(count_positive) + '. Negative: ' + str(count_negative);

# Suffle train set
shuffle(dataSet);
print 'Data size= ' + str(len(dataSet));
#Save data
pickle.dump(dataSet, f_extracted);
f_extracted.close()
"""
f = open('f_extracted.pickle', 'rb')
dataSet = pickle.load(f);
print 'Load completed'
f.close()
print 'Data size= ' + str(len(dataSet));

# w1,w2
try:
	for w1,w2,label in dataSet:
		if (len(devSetw1w2) == 536870912) : break;
		devSetw1w2.append((feature_extract_w1w2(w1,w2),label));

	cut_point = int(len(devSetw1w2)/train_ratio);
	classifierw1w2 = nltk.DecisionTreeClassifier.train(devSetw1w2[:cut_point]);
	pickle.dump(classifierw1w2, f_w1w2);
	print 'Accuracy of classifierw1w2: ' + str(nltk.classify.accuracy(classifierw1w2, devSetw1w2[cut_point:]));
	devSetw1w2=[];
	f_w1w2.close();
except Exception as inst:
	print inst;




# w1,s1,w2,s2
try:
	for w1,w2,label in dataSet:
		if (len(devSetw1s1w2s2) == 536870912) : break;
		devSetw1s1w2s2.append((feature_extract_w1s1w2s2(w1,w2),label));

	cut_point = int(len(devSetw1s1w2s2)/train_ratio);
	classifierw1s1w2s2 = nltk.DecisionTreeClassifier.train(devSetw1s1w2s2[:cut_point]);
	pickle.dump(classifierw1t1w2s2, f_w1t1w2s2);
	print 'Accuracy of classifierw1s1w2s2: ' + str(nltk.classify.accuracy(classifierw1s1w2s2, devSetw1s1w2s2[cut_point:]));
	devSetw1s1w2s2=[];
	f_w1s1w2s2.close();
except Exception as inst:
	print inst;



# w1,t1,tw,t2
try:
	for w1,w2,label in dataSet:
		if (len(devSetw1t1w2t2) == 536870912) : break;
		devSetw1t1w2t2.append((feature_extract_w1t1w2t2(w1,w2),label));

	cut_point = int(len(devSetw1t1w2t2)/train_ratio);
	classifierw1t1w2t2 = nltk.DecisionTreeClassifier.train(devSetw1t1w2t2[:cut_point]);
	pickle.dump(classifierw1t1w2t2, f_w1t1w2t2);
	devSetw1t1w2t2=[];
	print 'Accuracy of classifierw1t1w2t2: ' + str(nltk.classify.accuracy(classifierw1t1w2t2, devSetw1t1w2t2[cut_point:]));
	f_w1t1w2t2.close();

except Exception as inst:
	print inst;


# w1,t1,stemp1,tw,t2,stemp2
try:
	for w1,w2,label in dataSet:
		if (len(devSetw1t1stem1w2t2stem2) == 536870912) : break;
		devSetw1t1stem1w2t2stem2.append((feature_extract_w1t1stem1w2t2stem2(w1,w2),label));

	cut_point = int(len(devSetw1t1stem1w2t2stem2)/train_ratio);
	classifierw1t1stem1w2t2stemp2 = nltk.DecisionTreeClassifier.train(devSetw1t1stem1w2t2stem2[:cut_point]);
	pickle.dump(classifierw1t1stem1w2t2stemp2, f_w1t1stem2w2t2stem2);
	devSetw1t1stem1w2t2stem2=[];
	print 'Accuracy of classifierw1t1stem1w2t2stemp2: ' + str(nltk.classify.accuracy(classifierw1t1stem1w2t2stemp2, devSetw1t1stem1w2t2stemp2[cut_point:]));
	f_w1t1stem2w2t2stem2.close();
except Exception as inst:
	print inst;











