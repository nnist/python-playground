import sqlite3
from tabulate import tabulate
from datetime import datetime, timedelta
import os
import sys

def query_database(query):
    conn = sqlite3.connect('data/p2000.db')
    cur = conn.cursor()
    result = cur.execute(query)
    results = result.fetchall()
    cur.close()
    return results

def pretty_print(rows):
    for i in range(len(rows)):
        row = []
        for ii in range(len(rows[i])):
            item = rows[i][ii]
            if item == "Brandweer":
                item = "\033[31m" + item + "\033[0m"
            elif item == "Ambulance":
                item = "\033[32m" + item + "\033[0m"
            elif item == "Politie":
                item = "\033[34m" + item + "\033[0m"

            if ii == 2: # Region
                item = "\033[33m" + item + "\033[0m"
            elif ii == 5: # Details
                item = "\033[1m" + item + "\033[0m"
            row.append(item)
        rows[i] = row
    print(tabulate(rows))

# results = query_database("""SELECT * FROM messages WHERE capcodes NOT NULL"""))
# results = query_database("""SELECT * FROM messages WHERE type='Brandweer'""")

def main(argv):
    # Get most recent message
    results = query_database("""SELECT MAX(date_time), type, region, priority, postcode, details
                                FROM messages
                            """)
    print('\nMost recent message')
    pretty_print(results)

    # Get first message
    results = query_database("""SELECT MIN(date_time), type, region, priority, postcode, details
                                FROM messages
                            """)
    print('\nFirst message')
    pretty_print(results)

    # Count all call types
    results = query_database("""SELECT type, COUNT(*)
                                FROM messages
                                GROUP BY type
                            """)
    print('\nNumber of calls per type')
    pretty_print(results)

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
    pretty_print(results)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
