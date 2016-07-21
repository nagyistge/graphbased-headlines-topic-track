# PROPER NOUN MODEL BUILD
As a system based on keywords co-occurrence, words are treated differently even when they belong to the same proper noun/name. For example, the proper noun “Thomas Edison” is broken into two separated words “Thomas” and “Edison”. The purpose of the system is to build a model to predict whether two adjacent words make up a proper noun, therefore they can be merged and treated as a single word.
The model is trained from the headline corpus itself and outcome a model, stored as pickle file. It is the loaded and used as a part of topic-tracking-source module.

# INPUT
Database that contain text corpus. You can modify this from line 33 to 37 of ModelBuilder.py.

# OUTPUT
Classifier in pickle format (with data structure from NLTK). The classifier return True if the words pair is highly consider to be mergeable and can be treat as one single word.
