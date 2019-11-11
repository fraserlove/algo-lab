import sqlite3

conn = sqlite3.connect("Temperatures.db")
cursor = conn.cursor()
print("%-15s%20s%20s" % ("City", "Temperature", "Local Time"))
for row in cursor.execute('SELECT * FROM Temps ORDER BY temperature DESC'):
    city, temperature, localTime = row
    print("%-15s %15d %20s" %(city, temperature, localTime))
