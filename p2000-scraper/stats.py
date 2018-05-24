"""Show useful information about P2000 items in the database."""
import sqlite3
import os
import sys
import argparse
from datetime import datetime, timedelta
from tabulate import tabulate

def query_database(query):
    """Query the database and return the results in a list."""
    conn = sqlite3.connect('data/p2000.db')
    cur = conn.cursor()
    result = cur.execute(query)
    results = result.fetchall()
    cur.close()
    return results

def pretty_print(rows):
    """Tabulate the input, colorize it and then print it."""
    pretty_rows = []
    for row in enumerate(rows):
        pretty_row = list(row[1])
        for item in enumerate(row[1]):
            colorized_item = item[1]
            if item[1] is None:
                colorized_item = ''
            if item[1] == "Brandweer":
                colorized_item = "\033[31m" + item[1] + "\033[0m" # Red
            elif item[1] == "Ambulance":
                colorized_item = "\033[32m" + item[1] + "\033[0m" # Green
            elif item[1] == "Politie":
                colorized_item = "\033[34m" + item[1] + "\033[0m" # Blue
            elif item[1] == "KNRM":
                colorized_item = "\033[33m" + item[1] + "\033[0m" # Yellow

            if item[0] == 2: # Region
                colorized_item = "\033[33m" + item[1] + "\033[0m" # Yellow
            elif item[0] == 5: # Details
                colorized_item = "\033[1m" + item[1] + "\033[0m" # Bold
            pretty_row[item[0]] = colorized_item
        pretty_rows.append(pretty_row)
    print(tabulate(pretty_rows))

# results = query_database("""SELECT * FROM messages WHERE capcodes NOT NULL"""))
# results = query_database("""SELECT * FROM messages WHERE type='Brandweer'""")

def main(argv):
    """Show useful information about P2000 items in the database."""
    parser = argparse.ArgumentParser(
        description="""Show useful information about the scraped P2000 items."""
    )
    parser.add_argument(
        '-a', '--all', help="Show all information", action='store_true'
    )
    parser.add_argument(
        '-r', '--recent', help="Show most recent message", action='store_true'
    )
    parser.add_argument(
        '-f', '--first', help="Show first message", action='store_true'
    )
    parser.add_argument(
        '--type', help="Show number of calls per type",
        action='store_true'
    )
    parser.add_argument(
        '--region', help="Show number of messages per region",
        action='store_true'
    )
    parser.add_argument(
        '-t', '--time', help="Show all messages of the last TIME minutes",
        default=0, type=int
    )
    args = parser.parse_args(argv)

    if args.all or args.recent:
        # Get most recent message
        results = query_database("""SELECT MAX(date_time), type, region,
                                    priority, postcode, details
                                    FROM messages
                                """)
        print('\nMost recent message')
        pretty_print(results)

    if args.all or args.first:
        # Get first message
        results = query_database("""SELECT MIN(date_time), type, region,
                                    priority, postcode, details
                                    FROM messages
                                """)
        print('\nFirst message')
        pretty_print(results)

    if args.all or args.type:
        # Count all call types
        results = query_database("""SELECT type, COUNT(*)
                                    FROM messages
                                    GROUP BY type
                                """)
        print('\nNumber of calls per type')
        pretty_print(results)

    if args.all or args.region:
        # Return number of messages per region
        results = query_database("""SELECT region, COUNT(*) AS cnt
                                    FROM messages
                                    GROUP BY region
                                    ORDER BY cnt DESC
                                """)
        print('\nNumber of messages per region')
        print(tabulate(results))

    if args.all and not args.time:
        args.time = 30
    if args.time > 0:
        # Get results from entered time period
        date_time = datetime.today() - timedelta(minutes=args.time)
        results = query_database("""SELECT date_time, type, region, priority,
                                    postcode, details FROM messages
                                    WHERE date_time
                                    > '""" + str(date_time) + """'
                                    ORDER BY date_time ASC""")
        print('\nAll messages of last', args.time, 'minutes (' +
              str(len(results)), 'total)')
        pretty_print(results)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0) # pylint: disable=protected-access
