import json


class Professor:
    ID          = 0
    name        = ""
    uniID       = 0
    uniName     = ""
    joinYear    = ""
    rank        = ""
    fields      = ""
    bachelor    = ""
    master      = ""
    PhD         = ""
    postdoc     = ""
    profile     = ""
    publications = []
    
    
    def toJSON(self):
        json =  {"id"       : self.ID,
        "name"      : self.name,
        "rank"      : self.rank,
        "subfields" : self.fields,
        "university": self.uniName,
        "joinyear"  : self.joinYear,
        "publications" : self.publications,
        "bcs"          : self.bachelor,
        "mcs"          : self.master,
        "phd"          : self.PhD,
        "pdoc"          : self.postdoc,
        "unitid"    : self.uniID,
        "city"      : "__",
        "state"     : "__",
        "rpub"      : "__",
        "numpub"    : 14
        }
        
        #print "json begins:"
        #print json.dumps(vars(james),sort_keys=False, indent=4)
        return json
    
    # @staticmethod
    # def findPublications(professorID, publicationFile):
    #     pubFile = open(publicationFile, 'r')
    #     pubList = []
    #     for line in pubFile:
    #         splits = line.split(",")
    #         profID = int(splits[0])
    #         if profID == professorID:
    #             for paper in splits[2:]:
    #                 # each paper is in form title:venue:domain:abstract
    #
    #                 paperSplits = paper.split(":")
    #                 title = ""
    #                 venue = ""
    #                 authors = ""
    #                 year = ""
    #
    #                 if len(paperSplits) > 0:
    #                     title = paperSplits[0]
    #                 if len(paperSplits) > 1:
    #                     venue = paperSplits[1]
    #                 if len(paperSplits) > 2:
    #                     authors = paperSplits[2]
    #                 if len(paperSplits) > 3:
    #                     year = paperSplits[3]
    #
    #                 d = {"title" : title, "venue" : venue, "authors": auhthors, "year": year}
    #                 pubList.append(d)
    #
    #     return pubList
                

    
    @staticmethod
    def findProfByProfID(professorIDs, prof_file):
        profFile = open(prof_file, 'r')
        profList = []
        
        for line in profFile:
            splits = line.split(',')
            ID = int(splits[0].strip())
            #print 'profID', profID

            if ID in professorIDs:
                p = Professor()
                p.ID   = ID
                p.name     = splits[1].strip()
                p.uniID    = int(splits[2].strip())
                p.uniName  = splits[3].strip()
                p.joinYear = splits[4].strip()
                p.rank     = splits[5].strip()
                p.fields   = splits[6].strip()
                p.bachelor = splits[7].strip()
                p.master   = splits[8].strip()
                p.PhD      = splits[9].strip()
                p.postdoc  = splits[10].strip()
                p.profile  = splits[11].strip()
                
                profList.append(p)
        return profList
        
    
    @staticmethod
    def findSingleProfByProfID(professorID, prof_file, invertedIndex):
        profFile = open(prof_file, 'r')
        
        for line in profFile:
            splits = line.split(',')
            ID = int(splits[0].strip())
            #print 'profID', profID

            if ID == professorID:
                p = Professor()
                p.ID   = ID
                p.name     = splits[1].strip()
                p.uniID    = int(splits[2].strip())
                p.uniName  = splits[3].strip()
                p.joinYear = splits[4].strip()
                p.rank     = splits[5].strip()
                p.fields   = splits[6].strip()
                p.bachelor = splits[7].strip()
                p.master   = splits[8].strip()
                p.PhD      = splits[9].strip()
                p.postdoc  = splits[10].strip()
                p.profile  = splits[11].strip()
                #p.publications = Professor.findPublications(ID, '../data/corpus_2.txt')
                p.publications = invertedIndex.publications[professorID]
                return p