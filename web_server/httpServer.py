import SimpleHTTPServer
import CGIHTTPServer, BaseHTTPServer

import cgitb; cgitb.enable()  ## This line enables CGI error reporting


import SocketServer
from urlparse import urlparse, parse_qs


PORT = 8000


class MyRequestHandler(CGIHTTPServer.CGIHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        # parsed_path is in form ParseResult(scheme='', netloc='', path='/webpages/images/icon-search.png', params='', query='', fragment='')
        print 'parsed_path', parsed_path

        args = parsed_path[4].split('&')
        
        print 'args:', args
        
        print 'self.path', self.path
        
        

        if self.path == '/':
            self.path = '../../webpages/index.html'
        elif self.path.endswith('.py'):
            page = self.path[1:]
            print 'page', page
        

        #return CGIHTTPServer.CGIHTTPRequestHandler.do_GET(self)


# class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         parsed_path = urlparse(self.path)
#         # parsed_path is in form ParseResult(scheme='', netloc='', path='/webpages/images/icon-search.png', params='', query='', fragment='')
#         print 'parsed_path', parsed_path
#
#         args = parsed_path[4].split('&')
#
#         print 'args:', args
#
#         print 'self.path', self.path
#
#
#
#         if self.path == '/':
#             self.path = '../../webpages/index.html'
#         elif self.path.endswith('.py'):
#             page = self.path[1:]
#             print 'page', page
#
#
#         return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


handler = CGIHTTPServer.CGIHTTPRequestHandler
# handler = MyRequestHandler
#handler.cgi_directories = ['../../webpages']

httpd = BaseHTTPServer.HTTPServer(('',8000), handler)
#httpd = SocketServer.TCPServer(("", PORT), handler)


print "serving at port", PORT
httpd.serve_forever()