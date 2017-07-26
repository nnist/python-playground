import sqlite3
from tabulate import tabulate
from datetime import datetime, timedelta

def query_database(query):
    conn = sqlite3.connect('data/p2000.db')
    cur = conn.cursor()
    result = cur.execute(query)
    results = result.fetchall()
    cur.close()
    return results

# results = query_database("""SELECT * FROM messages WHERE capcodes NOT NULL"""))
# results = query_database("""SELECT * FROM messages WHERE type='Brandweer'""")

# Get most recent message
results = query_database("""SELECT MAX(date_time), type, region, details
                            FROM messages
                        """)
print('\nMost recent message')
print(tabulate(results))

# Get first message
results = query_database("""SELECT MIN(date_time), type, region, details
                            FROM messages
                        """)
print('\nFirst message')
print(tabulate(results))

# Count all call types
results = query_database("""SELECT type, COUNT(*)
                            FROM messages
                            GROUP BY type
                        """)
print('\nNumber of calls per type')
print(tabulate(results))

# Return number of messages per region
results = query_database("""SELECT region, COUNT(*) AS cnt
                            FROM messages
                            GROUP BY region
                            ORDER BY cnt DESC
                        """)
print('\nNumber of messages per region')
print(tabulate(results))

# Get results of last half hour
dt = datetime.today() - timedelta(minutes=30)
results = query_database("SELECT date_time, type, region, priority, postcode, details FROM messages WHERE date_time > '" + str(dt) + "' ORDER BY date_time ASC")
print('\nAll messages of last half hour')
print(tabulate(results))
