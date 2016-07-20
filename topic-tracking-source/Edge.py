######################################
# Author: Nguyen Duc Duy - UNITN
#
# Implement edge for Graph
# Properties:
# - word0;
# - word1;
# -	efreq;
# - timeAdded
# Methods:
# - __init__: 2 constructor
# - isDump
# - setValue
# - increaseFreq
# - setefreq
# - setTime
# - resetTime
# - getWords
# - getword0
# - getword1
# - getfreq
# - gettimeAdded
# - toString
######################################

from datetime import datetime;
from re import sub;
from nltk import word_tokenize;

class Edge:
	word0 = "";
	word1 = "";
	efreq=0;
	timeAdded="";
	
	def __init__(self,w0,w1,fre):
		self.word0 = w0;
		self.word1 = w1;
		self.wfreq = fre;
		self.timeAdded = datetime.now();
	
	def __init__(self,w0,w1):
		self.word0 = w0;
		self.word1 = w1;
		self.efreq = 1;
		self.timeAdded = datetime.now();
	
	def __init__(self,ws):
		ws.encode('ascii', 'ignore');
		tks = word_tokenize(sub(r'[^\w\s]', '', ws.strip()));
		#print ws;
		
		if  (len(tks)>2): print "Warning! Found Tupple size > 2 while adding edge! Keep 2 fist items by default."
		elif (not (len(tks)==2)):
			print "Warning! Found Tupple size < 2. Error encounted!"
		else:	
			#print tks;
			self.word0 = tks[0];
			self.word1 = tks[1];
			self.efreq = 1;
			self.timeAdded = datetime.now();
	
	
#	def __init__(self,tup):
#		self.word0 = tup[0];
#		self.word1 = tup[1];
#		self.efreq = 1;
#		self.timeAdded = datetime.now();
		
	def isDump(self):
		if (self.word0 == "" or self.word1 == "" or self.efreq==0): 
			return True;
		else: 
			return False;
		
	def setValue(self,w0,w1,fre):
		self.word0 = w0;
		self.word1 = w1;
		self.efreq = fre;
		self.timeAdded = datetime.now();
	
#	def increaseFreq(self):
#		self.wfreq += 1;
		
	def increaseFreq(self,n):
		self.efreq += n;
		
	def setefreq(self,n):
		self.efreq = n;
		
	def setTime(self,t):
		self.timeAdded = t;	
		
	def resetTime(self):
		self.timeAdded = datetime.now();
	
	def getWords(self):
		return (self.word0,self.word1);
	
	def getword0(self):
		return self.word0;

	def getword1(self):
		return self.word1;
		
	def getfreq(self):
		return self.efreq;
		
	def gettimeAdded(self):
		return self.timeAdded;
		
	def toString(self):
		return '[e= (' + self.word0 +  ',' + self.word1 + ') | freq= ' + str(self.efreq) + ' | timeAdded= ' + str(self.timeAdded)+ ']';

# TEST
#e = Edge("see","you");
#print e.toString();
#print e.isDump();
#e.setValue("saw","him",10);
#print e.toString();
#print e.isDump();
#e.increaseFreq(2);
#print e.toString();
#e.setefreq(3);
#print e.toString();
#time.sleep(10);
#e.resetTime();
#print e.toString();
#print e.getWords();
#print e.getword0();
#print e.getword1();
#print e.getfreq();
#print e.gettimeAdded();