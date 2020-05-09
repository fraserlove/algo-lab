import sqlite3

def update():
    with sqlite3.connect("Temperatures.db") as conn:
        cursor = conn.cursor()
        for row in cursor.execute("SELECT * FROM Temps"):
            print(row)

        keyfield = "'" + input('Enter the city name of the record to update: ') + "'"
        field = input("Change which field (temperature or localTime): ")
        new_val = input("Enter the new value for this field: ")

        # Validate new entry to make sure that the new values is of the right data type
        try:
            cursor.execute("UPDATE Temps SET " + field + "=" + new_val + " WHERE city = " + keyfield)
            print("\n Record Updated!")
        except:
            print("\nError: invalid data entered, record not updated")

        for row in cursor.execute("SELECT * FROM Temps"):
            print(row)

update()
