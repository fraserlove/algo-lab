import sqlite3

conn = sqlite3.connect("Temperatures.db")
cursor = conn.cursor()

# creating a table
cursor.execute("""  CREATE TABLE Temps (
                    city TEXT,
                    temperature INTEGER,
                    localTime TEXT,
                    primary key (city))
                    """)

# inserting multiple records

Temps = [('London', 7, '1200'),
         ('Accra', 30, '1200'),
         ('Baghdad', 20, '1500'),
         ('Winnipeg', -12, '0600'),
         ('New York', 14, '0700'),
         ('Nairobi', 27, '1500'),
         ('Sydney', 22, '2300')]
cursor.executemany("INSERT INTO Temps VALUES (?,?,?)", Temps)
conn.commit()
conn.close()
print('Table sucessfully created!')
