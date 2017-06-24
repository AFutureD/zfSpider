import pymysql

conn = pymysql.connect(host = '123.207.229.127',port=3306,user = 'root', password='dhn78834',db='class',charset='utf8')

cursor = conn.cursor()

cursor.execute("select * from student_info WHERE Sid = '15999222'")

print(cursor.fetchall())

conn.close()