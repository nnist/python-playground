import sqlite3

conn = sqlite3.connect('test.db')

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS moods (
    id INTEGER PRIMARY KEY,
    date_time,
    anxiety,
    depressive
)""")

anxiety = 3
depressive = 1

cur.execute("""INSERT INTO moods VALUES (NULL, CURRENT_TIMESTAMP, ?, ?)""", (anxiety, depressive))

conn.commit()

cur.execute("""SELECT * FROM moods""")

for row in cur:
        print (row)

cur.close()
