#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
searchQuery = form.getvalue('query')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Hello %s</h2>" % (searchQuery)
print '<div id="searchContainer">'
print '<form action="cgi-bin/httpServer.py">'
print '<input id="query" name="query" type="text" />'
print '<div id="delete"><span id="x">x</span></div>'
print '<input id="submit" name="submit" type="submit" value="Search" />'
print '</form>'
print '</div>'
print "</body>"
print "</html>"