import sqlite3

def delete_record(db_name):
    conn = sqlite3.connect(db_name)
    with conn:
        cursor = conn.cursor()
        city = input("Enter the city to delete: ")
        keyfield = "'" + city + "'"
        cursor.execute("DELETE FROM Temps WHERE city = " + keyfield)
    for row in cursor.execute("SELECT * FROM Temps"):
        print(row)

delete_record("Temperatures.db")
