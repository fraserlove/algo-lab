import sqlite3, csv

def import_file(path):
    connection = sqlite3.connect("Films.db")
    cursor = connection.cursor()
    with open(path, 'r') as file:
        no_records = 0
        for row in file:
            print(row.split(","))
            cursor.execute("INSERT INTO FilmsTable VALUES (?,?,?,?,?,?)", row.split(","))
            connection.commit()
            no_records += 1
    connection.close()
    print('\n{} Records Transferred'.format(no_records))

import_file('data/films.txt')
