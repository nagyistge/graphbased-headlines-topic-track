#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
######################################
# Author: Nguyen Duc Duy - UNITN
#
# Implement node for Graph
# Properties:
# - nodes: set of elements in NODE type
# - edges: set of elements in Edge type
# -	nodesStr: set of all "label" or "words" of nodes, in String type;
# -	edgesTup: set of all pair of "words" in edges, in Tuple type;
# - timeAdded
# Methods:
# - __init__: 1 constructor, param can be set OR list
# - isDump
# - updateNodeEdgeList: pour all words in nodes to nodesStr (Node to str), pour all words in edges to edgesTup (Edges to tuple)
# - AddNode: add a node to graph. It could be a object in Node type OR a String
# - AddEdge: add a edge to graph. It could be a object in Edge type OR a String consists of 2 words seperated by " " (space)
# - AddNodes: add multiple nodes
# - AddEdges: add multiple edges 
# - RemoveNode: remove a single node (no refine applied)
# - RemoveEdge: remove a single edge (no refine applied)
# - RemoveNodes: remove a list/set of nodes (refine applied)
# - RemoveEdges: remove a list/set of edges (refine applied)
# - GraphRefine: self-refine the graph
# - GetNodes: return a set of Nodes
# - GetEdges: return a set of Edges
# - GetNodesSTR: return set of STRING, contains word of node
# - GetEdgesTUP: return set of TUPLE, contain word pair of edge
# - toString: Print statistics about graph
# - printNodes: print all nodes
# - printEdges: print all edges
# - isSteady: return true if there are no isolated nodes, odd edges
######################################

from Node import Node;
from Edge import Edge;
from re import sub;
from sets import Set;
from datetime import datetime;
import json;

class Graph:
	nodes = Set([]);
	edges = Set([]);
	nodesStr = Set([]);
	edgesTup = Set([]);
	
	def __init__(self,ns,ed): # Only init from  list of nodes and edges
		if (type(ns) == type(Set([]))): # param is a set
			self.nodes = ns;	# direct assign
		else:							# might be a list
			self.nodes = Set(ns);
			
		if (type(ed) == type(Set([]))): # param is a set
			self.edges = ed;	# direct assign
		else:							# might be a list
			self.edges = Set(ed);	
		
		self.updateNodeEdgeList();
			
	def isDump(self):
		if (len(self.nodes) == 0 or len(self.edges) == 0  or len(self.nodesStr) == 0  or len(self.edgesTup) == 0 ): 
			return True;
		else: 
			return False;
		
	def updateNodeEdgeList(self):
		for n in self.nodes:
			self.nodesStr.add(n.getWord());
		for e in self.edges:
			self.edgesTup.add(e.getWords());
	
	def AddNode(self,newNode,logCollection):
		if (type(newNode) == type(Node("be"))): #a Type of Node
			#Check if node is not arealy exist
			if (not(newNode.getWord() in self.nodesStr)):
				self.nodes.add(newNode);							# Freq and Time are also transfered
				self.nodesStr.add(newNode.getWord());
			else: # Find and update the exist one
				node="";
				for node in self.nodes:
					if (node.getWord() == newNode.getWord()): # found the word
						newNode.increaseFreq(node.getfreq());
						newNode.resetTime();
						break;
				self.nodes.remove(node);
				self.nodes.add(newNode);
				
			logCollection.insert_one({'action':'addNode', 'data':newNode.getWord(), 'timestamp': datetime.now()});		# Write log
			
		else: # a string
			nNode = Node(sub(r'[^\w\s]', '', newNode.strip())); # make a new node
			self.AddNode(nNode,logCollection);
			#Call back itself
			
	def AddEdge(self,newEdge,logCollection):
		if (type(newEdge) == type(Edge("to be"))): # a Type of Edge 
			if (not(newEdge.getWords() in self.edgesTup)):
				self.edges.add(newEdge);							# Freq and Time are also transfered
				self.edgesTup.add(newEdge.getWords());
			else: # Find and update the exist one
				edge="";
				for edge in self.edges:
					if (edge.getWords() == newEdge.getWords()): # found the word
						newEdge.increaseFreq(edge.getfreq());
						newEdge.resetTime();
						break;
				self.edges.remove(edge);
				self.edges.add(newEdge);
#		elif (type(newEdge) == type(("to","be"))): # a Tuple
#			self.nodes.add(Edge(newEdge));					# Freq and Time ARE NOT transfered
			logCollection.insert_one({'action':'addEdge', 'data': str(newEdge.getword0() + ' ' + newEdge.getword1()), 'timestamp': datetime.now()});		# Write log
		
		else:									# A text, type: word1[space]word2
			#tup = tuple(sub(r'[^\w\s]', '', newEdge.strip()).split());
			#if  (len(tup)>2): print "Warning! Found Tupple size > 2 while adding edge! Keep 2 fist items by default."
			nEdge = Edge(newEdge);
			if not(nEdge.isDump()):
				self.AddEdge(nEdge,logCollection);
	
	def AddNodes(self,newnodes,logCollection): #add multiple nodes from a SET of LIST of STRINGS or NODES
		for node in newnodes:
			self.AddNode(node,logCollection);
	
	def AddEdges(self,newedges,logCollection): #add multiple nodes from a SET of LIST of STRINGS or EDGES
		for edge in newedges:
			self.AddEdge(edge,logCollection);
	
	def RemoveNode(self,elNode,logCollection): #Warning! This just remove the single node itself, all reated edges must be remove in GraphRefine
		if (type(elNode) == type(Node("be"))): #a Type of Node
			#Check if node is not arealy exist
			word = elNode.getWord();
			if (word in self.nodesStr):
				node="";
				for node in self.nodes:
					if (word == node.getWord()): # found the word
						self.nodes.remove(node);
						self.nodesStr.remove(word);
						logCollection.insert_one({'action':'removeNode', 'data':word, 'timestamp': datetime.now()});		# Write log
						break;
			# Not exist, do nothing			
		else: # a string
			nNode = Node(sub(r'[^\w\s]', '', elNode.strip())); # make a new node
			self.RemoveNode(nNode,logCollection);
			#Call back itself
	
	def RemoveEdge(self,elEdge,logCollection): #Warning! This just remove the single node itself, all reated edges must be remove in GraphRefine
		if (type(elEdge) == type(Edge("be you"))): #a Type of Node
			#Check elEdge node is not arealy exist
			words = elEdge.getWords();
			if (words in self.edgesTup):
				edge="";
				for edge in self.edges:
					if (words == edge.getWords()): # found the word tuple
						self.edges.remove(edge);
						self.edgesTup.remove(words);
						logCollection.insert_one({'action':'removeEdge', 'data': str(words[0] + ' ' + words[1]), 'timestamp': datetime.now()});		# Write log
						break;
			# Not exist, do nothing
		else: # a string
			#tup = tuple(sub(r'[^\w\s]', '', newEdge.strip()).split());
			#if  (len(tup)>2): print "Warning! Found Tupple size > 2 while adding edge! Keep 2 fist items by default."
			elEdge = Edge(elEdge);		
			self.RemoveEdge(elEdge,logCollection);
			#Call back itself
	
	
	
	def RemoveNodes(self,lsNodes,logCollection):
		for nd in lsNodes:
			self.RemoveNode(nd,logCollection);
		self.GraphRefine(logCollection);

	def RemoveEdges(self,lsEdges,logCollection):
		for ed in lsEdges:
			self.RemoveEdge(ed,logCollection);
		self.GraphRefine(logCollection);

	def GraphRefine(self,logCollection):
		# Remove isolated points
		nodeWords = self.nodesStr;
		edgeWords = Set([e[0] for e in self.edgesTup]) | Set([e[1] for e in self.edgesTup]);
		isolatedNodes = nodeWords - edgeWords;
		if (len(isolatedNodes)>0):
			self.RemoveNodes(isolatedNodes,logCollection);
		#Remove edges whose w1 or w2 is not in list of node
		elEdges = [];
		for edge in self.edges:
			words = edge.getWords();
			if (not(words[0] in self.nodesStr) or not(words[1] in self.nodesStr)):
				elEdges.append(edge);
		for edge in elEdges:
			self.RemoveEdge(edge,logCollection);

	def GetNodes(self):
		return self.nodes;

	def GetEdges(self):
		return self.edges;
		
	def GetNodesSTR(self):
		return self.nodesStr;
	
	def GetNodesSTRwithFreq(self):
		rs=[];
		for node in self.nodes:
			rs.append(node.getWord()+':'+str(node.getfreq()));
		return rs;
	
	def GetEdgesTUP(self):
		return self.edgesTup;
	
	def GetEdgeSTRwithFreq(self):
		rs=[];
		for edge in self.edges:
			rs.append(edge.getword0()+ ' ' + edge.getword1() +':'+str(edge.getfreq()));
		return rs;
		
	def toString(self):
		return '[Num of nodes= ' + str(len(self.nodes)) + ' | Num of edges= ' + str(len(self.edges)) + ']';
		
	def printNodes(self):
		print "Node: ",;
		for n in self.nodes:
			print n.getWord().encode('utf-8') + '->' + str(n.getfreq())+ ', ',;
		print 
	
	def printEdges(self):
		print "Edges: ",;
		for e in self.edges:
			print str(e.getWords()).encode('utf-8') + '->' + str(e.getfreq())+ ', ',;
		print 

	def isSteady(self):
		res = True;
		nodeWords = self.nodesStr;
		edgeWords = Set([e[0] for e in self.edgesTup]) | Set([e[1] for e in self.edgesTup]);
		# Check if any words in edges is not in Node set
		if (not(nodeWords >= edgeWords)): 
			res = False;
			print 'Warning! There is(are) word(s) in Edge set not exist in Node set. They are: ' + str(edgeWords - nodeWords);
		# Check if there are any isolated node
		isolatedNodes = nodeWords - edgeWords;
		if (len(isolatedNodes)>0):
			res = False;
			print 'Warning! Isolated node(s) found. They are: ' + str(isolatedNodes);
		# Check if number of edge <= n(n − 1)/2  where n is number of Node. See https://en.wikipedia.org/wiki/Complete_graph
		n = len(nodeWords);
		if (len(self.edges) > len(nodeWords)):
			res = False;
			print 'Warning! Number of edges exceeded maximum of full graph.';
			
		return res;

	
######################################		
# TEST
#n1 = Node("see_s");
#n2 = Node("you");
#e = Edge("see you");
#g = Graph(Set([n1,n2]),Set([e]));
#print g.toString();
#g.printNodes();
#g.printEdges();
#print g.isDump();
#g.AddNode('is');
#g.AddNode('you');
#n3 = Node('a');
#g.AddNode(n3);
#g.AddEdge('.ques % you');
#g.AddEdge('.ques % you');
#print g.toString();
#g.printNodes();
#g.printEdges();
#print g.toString();
#print str(g.GetNodesSTR());
#print str(g.GetEdgesTUP());
#print g.isSteady();
#for no in g.GetNodes():
#	print no.toString();
#for ed in g.GetEdges():
#	print ed.toString();
#print;
#g.AddNodes([Node('he'),Node('she')]);
#g.AddEdges([Edge('he be'),Edge('see you')]);
#g.RemoveEdge('.ques % you');
#g.RemoveNode('see');
#for no in g.GetNodes():
#	print no.toString();
#for ed in g.GetEdges():
#	print ed.toString();
#print g.isSteady();
#g.RemoveNodes([Node('he'),Node('she')]);
#g.RemoveEdges([Edge('he_s be'),Edge('see you')]);
#for no in g.GetNodes():
#	print no.toString();
#for ed in g.GetEdges():
#	print ed.toString();
#print g.isSteady();
#print;
#g.AddNodes([Node('he'),Node('be')])
#g.GraphRefine();
#g.printNodes();
#g.printEdges();
#print g.isSteady();