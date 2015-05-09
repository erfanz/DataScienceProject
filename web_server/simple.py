import random
import string

import cherrypy

import os
#import sys
#scriptpath = "../code/inverted_index/InvertedIndexBuilder.py"
#sys.path.append(os.path.abspath(scriptpath))
#import InvertedIndexBuilder 
#import ..code.inverted_index.InvertedIndexBuilder


# import inverted index
#pmName = input('../code/inverted_index/InvertedIndexBuilder.py')
#pm = __import__(pmName)
#print(dir(pm)) # just for fun :)
#from classes.invertedIndexBuilder import InvertedIndexBuilder



import sys, os
#parent_dir = os.pardir # find the path to module a
#sys.path.insert(0, './inverted_index/invertedIndexBuilder.py')
from inverted_index.invertedIndexBuilder import InvertedIndexBuilder
# Then go up one level to the common parent directory
# import inverted index
#pmName = input('../code/inverted_index/InvertedIndexBuilder.py')
#pm = __import__(pmName)
#print(dir(pm)) # just for fun :)
#from classes.invertedIndexBuilder import InvertedIndexBuilder 


PORT = 8000



index = InvertedIndexBuilder()


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """
        <!DOCTYPE html>
        <html><head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8"><meta charset="utf-8">
        <style>

        .states {
            fill: #000;
            stroke: #fff;
        }

        .symbol {
            fill: red;
            fill-opacity: .6;
            stroke: #fff;
        }

        svg {
            display:block; margin-left:auto; margin-right:auto;
        }



        </style>
        <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
	
        <script type="text/javascript" src="http://d3js.org/d3.v3.min.js"></script>
        <script type="text/javascript" src="http://d3js.org/queue.v1.min.js"></script>
        <script type="text/javascript" src="http://d3js.org/topojson.v1.min.js"></script>
        <script src="http://eyeseast.github.io/visible-data/components/bootstrap/js/tooltip.js" type="text/javascript"></script>
        <script src="http://eyeseast.github.io/visible-data/components/jquery/jquery.min.js" type="text/javascript"></script>
        <script src="http://eyeseast.github.io/visible-data/components/bootstrap/js/tooltip.js" type="text/javascript"></script>
        <script src="http://eyeseast.github.io/visible-data/components/underscore/underscore-min.js" type="text/javascript"></script>
        <script src="http://eyeseast.github.io/visible-data/components/highlightjs/highlight.pack.js" type="text/javascript"></script>
        <title>ProfFinder</title>
        <style>
        .tooltip-inner{
            background-color:#444;
        }
        .tooltip.top .tooltip-arrow{
            border-top-color:#444;
        }
        .tooltip.bottom .tooltip-arrow{
            border-bottom-color:#444;
        }
        .tooltip.left .tooltip-arrow{
            border-left-color:#444;
        }
        .tooltip.right .tooltip-arrow{
            border-right-color:#444;
        }
        </style>
	
        </head>
        
        
        <body>

        <div class="row">
        <div class="col-md-2"></div>
        <div class="col-md-8">
        <div class="page-header center">
        <img src="/images/logo.png" style="display:block; margin-left:auto; margin-right:auto" height=150/>
        </div>

        <div id="searchContainer" >
        <form action="showResults" style="display:block; margin-left:auto; margin-right:auto; width:50%">
        <input id="query" name="query" type="text" style="width:85%"/>
        <input id="submit" name="submit" type="submit" value="Search" />
        </form>
        </div>
		
        <div class="page-header center">
		
        </div>
	
        </div>
        </div>

        <script type="x-jst" id="tooltip-template">
        <h5><%= name %></h5>
        <p>CS Faculty Members: <%= total_cs_fac%></p>
        </script>

        <script>

        var width = 960,
        height = 500;

        var radius = d3.scale.sqrt()
        .domain([0, 200])
        .range([0, 20]);

        var formats = {
            percent: d3.format('%')
        };
	
        var path = d3.geo.path();

        var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

        queue()
        .defer(d3.json, "/json/us.json")
        .defer(d3.json, '/json/Inst_info.json')
        .await(ready);
	
	
        // template, for later
        var template = _.template(d3.select('#tooltip-template').html());

        function ready(error, us, centroid) {
            svg.append("path")
            .attr("class", "states")
            .datum(topojson.feature(us, us.objects.states))
            .attr("d", path);

            var schools = svg.selectAll(".symbol")
            .data(centroid.features)
            .enter().append("path")
            .attr("class", "symbol")
            .attr("d", path.pointRadius(function(d) { return radius(d.properties.total_cs_fac)}));
	  
            schools.on('mouseover', tooltipShow)
            .on('mouseout', tooltipHide);
        }

        function tooltipShow(d, i) {
            var datum = d.properties;
            if (!datum) return;

            datum.formats = formats;

            $(this).tooltip({
                title: template(datum),
                html: true,
                container: svg.node().parentNode,
                placement: 'auto'
            }).tooltip('show');
        }

        function tooltipHide(d, i) {
            $(this).tooltip('hide');
        }

        </script>

        </body>
        </html>       
        """

    @cherrypy.expose
    def showResults(self, query, submit):
        # first, we tokenize the search query
        tokens = query.lower().split()
        
        # then, removes the stop words
        important_tokens = [x for x in tokens if x not in index.stopWords]
        profIDs = index.mergeJoin(important_tokens)
        print profIDs
        return profIDs

if __name__ == '__main__':
    print 'Building and loading the inverted index ... (may take a few minutes)'
    stopwordsFile = '../utils/stopwords.txt'
    publicationsFile = '../data/entities/publication.csv'
    index.build(stopwordsFile, publicationsFile)
    cherrypy.quickstart(StringGenerator(), '/', 'simple.config')