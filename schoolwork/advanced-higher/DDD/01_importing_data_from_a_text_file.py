import sqlite3, csv

connection = sqlite3.connect("Films.db")
cursor = connection.cursor()
with open('values.csv', 'r') as file:
    no_records = 0
    for row in file:
        cursor.execute("INSERT INTO FilmsTable VALUES (?,?,?,?,?,?)", row.split(","))
        connection.commit()
        no_records += 1
connection.close()
print('\n{} Records Transferred'.format(no_records))
