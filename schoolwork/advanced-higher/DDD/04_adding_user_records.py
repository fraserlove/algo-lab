import sqlite3

conn = sqlite3.connect("Temperatures.db")
cursor = conn.cursor()
continue_session = 'y'

while continue_session == 'y':
    city = input("Enter the city name: ")
    temp = input("Enter the temperature: ")
    time = input("Enter the local time: ")
    # Try ... except statment is used so that if a city which already exists in
    # the database is entered the program wont crash. This is because the city field must be unique
    try:
        cursor.execute("INSERT INTO Temps VALUES (?,?,?)", [city, temp, time])
        conn.commit()
    except:
        print("Error: A record for this city already exists!")
    continue_session = input('Do you want to enter another record (y/n): ')
conn.close()
