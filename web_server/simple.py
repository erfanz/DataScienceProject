import random
import string
import json
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
from python_files.professor import Professor



# Then go up one level to the common parent directory
# import inverted index
#pmName = input('../code/inverted_index/InvertedIndexBuilder.py')
#pm = __import__(pmName)
#print(dir(pm)) # just for fun :)
#from classes.invertedIndexBuilder import InvertedIndexBuilder 


index = InvertedIndexBuilder()


stopwordsFile   = '../utils/stopwords.txt'
corpusFile      = '../data/corpus_2.txt'
profFile        = '../data/faculty_indexed.csv'


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
        print 'profIDs', profIDs
        sortedProfIDs = index.sortByTF_IDF(profIDs, important_tokens)
        #print "sorted prof ID", sortedProfIDs
        #profIDs = [158972, 18382, 158944]
        
        ultimateList = []
        for prof in sortedProfIDs:
            ultimateList.append(prof[0])
        print 'ultimateList' ,  ultimateList
        
        profList = Professor.findProfByProfID(ultimateList, profFile, index)
        print 'profList', profList
        jsonList = []
        for prof in profList:
            jsonList.append(prof.toJSON())
            
        # print json.dumps(jsonList) 
        
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
        <script src="http://eyeseast.github.io/visible-data/components/jquery/jquery.min.js" type="text/javascript"></script>
        <script src="http://eyeseast.github.io/visible-data/components/bootstrap/js/tooltip.js" type="text/javascript"></script>
        <script src="http://eyeseast.github.io/visible-data/components/underscore/underscore-min.js" type="text/javascript"></script>
        <script src="http://eyeseast.github.io/visible-data/components/highlightjs/highlight.pack.js" type="text/javascript"></script>
        <!--script src="javascript/jput-2.js" type="text/javascript"></script-->
        <script src="javascript/jput.min.js" type="text/javascript"></script>
	
        <title>ProfFinder</title>
	
        </head>
        <body>

        <div class="row">
        <div class="col-md-2"></div>
        <div class="col-md-8">
        <div class="page-header center" style="height: 62px;"><div style="float:left" height=60>
        <img src="images/logo.png" height=60/></div>
        <div id="searchContainer" style="float:left; width:80%">
        <form action="showResults" >
        <input id="query" name="query" type="text" style="width:85%"/>
        <input id="submit" name="submit" type="submit" value="Search" />
        </form>
        </div>
        </div>

        <script>
        
            var json= """ + json.dumps(jsonList) + """;


			$(document).ready(function(){
				queue()
					.defer(d3.json, '/json/Inst_info.json')
					.await(ready);
			});

			function ready(error, centroid) {
				for(var j = 0; j < json.length; j++) {
					for(var i = 0; i < centroid.features.length; i++) {
						var obj = centroid.features[i];
						if (obj.id == json[j].unitid) {
						json[j]["city"] = obj.properties.city;
						json[j]["state"] = obj.properties.state;
						}
					}
				}

				$('#main').jPut({
				jsonData:json,   //your json data
				name:'template'  //jPut template name
				});
			}
        </script>
	
	
        <div id="main">

        <div jput="template">
        <div style="margin: 10px">
        <a href="/profile?query=""" + query + """&pid={{id}}&uniid={{unitid}}">{{name}} ({{rank}} Professor)</a><br>
        <div style="margin-left: 10px">
        {{university}} ({{city}}, {{state}})<br>
        Research Field: {{subfields}}<br>
		Recent Publication: {{rpub}} ({{numpub}} publications found)<br>
        </div>
        </div>
        </div>
        </div>
	
	
		
        <!--div class="page-header center">
        <p align='center'>Page &lt; <a href="#">1</a> &gt;</p>
        </div-->
	
        </div>
        <div class="col-md-2" id="sidebar"></div>

        </body>
        </html>
        
        """
    @cherrypy.expose
    def profile(self, query, pid, uniid):
        professor = Professor.findSingleProfByProfID(int(pid), profFile, index)
        jsonEntity = [professor.toJSON()]
        
        return """
        <!DOCTYPE html>
        <html><head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8"><meta charset="utf-8">
        <style>

        .states {
            fill: #000;
            stroke: #fff;
            stroke-width: 0.4;
        }

        .symbol {
            fill: red;
            fill-opacity: 0.8;
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
        <script src="http://eyeseast.github.io/visible-data/components/jquery/jquery.min.js" type="text/javascript"></script>
        <script src="http://eyeseast.github.io/visible-data/components/bootstrap/js/tooltip.js" type="text/javascript"></script>
        <script src="http://eyeseast.github.io/visible-data/components/underscore/underscore-min.js" type="text/javascript"></script>
        <script src="http://eyeseast.github.io/visible-data/components/highlightjs/highlight.pack.js" type="text/javascript"></script>
        <script src="javascript/jput-2.js" type="text/javascript"></script>
        <script src="javascript/jput.min.js" type="text/javascript"></script>
	
        <title>ProfFinder</title>
	
        </head>
        <body>

        <div class="row">
        <div class="col-md-2"></div>
        <div class="col-md-8">
        <div class="page-header center" style="height: 62px;"><div style="float:left" height=60>
        <img src="images/logo.png" height=60/></div>
        <div id="searchContainer" style="float:left; width:80%">
        <form action="showResults" >
        <input id="query" name="query" type="text" style="width:85%"/>
        <input id="submit" name="submit" type="submit" value="Search" />
        </form>
        </div>
        </div>
        </div>
        </div>
        <div class="row">
        <div class="col-md-2"></div>
        <div class="col-md-6" id="main">
        <div jPut="template">
        <div style="margin: 10px">
        <h3>{{name}} ({{rank}} Professor)</h3>
        <div style="margin-left: 10px">
        Faculty at {{university}} since {{joinyear}}<br/>
        {{acastart}}{{bscstr}}{{mscstr}}{{phdstr}}{{pdocstr}}{{acaend}}
	
        Research Field: {{subfields}}<br>
        </div>
        
        </div>
	
	
        <br/>
        
        <div style="margin: 10px" jrepeat="publications">
        <h4>Publications</h4>
        <div style="margin: 10px;" jput="publications">
        <div style="margin-left: 10px;">
        {{authors}}:<br>
        <div style="margin-left: 10px; margin-bottom: 15px; margin-left: 20px">
        <em><strong>{{title}}</strong></em><br/>
        {{venue}} ({{year}})
        </div>
        </div>
        </div>
        </div>
        
        </div>
        </div>
        <div class="col-md-2" id="sidebar">
        <div style="margin: 10px" jput="side">	
        <h4>Institution</h4>
        <div style="margin-left: 10px">
        <a href="http://{{website}}">{{name}}</a><br/>
        <a href="{{dept_site}}">CS Department</a><br>
        {{addr}}<br>
        {{city}}, {{state}} {{zip_code}}<br>
        USA<br><br>
        Size of CS faculty: {{total_cs_fac}}<br>
        <a href="http://{{price_calc}}">Admission information</a><br><br>
	
        <a href="{{citylink}}">City Information ({{city}})</a>

        </div>
        </div>

        </div>

        <script>
        var unitid = "0";
        var json=""" + json.dumps(jsonEntity) + """;

        statedict = {
            "AL": "Alabama",
            "AK": "Alaska",
            "AS": "American-Samoa",
            "AZ": "Arizona",
            "AR": "Arkansas",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "DC": "District-Of-Columbia",
            "FM": "Federated-States-Of-Micronesia",
            "FL": "Florida",
            "GA": "Georgia",
            "GU": "Guam",
            "HI": "Hawaii",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "IA": "Iowa",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "ME": "Maine",
            "MH": "Marshall Islands",
            "MD": "Maryland",
            "MA": "Massachusetts",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MS": "Mississippi",
            "MO": "Missouri",
            "MT": "Montana",
            "NE": "Nebraska",
            "NV": "Nevada",
            "NH": "New-Hampshire",
            "NJ": "New-Jersey",
            "NM": "New-Mexico",
            "NY": "New-York",
            "NC": "North-Carolina",
            "ND": "North-Dakota",
            "MP": "Northern-Mariana-Islands",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PW": "Palau",
            "PA": "Pennsylvania",
            "PR": "Puerto-Rico",
            "RI": "Rhode-Island",
            "SC": "South-Carolina",
            "SD": "South-Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VT": "Vermont",
            "VI": "Virgin Islands",
            "VA": "Virginia",
            "WA": "Washington",
            "WV": "West Virginia",
            "WI": "Wisconsin",
            "WY": "Wyoming"
        }

        $(document).ready(function(){
            json[0]["bscstr"] = "";
            json[0]["mscstr"] = "";
            json[0]["phdstr"] = "";
            json[0]["pdocstr"] = "";
            json[0]["acastart"] = "<div style=\\\"margin-left: 20px; margin-bottom: 10px\\\">";
            json[0]["acaend"] = "</div>";
            if(json[0].hasOwnProperty('bsc')){
                json[0]["bscstr"] = "B.S. " + json[0]["bcs"] + "<br/>";
            }
            if(json[0].hasOwnProperty('msc')){
                json[0]["mscstr"] = "M.S. " + json[0]["mcs"] + "<br/>";
            }
            if(json[0].hasOwnProperty('phd')){
                json[0]["phdstr"] = "PhD. " + json[0]["phd"] + "<br/>";
            }
            if(json[0].hasOwnProperty('pdoc')){
                json[0]["pdocstr"] = "Post Doc. " + json[0]["pdoc"] + "<br/>";
            }
	

            $('#main').jPut({
                jsonData:json,   //your json data
                name:'template'  //jPut template name
            });
   
            unitid = json[0]["unitid"];
   
            queue()
            .defer(d3.json, "/json/us.json")
            .defer(d3.json, '/json/Inst_info.json')
            .await(ready);
        });


        var width = 200,
        height = 104;

        var radius = d3.scale.sqrt()
        .domain([0, 1e6])
        .range([0, 10]);
	
        var margin = {top: 5, left: 5, bottom: 5, right: 5}
        , width = parseInt(d3.select('#sidebar').style('width'))
        , width = width - margin.left - margin.right
        , mapRatio = .5
        , height = width * mapRatio;

        var projection = d3.geo.albersUsa()
        .scale(width)
        .translate([width / 2, height / 2]);

        var path = d3.geo.path()
        .projection(projection);	
        //var path = d3.geo.path();

        var svg = d3.select("#sidebar").insert("svg", ":first-child")
        .attr("width", width)
        .attr("height", height);

        /*queue()
        .defer(d3.json, "us.json")
        .defer(d3.json, 'Inst_info.json')
        .await(ready);*/

        function ready(error, us, centroid) {
            var sidedata = {};
            for(var i = 0; i < centroid.features.length; i++) {
                var obj = centroid.features[i];
                if (obj.id == unitid) {
                    sidedata = obj.properties;
                    sidedata["citylink"] = "http://www.city-data.com/city/"+sidedata.city+"-"+statedict[sidedata.state]+".html";
		
                    $('#sidebar').jPut({
                        jsonData: [sidedata],   //your json data
                        name:'side'  //jPut template name
                    });
                }
            }

   

            svg.append("path")
            .attr("class", "states")
            .datum(topojson.feature(us, us.objects.states))
            .attr("d", path);
 
            svg.selectAll(".symbol")
            .data(centroid.features)
            .enter().append("path")
            .attr("class", "symbol")
            .attr("d", path.pointRadius(function(d) { 
                if(d.id == unitid){
                    return 5;}
                    else{return 0;}}));
                }


                d3.select(window).on('resize', resize);

                function resize() {
                    // adjust things when the window size changes
                    width = parseInt(d3.select('#svg').style('width'));
                    width = width - margin.left - margin.right;
                    height = width * mapRatio;

                    // update projection
                    projection
                    .translate([width / 2, height / 2])
                    .scale(width);

                    // resize the map container
                    svg
                    .style('width', width + 'px')
                    .style('height', height + 'px');

                    // resize the map
                    svg.selectAll('.symbols').attr('d', path);
                    svg.selectAll('.states').attr('d', path);
                }
                </script>

                </body>
                </html>
        
        """
        

if __name__ == '__main__':
    print 'Building and loading the inverted index ... (may take a few minutes)'
    index.build(stopwordsFile, corpusFile)
    cherrypy.quickstart(StringGenerator(), '/', 'simple.config')