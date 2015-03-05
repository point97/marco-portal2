#!python2

"""
A CORS-enabled SimpleHTTPServer, useful for simulating a production environment
(a separate server for serving static files).

Found here: http://stackoverflow.com/a/21957017/65295


Suggested usage:
- Set DEBUG to False, etc.

$ python manage.py collectstatic
$ python manage.py compress
$ cd STATIC_ROOT
$ python2 path/to/marco-portal2/scripts/SimpleCORSHTTPServer

"""

from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    BaseHTTPServer.test(CORSRequestHandler, BaseHTTPServer.HTTPServer)

