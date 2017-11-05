import psycopg2

connect = False
connect = psycopg2.connect(database = 'django_test', user = 'roman', host = 'localhost', password = 'admin')
if (connect):
    print("Yes")
else:
    print("Not")
cursor = connect.cursor()

cursor.execute('SELECT * FROM frontend_city;')

print(cursor.fetchall())
print(cursor.fetchall())

connect.close()