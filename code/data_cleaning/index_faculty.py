import sys
import argparse
import operator
import re, string
import csv

def edit_dist(strA, strB):
	"edit distance"
	d = [[0]*(len(strB)+1) for _ in range(len(strA)+1)]
	for i in range(0,len(strA)+1):
		d[i][0] = i
	for j in range(0,len(strB)+1):
		d[0][j] = j
	for i in range(1,len(strA)+1):
		for j in range(1,len(strB)+1):
			if strA[i-1] == strB[j-1]:
				d[i][j] = d[i-1][j-1]
			else:
				d[i][j] = min(d[i][j-1],d[i-1][j],d[i-1][j-1])+1
	return d[len(strA)][len(strB)]

def index_faculty(faculty_file,corpus_file):
	corpus = {}
	with open(corpus_file,'r') as f:
		for line in f:
			line = line.decode('utf-8','replace')
			prof = line.lower().split(',')
			if len(prof) < 3:
				continue
			corpus[prof[1]] = prof[0]
			print prof[1] #debug	

	faculty_index = {}
	with open(faculty_file,'r') as f, open('faculty_indexed.csv','w') as fi:
		for line in f:
			line = line.decode('utf-8','replace')
			prof = line.lower().split(',')
			if len(prof) < 3:
				continue
			if prof[0].split()[0] == 'name':
				continue
			print prof[0].split() #debug

			first_name = prof[0].split()[0]
			last_name = prof[0].split()[-1]
			full_name = first_name + " " + last_name
			
			id = -1
			not_identified = 1;
			if full_name in corpus:
				id = corpus[full_name]
				faculty_index[id] = line
				not_identified = 0;
			else:
				for k_full_name in corpus.keys(): #full name
					k_last_name = k_full_name.split()[1]
					k_first_name = k_full_name.split()[0]
					if edit_dist(k_last_name,last_name) < 3:
						id = corpus[k_full_name]				

						if edit_dist(k_first_name,first_name) < 3:
							not_identified = 0
							faculty_index[id] = line
							break

				if not_identified == 1:
					if id == -1:
						print '[Non-identifiable] ' + first_name,last_name
					else:
						faculty_index[id] = line
					#faculty_index[line.split(',')[0]] = line;

		for k, v in faculty_index.items():
			fi.write(k.encode('ascii','ignore') + "," + v.encode('ascii','ignore'))


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-faculty', required=True, help='unindexed original faculty dataset (e.g., faculty.csv)')
	parser.add_argument('-corpus', required=True, help='corpus file (e.g., corpus.txt)')
	opts = parser.parse_args()

	index_faculty(opts.faculty,opts.corpus)

if __name__ == '__main__':
	main()
