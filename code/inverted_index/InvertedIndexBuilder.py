from collections import defaultdict
import operator


DATA_DIRECTORY = "../../data"
STOP_WORDS = "../../utils/stopwords.txt"

def buildInvertedIndex():
    ########################
    #
    # Returns: inverted index, which is a dictionary.
    #           Each entry of this dictionary is in this form:  Key: term, Value: [(prof_id, term_frequency), (prof_id, term_frequency), ...]
    #           Where term_frequency is the number of occurences of the 'term', in all the papers, abstracts, and domains of prof_id 
    #        
    #######################
    corpus_file = open(DATA_DIRECTORY + '/corpus.csv', 'r')
    stopWords = loadStopWords(STOP_WORDS)
    invertedIndex = defaultdict(list)
    
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
            invertedIndex[term].append(t)
        
    return invertedIndex


def loadStopWords(stopWordFilePath):
    with open(stopWordFilePath) as stopword_file:
        stopwords = stopword_file.readlines()
    
    stopwords = [s_word.strip() for s_word in stopwords]
    return stopwords
    

    

if __name__ == '__main__':
    invertedIndex = buildInvertedIndex()
    termfreq = dict()
    
    
    
    for term in invertedIndex.keys():
        if term == 'database systems':
            print "len", len(invertedIndex[term])
        
        if term == 'database system':
            print "len", len(invertedIndex[term])
        
            
        summ = 0
        for prof_tf in invertedIndex[term]:
            summ += prof_tf[1] 
        termfreq[term] = summ
    
    if 'database systems' in termfreq.keys():
        print termfreq['database systems']
    if 'database system' in termfreq.keys():
        print termfreq['database system']
    
    
    sorted_termfreq = sorted(termfreq.items(), key=operator.itemgetter(1))
    #print sorted_termfreq
    
        
    