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
			prof = line.lower().split(',')
			if len(prof) < 3:
				continue
			corpus[prof[1].split()[1]] = (prof[1].split()[0],prof[0])
	
	faculty_index = {}
	with open(faculty_file,'r') as f, open('faculty_indexed.csv','w') as fi:
		for line in f:
			prof = line.lower().split(',')
			if len(prof) < 3:
				continue
			if len(prof[0].split()) < 2:
				continue
			first_name = prof[0].split()[0]
			last_name = prof[0].split()[1]
			if last_name in corpus:
				first_id = corpus[last_name]
				if edit_dist(first_id[0],first_name) < 3:
					faculty_index[first_id[1]] = line
			else:
				for l in corpus.keys():
					if edit_dist(l,last_name) < 3:
						first_id = corpus[l]
						if edit_dist(first_id[0],first_name) < 3:
							faculty_index[first_id[1]] = line
							break
		for k, v in faculty_index.items():
			fi.write(k + "," + v)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-faculty', required=True, help='unindexed original faculty dataset (e.g., faculty.csv)')
	parser.add_argument('-corpus', required=True, help='corpus file (e.g., corpus.txt)')
	opts = parser.parse_args()

	index_faculty(opts.faculty,opts.corpus)

if __name__ == '__main__':
	main()
