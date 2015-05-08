import csv

dept = {}
uni = {}
name = {}

mFile = open(('merged.csv'), 'w')

def merge_url (urlA, urlB):
	stripA = urlA.replace('http://','').replace('https://','').rstrip('/')
	stripB = urlB.replace('http://','').replace('https://','').rstrip('/')
	if stripA != stripB:
		print(urlA + ' -- ' + urlB)
		

filereader = csv.reader(open(('batch_results.csv'),'r'))
for line in filereader:
	unitid = line[28]
	if unitid not in dept:
		name[unitid] = line[29]
		dept[unitid] = line[30]
		uni [unitid] = line[31]
	else:
		merge_url(dept[unitid], line[30])
		merge_url(uni[unitid], line[31])


	