from collections import defaultdict # for defaultdict
import operator                     # for sorting dictionary
import sys, getopt                  # for command line arguments
import math


########################
#
# Returns: inverted index, which is a dictionary.
#           Each entry of this dictionary is in this form:  Key: term,    Value: [(prof_id, term_frequency), (prof_id, term_frequency), ...]
#           Where term_frequency is the number of occurences of the 'term', in all the papers, abstracts, and domains of prof_id 
#        
#######################



class InvertedIndexBuilder:
    invertedIndex = defaultdict(list)
    publications = defaultdict(list)    # publications[profID] stores a list of publications for professor with profID. Each member of the list is in the form {'title': title, 'venue': venue, 'authors': authors, 'year':year}
    
    stopWords = list()
    profCnt = 0
    
    def build(self, stopwordsFile, corpusFile):

        corpus_file = open(corpusFile, 'r')
        self.loadStopWords(stopwordsFile)
    
    
        for line in corpus_file:
            
            self.profCnt += 1
            # initializing the term frequency list 
            termFrequency = defaultdict(lambda: 0)
        
            # each line will be in form ( prof_id,prof_name,title_1:venue_1:domain_1:year_1:#co-author_1_1#co-author_1_2#...,title_2:venue_2:domain_2:year_2:#co-authors_2_1, ....)
            splits = line.lower().split(",")
            profID = int(splits[0])
            profName = splits[1]
            
            pubs = []
            for paper in splits[2:]:
                # each paper is in form title:venue:domain:year:#co-author1#co-author2#...
                paperSplits = paper.split(":")
                
                title = ""
                venue = ""
                domain = ""
                year = 0
                authors = ""
                            
                if len(paperSplits) > 0:
                    title = paperSplits[0].capitalize()
                if len(paperSplits) > 1:
                    venue = paperSplits[1].capitalize()
                if len(paperSplits) > 2:
                    domain = paperSplits[2].capitalize()
                if len(paperSplits) > 3:
                    year = paperSplits[3]
                if len(paperSplits) > 4:
                    authors = (', ').join(map(lambda x: x.title() , paperSplits[4].split('#')))
                    

                                    
                
                #domain = paperSplits[2]
                #abstract = paperSplits[3]
                pubs.append({'title': title, 'venue': venue, 'domain': domain, 'year': year, 'authors': authors})
            
                for paperSplit in paperSplits:
                    terms = paperSplit.split()
                
                    # firs, remove the stopwords
                    termsCleaned = [t for t in terms if t not in self.stopWords] 
                
                    # updating the term frequencies for unigrams
                    for term in termsCleaned:
                        if term not in self.stopWords:
                            termFrequency[term] += 1
        
                    # build bigrams
                    bigramsList = zip(terms, termsCleaned[1:])
        
                    # updating the term frequencies for bigrams
                    for bigram in bigramsList:
                        # each bigram is in form (first_term, second_term)
                        key = bigram[0] + " " + bigram[1]
                        termFrequency[key] += 1
            
            # sort the publications by year (from most recent to oldest)
            pubs = sorted(pubs,key=operator.itemgetter('year'),reverse=True)
            self.publications[profID] = pubs
        
            # adding all the terms (unigrams + bigrams) to the inverted index
            for term in termFrequency.keys():
                t = (profID, termFrequency[term]) 
                self.invertedIndex[term].append(t)
        
        # now sort each entry by the prof ID so later we can do merge sort
        for term in self.invertedIndex.keys():
            self.invertedIndex[term].sort(key=lambda tup: tup[0])  # sorts in place


    def loadStopWords(self, stopWordFilePath):
        with open(stopWordFilePath) as stopword_file:
            self.stopWords = stopword_file.readlines()
    
        self.stopWords = [s_word.strip() for s_word in self.stopWords]
        
    def mergeJoin(self, terms):
        if len(terms) == 0:
            return []
        else:
            return self.mergeJoinHelper(terms[0], terms[1:])
    
    def mergeJoinHelper(self, first, rest):
        if len(rest) == 0:
            output = []
            for x in self.invertedIndex[first]:
                output.append(x[0])
            return output
        else:
            rest_output = self.mergeJoinHelper(rest[0], rest[1:])
            # now we join first to rest
            i = 0
            j = 0
            output = list()
            while (i < len(self.invertedIndex[first]) and j < len(rest_output)):
                if self.invertedIndex[first][i][0] == rest_output[j]:
                    output.append(self.invertedIndex[first][i][0])
                    i += 1
                    j += 1
                elif self.invertedIndex[first][i][0] < rest_output[j]:
                    i += 1
                else:
                    j += 1
            return output            
        
    def sortByTF_IDF(self, profIDs, query):
        profWeight = defaultdict(lambda: 0.0) 
        for term in query:
            for prof in self.invertedIndex[term]:
                if prof[0] in profIDs:
                    tf = prof[1]
                    df = len(self.invertedIndex[term])
                    profWeight[prof[0]] += (1 + math.log(tf)) * math.log(self.profCnt / len(self.invertedIndex[term]))
        
        profWeightUpdated = defaultdict(lambda: 0.0) 
        for prof in profWeight.keys():
            if profWeight[prof] > 1:
                profWeightUpdated[prof] = profWeight[prof]
        
        profWeightUpdated = sorted(profWeightUpdated.iteritems(),key=operator.itemgetter(1),reverse=True)
        return profWeightUpdated
            
            
    
if __name__ == '__main__':
    if len(sys.argv) != 5:
        print  sys.argv[0], '-s <stopwords file> -c <corpus file>'
        sys.exit(2)        
        
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hs:c:")
    except getopt.GetoptError:
        print  sys.argv[0], '-s <stopwords file> -c <corpus file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print  sys.argv[0], '-s <stopwords file> -c <corpus file>'
            sys.exit()
        elif opt == "-s":
            stopwordsFile = arg
        elif opt == "-c":
            corpusFile = arg
    
    index = InvertedIndexBuilder()
    index.build(stopwordsFile, corpusFile)
    termfreq = dict()
    
    
    
    for term in index.invertedIndex.keys():
        if term == 'database systems':
            print "len", len(index.invertedIndex[term])
        
        if term == 'database system':
            print "len", len(index.invertedIndex[term])
        
            
        summ = 0
        for prof_tf in index.invertedIndex[term]:
            summ += prof_tf[1] 
        termfreq[term] = summ
    
    if 'database systems' in termfreq.keys():
        print termfreq['database systems']
    if 'database system' in termfreq.keys():
        print termfreq['database system']
    
    
    sorted_termfreq = sorted(termfreq.items(), key=operator.itemgetter(1))
    print sorted_termfreq
    
        
    