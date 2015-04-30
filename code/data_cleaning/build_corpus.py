import sys
import argparse
import operator
import re, string
import csv

def build_corpus(dom_dic,pub_dic,author_dic,venue_dic):
	corpus = []
	id = 0
	for k,v in author_dic.items():
		id += 1
		doc = str(id) + ',' + k
		for idx in v:
			pub = pub_dic[idx] #(title,names,year,venue,refs,abstract)
			doc += ',' + ':'.join([pub[0],pub[3]])
			dom_ = ''
			for k2, v2 in dom_dic.items():
				if idx in v2:
					dom_ += ' '.join(k2.split(','))
			doc += ':' + dom_ + ':' + pub[5]
		corpus.append(doc)
	with open('corpus.txt','wb') as f:
		for d in corpus:
			f.write(d+'\n')

def build_database(dom_dic,pub_dic,author_dic,venue_dic,input):
	with open(input) as file:
		regex = re.compile('[%s]' % re.escape(string.punctuation))
		
		#initialize variables
		domain = re.sub(r'[.].*','',input).rstrip()
		domain = re.sub('_',',',domain)
		dom_dic[domain] = []
		names = [] #[last_name,first_name, ... ]
		refs = []
		year = -1
		title = ''
		venue = ''
		index = -1
		abstract = ''

		for line in file:
			if line[:2] == '#*':
				title = line[2:].strip()
				title = regex.sub(' ', title)
				title =	re.sub(':',' ',title)
				#re-initialize variables
				refs = []
				year = -1
				venue = ''
				index = -1
				abstract = ''
				names = []
			elif line[:2] == '#@':
				author = line[2:].strip()
				authors = author.split(',')
				for a in authors:
					a_name = a.split()
					if len(a_name) >= 2:
						names.append(a_name[0]+' '+a_name[-1])
			elif line[:2] == '#t':
				year = int(line[2:].strip())
			elif line[:2] == '#c':
				venue = line[2:].strip()
				venue = regex.sub(' ', venue)
				venue = re.sub(':',' ',venue)
			elif line[:2] == '#i':
				index = int(line[6:].strip())
			elif line[:2] == '#%':
				if len(line[2:].strip()) > 0:
					refs.append(int(line[2:].rstrip()))
			elif line[:2] == '#!':
				abstract = line[2:].strip()
				abstract = regex.sub(' ', abstract)
				abstract = re.sub(':',' ',abstract)
				#instate information to dics
				dom_dic[domain].append(index)
				pub_dic[index] = (title,names,year,venue,refs,abstract)
				venue_dic[venue] = '' # augment with scope info
				for name in names:
					if name in author_dic:
						author_dic[name].append(index)
					else:
						author_dic[name] = [index]

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-list', required=True, help='domain input list (e.g., list.txt)')
	opts = parser.parse_args()
	
	with open(opts.list) as input_list:
		dom_dic = {}
		pub_dic ={}
		author_dic = {}
		venue_dic = {}
		for input in input_list:
			print input
			build_database(dom_dic,pub_dic,author_dic,venue_dic,input.strip())
		
		with open('domain.csv','wb') as f:
			csv_writer = csv.writer(f)
			for k, v in dom_dic.items():
				csv_writer.writerow([k,v])
		with open('publication.csv','wb') as f:
			csv_writer = csv.writer(f)
			for k, v in pub_dic.items():
				csv_writer.writerow([k,v])
		with open('author.csv','wb') as f:
			csv_writer = csv.writer(f)
			for k, v in author_dic.items():
				csv_writer.writerow([k,v])
		with open('venue.csv','wb') as f:
			csv_writer = csv.writer(f)
			for k, v in venue_dic.items():
				csv_writer.writerow([k,v])

		build_corpus(dom_dic,pub_dic,author_dic,venue_dic)

if __name__ == '__main__':
	main()
