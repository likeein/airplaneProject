import pymssql

conn = pymssql.connect(host="127.0.0.1", database='DBP', user='testDB', password='0000',  charset='utf8')
cursor = conn.cursor()
cursor.execute('SELECT * FROM Airplane;')
for row in cursor:
    print(row[0], row[1], row[2])
conn.close()