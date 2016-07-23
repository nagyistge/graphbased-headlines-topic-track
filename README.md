# GRAPHBASED HEADLINES TOPIC TRACK
Project of UNITN subject: Computational skills for text analysis. In this project, I build a program that analysis the news headlines collected in the internet (see open heading corpus). Outcome of the system is a topic modeling method with the graph representation.
# What is in the source pack
In this code package, you will find the following modules:
- propernoun-model-build: module to build classifier to identify sequences of proper noun/name. Mostly based on keyword as a unit of meaning, there are situation that proper noun/name consists of two words. So the classifier try to merge them together, leaning from the big data corpus.
- topic-tracking-source: this is the primary part of the package. This module query headlines from the database, processes it, then save the outcome under the graph structure to the database.
- web-visualization: this module run in web server. It query the graphs in database in visualize on the browser interface.
