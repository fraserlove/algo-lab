import sqlite3
connection = sqlite3.connect("Films.db")
cursor = connection.cursor()

sql_cmd = """
    CREATE TABLE FilmsTable (
        filmID TEXT,
        title TEXT,
        yearReleased INTEGER,
        rating TEXT,
        duration INTEGER,
        genre TEXT,
        primary key (filmID)
    ) """

cursor.execute(sql_cmd)
print('FilmsTable created in MyFilms.db')

# The commit statment saves changes to the database
connection.commit()
connection.close()
