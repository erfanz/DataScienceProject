import xml.etree.ElementTree as ET
from collections import defaultdict

tree = ET.parse('../../temp/dblp_small.xml')

dblp = tree.getroot()

next_id = 0

# prof_id,prof_name,title:venue:domain:abstract, ...
authorPaperDict = defaultdict(list)
for article in dblp:
    titles = article.findall('title')
    
    if len(titles) == 0:
        continue
    title = titles[0].text.translate(None, ';,:.-\"\'@#()[]{}!$%^&*_-=+/?<>\\|~') 

    authors = list()
    for author in article.findall('author'):
        authorName = author.text
        authorPaperDict[authorName].append(title)
    

for author in authorPaperDict.keys():
    paperList = ""
    papers = authorPaperDict[author]
    for paper in papers[:-1]:
        paperList += paper + ","
    paperList += papers[-1]
    
    print author + "," + paperList
    