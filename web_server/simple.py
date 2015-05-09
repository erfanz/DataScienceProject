import random
import string

import cherrypy

erfan = "salam"
class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """
        <html>
            <head>
                <link href="main.css" rel="stylesheet">
	            <script src="./static/javascript/jquery-2.1.3.min.js"></script>
	            <script src="./public/javascript/searchbox.js"></script>
            </head>
            <body>
	            <div id="searchContainer">
		            <form action="generate">
			            <input id="query" name="query" type="text" />
			            <div id="delete"><span id="x">x</span></div>
			            <input id="submit" name="submit" type="submit" value="Search" />
                    </form>
                </div>
            </body>
        </html>
"""

    @cherrypy.expose
    def generate(self, length=8):
        return  erfan + '' + erfan

if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator(), '/', 'simple.config')