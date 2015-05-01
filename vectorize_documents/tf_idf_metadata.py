from __future__ import division
import os
import numpy as np

tf_idf_corpus = {}

try:
	print "reading from existing metadata.."
	fd = open('./metadata/tf_idf_corpus.txt', 'r')
	for line in fd.readlines():
		spl = (line.strip('\n')).split(' ')
		key = spl[0]
		val = spl[1]
		tf_idf_corpus[key] = int(val)
except:
	pass







all_texts_tf = []

files = [f for f in os.listdir('.') if os.path.isfile(f)]
print files
for f in files:
	if f == 'tf_idf_metadata.py' or f == '.DS_Store':
		pass
	else:
		(title, terms) = (f , {})
		
		fd = open(f, "r")

		for line in fd.readlines():
			split=line.split(' ')
			for word in split:

				#count number of terms for individual document
				if word in terms.keys():
					terms[word] += 1
				else:
					terms[word] = 1
		

				#count number of terms for entire doc
				#huge performance b00$t!
				try:
					tf_idf_corpus[word] += 1
				except:
					tf_idf_corpus[word] = 1

				# if word in tf_idf_corpus.keys():
				# 	tf_idf_corpus[word] += 1
				# else:
				# 	tf_idf_corpus[word] = 1


		all_texts_tf.append((title,terms))



for article in all_texts_tf:
	for word in article[1].keys():
		article[1][word] = article[1][word]/tf_idf_corpus[word]



for article in all_texts_tf:
	filename = (article[0].replace('.txt', ''))+ '_metadata.txt'
	fd = open( './metadata/'+filename, 'w+')
	for ele in article[1].keys():
		if ele != ' ' and ele != '': #omit space characters
			fd.write(str(ele))
			fd.write(' ')
			fd.write(str(article[1][ele]))
			fd.write('\n')
	fd.close()





fd = open('./metadata/tf_idf_corpus.txt', 'w+')
for ele in tf_idf_corpus.keys():
	fd.write(str(ele))
	fd.write(' ')
	fd.write(str(tf_idf_corpus[ele]))
	fd.write('\n')


print "done processing....."

