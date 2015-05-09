from collections import defaultdict # for defaultdict
import operator                     # for sorting dictionary
import sys, getopt                  # for command line arguments


########################
#
# Returns: inverted index, which is a dictionary.
#           Each entry of this dictionary is in this form:  Key: term, Value: [(prof_id, term_frequency), (prof_id, term_frequency), ...]
#           Where term_frequency is the number of occurences of the 'term', in all the papers, abstracts, and domains of prof_id 
#        
#######################



class InvertedIndexBuilder:
    invertedIndex = defaultdict(list)
    
    def buildInvertedIndex(self, stopwordsFile, publicationsFile):

        corpus_file = open(publicationsFile, 'r')
        stopWords = self.loadStopWords(stopwordsFile)
    
        for line in corpus_file:
            # initializing the term frequency list 
            termFrequency = defaultdict(lambda: 0)
        
            # each line will be in form ( prof_id,prof_name,title:venue:domain:abstract,title:venue:domain:abstract, ....)
            splits = line.lower().split(",")
            profID = splits[0]
            profName = splits[1]
        
            for paper in splits[2:]:
                # each paper is in form title:venue:domain:abstract
                paperSplits = paper.split(":")
            
                # title = paperSplits[0]
                # venue = paperSplits[1]
                # domain = paperSplits[2]
                # abstract = paperSplits[3]
            
                for paperSplit in paperSplits:
                    terms = paperSplit.split()
                
                    # firs, remove the stopwords
                    termsCleaned = [t for t in terms if t not in stopWords] 
                
                    # updating the term frequencies for unigrams
                    for term in termsCleaned:
                        if term not in stopWords:
                            termFrequency[term] += 1
        
                    # build bigrams
                    bigramsList = zip(terms, termsCleaned[1:])
        
                    # updating the term frequencies for bigrams
                    for bigram in bigramsList:
                        # each bigram is in form (first_term, second_term)
                        key = bigram[0] + " " + bigram[1]
                        termFrequency[key] += 1
        
            # adding all the terms (unigrams + bigrams) to the inverted index
            for term in termFrequency.keys():
                t = (profID, termFrequency[term]) 
                self.invertedIndex[term].append(t)
        
        # all entries must be sorted by profID, so that later on, we can do merge join.
        for term in self.invertedIndex.keys():
            self.invertedIndex[term].sort(key=lambda tup: tup[0])
            

    def loadStopWords(self, stopWordFilePath):
        with open(stopWordFilePath) as stopword_file:
            stopwords = stopword_file.readlines()
    
        stopwords = [s_word.strip() for s_word in stopwords]
        return stopwords
    

    
if __name__ == '__main__':
    if len(sys.argv) != 5:
        print  sys.argv[0], '-s <stopwords file> -p <publications file>'
        sys.exit(2)        
        
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hs:p:")
    except getopt.GetoptError:
        print  sys.argv[0], '-s <stopwords file> -p <publications file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print  sys.argv[0], '-s <stopwords file> -p <publications file>'
            sys.exit()
        elif opt == "-s":
            stopwordsFile = arg
        elif opt == "-p":
            publicationsFile = arg
    
    index = InvertedIndexBuilder()
    index.buildInvertedIndex(stopwordsFile, publicationsFile)
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
    
        
    