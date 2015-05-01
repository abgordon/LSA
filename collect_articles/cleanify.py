import os
import re
from stemming.porter2 import stem

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
	if f == 'cleanify.py' or f == 'vectorize_tf_idf.py' or f == 'tf_idf_metadata.py':
		pass
	else:
		counter = 0
		fd = open(f, "r")
		stringarray = []
		lines = fd.readlines()
		for line in lines:
			for word in line.split(' '):
				counter +=1
				stringarray.append(stem(re.sub('[^A-Za-z0-9]+', ' ', word).lower()))
				if counter ==1500:
					break
		newfile = open(f, 'w')

		for x in stringarray:
			newfile.write(x)
			newfile.write(' ')


	fd.close()

