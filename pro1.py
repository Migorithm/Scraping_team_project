import cx_Oracle

dsn = cx_Oracle.makedsn("localhost", 1521, 'xe')
db = cx_Oracle.connect('SCOTT', 'TIGER', dsn)
cur = db.cursor()

res = cur.var(cx_Oracle.CURSOR)
cur.callproc("MINI_PRO01", ['포도',res])
result = res.getvalue()
for row in result:
    print(row)

"""SELECT table_name FROM
(SELECT ALL_TABLES. *, rownum rn 
FROM ALL_TABLES WHERE OWNER = 'SCOTT') 
where rn > 10;
"""