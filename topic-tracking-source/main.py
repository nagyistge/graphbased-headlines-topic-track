#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
######################################
# Author: Nguyen Duc Duy - UNITN
#	THE MAIN BIG BOY
######################################
from functions import *;
from Graph import Graph;
from time import sleep;
from datetime import datetime;
from datetime import timedelta;
import sys;
from pymongo import MongoClient;
import threading;
from sets import Set;
from nltk.stem import WordNetLemmatizer;
import pickle;

######################################
#	CONST DECLARATION
HOST = 'localhost';			# Host name
PORT = 27017;				# Port
DB_NAME = 'rskills';			# Name of the database
COLLECTION_NAME	 = 'crawleddata';	# Name of the collection
LOG_COLLECTION_NAME	 = 'commandlog';	# Name of the log collection
RESULT_LOG_COLLECTION_NAME	 = 'resultlog';	# Name of the result log collection
QUERY_START_TIME = datetime(2015, 10, 14, 16, 0, 0, 0);	# The time to start query from (the CRAWLED TIME)
DELTA_TIME = timedelta(minutes=60);									# Deltatime, so query will get data from QUERY_START_TIME yo QUERY_START_TIME + DELTA_TIME
STARTING_PRUNNING_PREVENTION_BIAS = 0;  #At the beginning corpust, freq of edge and node always be low, so we put a bias to disregard prunning at the beginning
#MAXIMUM_NUMBER_OF_CORPUS = 1000; #Maximum number of corpus to be process. This is the Hard-breaking point of the program
MAXIMUM_NUMBER_OF_CORPUS = 999999999999999; #Maximum number of corpus to be process. This is the Hard-breaking point of the program

######################################
#	BODY OF THE PROGRAM
client = MongoClient(HOST, PORT);
db = client[DB_NAME];
col = db[COLLECTION_NAME];
collog = db[LOG_COLLECTION_NAME];
collog.remove( { } ); #Clear eveything inside collog to write new thing...
colresultlog = db[RESULT_LOG_COLLECTION_NAME];
colresultlog.remove( { } ); #Clear eveything inside result log to write new thing...
print 'Connections establshed!';
g = Graph([],[]);
current_time = QUERY_START_TIME;	# time point to start querying
count = 0;
tagger = BuildTagger(); # Build a tagger 
wordnet_lemmatizer = WordNetLemmatizer();

while (current_time < datetime.now()):
	start_time = time.time();
	print "[!] Enter time point 0 - Begin:" + str(time.time() - start_time);
	block = [];			# Block of all collected records
	count +=1;
	
	print '####################### \nEntered corpus number ' + str(count) + ':-)';
	#sys.stdout.write('####################### \nEntered corpus number ' + str(count) + ':-)' + '\n');
	print ' - Start query from DB...';
	#sys.stdout.write(' - Start query from DB...' + '\n');
	
	recCount=0;
	for record in col.find({"time": {"$gt": current_time, "$lt": current_time + DELTA_TIME}}):
		block.append(record);
	print "Query statement: from" + str(current_time) + " to " + str(current_time + DELTA_TIME);
	print "[!] Enter time point 1 - Enter Mashing:" + str(time.time() - start_time);	
	tup = TextMasher(block,tagger,wordnet_lemmatizer);
	# Load classifier for merging nodes
	f = open('my_classifier.pickle', 'rb')
	classifier = pickle.load(f)
	f.close()
	# Enter merging
	tup = MergeDuplicate(tup[0],tup[1],wordnet_lemmatizer);
	tup = BigramNodeMerge(tup[0],tup[1],classifier);
	print '   + Merging completed!';
	print "[!] Enter time point 2 - Finish Mashing:" + str(time.time() - start_time);
	print '   + Mashing completed!';
	print "[!] Enter time point 3 - Enter add node/edge:" + str(time.time() - start_time);
	g.AddNodes(tup[0],collog); 	# A connection to log
	g.AddEdges(tup[1],collog);	# A connection to log
	print "[!] Enter time point 4 - Finish add node/edge:" + str(time.time() - start_time);
	print '   + ' + str(len(tup[0])) + ' nodes and ' + str(len(tup[1])) + ' edges added.';
	#	sys.stdout.write();
	print ' - Start prettify the graph...';
	print "[!] Enter time point 5 - Enter Prunning:" + str(time.time() - start_time);
	if (count>STARTING_PRUNNING_PREVENTION_BIAS):  # a bias to avoid "early birds" to be removed
		GraphPrunning(g,collog);
		print '   + Well, it is beautiful now!';
	else:
		print '   + Prunning skipped! Due to staring bias...';
	current_time = current_time + DELTA_TIME;
	print 'Finished corpus number ' + str(count) + ';)';
	print "[!] Enter time point 6 - Finished Prunning:" + str(time.time() - start_time);
	if (count == MAXIMUM_NUMBER_OF_CORPUS): break;
	
	g.printNodes();
	g.printEdges();
	print "[!] Enter time point 7 - End corpus:" + str(time.time() - start_time);
	## Record to result log collection
	colresultlog.insert_one({'timestamp': datetime.now(), 'nodes' : json.dumps(g.GetNodesSTRwithFreq()), 'edges' : json.dumps(g.GetEdgeSTRwithFreq())});
	print "\n\n";
	#sys.stdout.write("\n\n" + '\n');
	#sys.stdout.flush()

print "\n Final result: ";
g.printNodes();
g.printEdges();