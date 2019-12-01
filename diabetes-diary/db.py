import sqlite3, datetime

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.date = str(datetime.date.today())[-2:] + "/" + str(datetime.date.today())[5:7] + "/" + str(datetime.date.today())[2:4]
        self.cur.execute("CREATE TABLE IF NOT EXISTS BloodLevels (\
                            date TEXT PRIMARY KEY NOT NULL, \
                            breakfast TEXT, \
                            lunch TEXT, \
                            dinner TEXT, \
                            bedtime TEXT)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM BloodLevels")
        rows = self.cur.fetchall()
        return rows

    def fetch_current(self):
        self.cur.execute("SELECT breakfast, lunch, dinner, bedtime FROM BloodLevels WHERE date = ?", (self.date,))
        row = self.cur.fetchone()
        return row

    def insert(self, breakfast, lunch, dinner, bedtime):
        try:
            self.cur.execute("INSERT INTO BloodLevels VALUES (?, ?, ?, ?, ?)", (self.date, breakfast, lunch, dinner, bedtime))
            self.conn.commit()
        except:
                self.cur.execute("UPDATE BloodLevels SET breakfast = ?, lunch = ?, dinner = ?, bedtime = ? WHERE date = ?", (breakfast, lunch, dinner, bedtime, self.date))
                self.conn.commit()

    def __del__(self):
        self.conn.close()
