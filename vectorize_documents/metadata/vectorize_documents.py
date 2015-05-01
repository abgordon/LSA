import os
import numpy as np
import matplotlib.pyplot as plt
import sys
from stemming.porter2 import stem
import re


"""
"Mini Search," a vector-based model for semantic similarity
Author: Andrew Gordon 4/30/2015
"""

files = [f for f in os.listdir('.') if os.path.isfile(f)]

def cosine(vect1, vect2):
	mag1 = np.linalg.norm(vect1)
	mag2 = np.linalg.norm(vect2)

	if mag1 == 0 or mag2 == 0:
		return 0
	else:
		cosine_theta = (np.dot(vect1,vect2))/(mag1*mag2)
		return cosine_theta

def usage():
	print """\nUsage:
	\n 	-d : Compare a document in filesystem to context documents
	\n 	-q <query string> : Compare a text query to documents to search
	\n
	"""

def printFiles():
	print "Files:"
	fnum = 0
	for f in files:
		if f == 'vectorize_documents.py'  or f == '.DS_Store' or f == 'tf_idf_corpus.txt' or f == 'clean_metadata.py':
			pass
		else:
			print str(fnum), f
			fnum+=1

def vectorizeQuery(string):
	normalize = stem(re.sub('[^A-Za-z0-9]+', ' ', string).lower())
	spl = normalize.split(' ')

	for term in spl:
		try:
			docs_vectorized[row_iterator, vector_space.index(term)] += 1
		except:
			print "warning:",term," not relevant to vector space"

mode = 0

"""
Parameters:
	k: number of values in S matrix you wish to keep.  100 is usually good for large numbers of documents
		-If the number of documents is less than 100, this will do nothing

	similarity_limit: cosine comparisons for document vectors must be above this value to be returned by query
"""

k = 100
similarity_limit = 0.5

try:
	if len(sys.argv) == 1:
		print "Not enought command line arguments"
		usage()
		sys.exit(0)

	if sys.argv[1] == '-d':
		printFiles()
		input_doc = input("Enter the document number you would like to compare: ")
		input_doc = int(input_doc)
	elif sys.argv[1] == '-q':
		mode = 1
		query_string = sys.argv[2]
	else:
		print "Invalid Command line argument"
		usage()
		sys.exit(0)
except:
	print "Unknown error, exiting....."
	sys.exit(0)


print "Creating Vector space from corpus text..........."
vector_space = []
corpus = open('tf_idf_corpus.txt', 'r')
for line in corpus.readlines():
	(key,val)=line.split(' ')
	vector_space.append(key)

print "Done"
dim_rows = len(files)-3
dim_cols = len(vector_space)
docs_vectorized = np.zeros(shape=(dim_rows + 1,len(vector_space)))

print "Creating Row Vectors from", len(files), "documents......."
row_iterator= 0

#print files


document_names = []
for f in files:
	if f == 'vectorize_documents.py'  or f == '.DS_Store' or f == 'tf_idf_corpus.txt':
		pass
	else:
		document_names.append(f)
		article = open(f, 'r')
		print "Reading document number", str(row_iterator) + ":",f
		for line in article.readlines():
			(key,val) = line.split(' ')
			docs_vectorized[row_iterator, vector_space.index(key)] = float(val)
		row_iterator+=1

print "Done"

print "dim_rows:", dim_rows
print "dim_cols:", dim_cols

if mode == 1:
	vectorizeQuery(query_string)

docs_vectorized = np.transpose(docs_vectorized)




#Perform singular value decomposition
U,s,V = np.linalg.svd(docs_vectorized, full_matrices=False)

#zero out noisy data
for i in range(100,len(s)):
 	s[i] = 0

#reweight vectors
for i in range(0, len(s)):
	V[i] = V[i] * s[i]

#reapproximate original vector space
A2 = np.dot(U,V)


A2_space_Cosines = np.zeros(shape=(1,len(document_names)))
A2Cosines=np.transpose(A2)


if mode == 0:
	for i in range(0,len(document_names)):
		angle=cosine(A2Cosines[input_doc], A2Cosines[i])
		A2_space_Cosines[0,i]=angle

	for i in range(0,len(document_names)):
		if A2_space_Cosines[0][i] > 0.5:
			plt.plot(i,A2_space_Cosines[0][i], 'ro')
			print "Query returned document", document_names[i]
		else:
			plt.plot(i,A2_space_Cosines[0][i], 'ro')
	plt.xlabel("Refined Cos similarity to " + document_names[input_doc])
	plt.show()


if mode==1:
	
	relevant_queries = []

	for i in range(0,len(document_names)):
		angle=cosine(A2Cosines[row_iterator], A2Cosines[i])
		relevant_queries.append((angle,document_names[i]))

	for x in relevant_queries:
		if x[0] > 0.2:
			print x












""" 
#uncomment this if you wish to see noisy data

original_space_cosines = np.zeros(shape=(1,len(document_names)))

Cosinemultiplier = np.transpose(docs_vectorized)


for i in range(0,len(document_names)):
	angle=cosine(Cosinemultiplier[input_doc], Cosinemultiplier[i])
	original_space_cosines[0,i]=angle

for i in range(0,len(document_names)):
	plt.plot(i,original_space_cosines[0][i], 'ro')
	if original_space_cosines[0][i] > 0.5:
		print i
		print document_names[i]


plt.xlabel("Original Cos similarity to " + document_names[input_doc])
plt.show()

"""


""" 
#Uncomment this if you wish to see nuts n' bolts stuff about SVD

print "A = "
print docs_vectorized
print docs_vectorized.shape

print "\n\n\n U = "
print U 
print "Shape U =", U.shape #look at cols of this (doc x doc)
print "\n\n\n s = "
print s
print "Shape s =", s.shape
print "\n\n\n V = "
print V
print "Shape V =", V.shape #look at rows of this (term x term)

print "s2 = "
print s

print "V2 = "
print V

print "A2 = "
print A2
print A2.shape
"""



