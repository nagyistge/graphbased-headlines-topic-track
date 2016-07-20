######################################
# Author: Nguyen Duc Duy - UNITN
#
# Implement node for Graph
# Properties:
# - word;
# -	wfreq;
# - timeAdded
# Methods:
# - __init__: 2 constructor
# - isDump
# - setValue
# - increaseFreq
# - setwfreq
# - resetTime
# - getWord
# - getfreq
# - gettimeAdded
# - setTime
# - toString
######################################

from datetime import datetime;
#import time;

class Node:
	word = "";
	wfreq=0;
	timeAdded="";
	
	def __init__(self,w,fre):
		self.word = w;
		self.wfreq = fre;
		self.timeAdded = datetime.now();
	
	def __init__(self,w):
		self.word = w;
		self.wfreq = 1;
		self.timeAdded = datetime.now();
	
	def isDump(self):
		if (self.word == "" or self.wfreq==0): 
			return True;
		else: 
			return False;
		
	def setValue(self,w,fre):
		self.word = w;
		self.wfreq = fre;
		self.timeAdded = datetime.now();
	
#	def increaseFreq(self):
#		self.wfreq += 1;
		
	def increaseFreq(self,n):
		self.wfreq += n;
		
	def setwfreq(self,n):
		self.wfreq = n;
		
	def setTime(self,t):
		self.timeAdded = t;
		
	def resetTime(self):
		self.timeAdded = datetime.now();
	
	def getWord(self):
		return self.word;
		
	def getfreq(self):
		return self.wfreq;
		
	def gettimeAdded(self):
		return self.timeAdded;
		
	def toString(self):
		return '[w= "' + self.word + '" | freq= ' + str(self.wfreq) + ' | timeAdded= ' + str(self.timeAdded)+ ']';

# TEST
#n = Node("see");
#print n.toString();
#print n.isDump();
#n.setValue("saw",10);
#print n.toString();
#print n.isDump();
#n.increaseFreq();
#print n.toString();
#n.increaseFreq(2);
#print n.toString();
#n.setwfreq(3);
#print n.toString();
#time.sleep(10);
#n.resetTime();
#print n.toString();
#print n.getWord();
#print n.getwfreq();
#print n.gettimeAdded();