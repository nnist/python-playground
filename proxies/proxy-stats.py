import sqlite3
from tabulate import tabulate
from datetime import datetime, timedelta

def query_database(query):
    conn = sqlite3.connect('data/proxies.db')
    cur = conn.cursor()
    result = cur.execute(query)
    results = result.fetchall()
    cur.close()
    return results

# Number of entries
results = query_database("""SELECT COUNT(*)
                            FROM proxies
                        """)
print('Number of proxies:', results[0][0])

# Proxies that have been seen
results = query_database("""SELECT COUNT(*)
                            FROM proxies
                            WHERE last_seen IS NOT NULL
                        """)
print('Proxies that have been seen:', results[0][0])

# Proxies that have never been seen
results = query_database("""SELECT COUNT(*)
                            FROM proxies
                            WHERE last_seen IS NULL
                        """)
print('Proxies that have never been seen:', results[0][0])

# HTTP proxies
results = query_database("""SELECT COUNT(*)
                            FROM proxies
                            WHERE proxy_type IS 'http'
                        """)
print('HTTP proxies:', results[0][0])

# HTTPS proxies
results = query_database("""SELECT COUNT(*)
                            FROM proxies
                            WHERE proxy_type IS 'https'
                        """)
print('HTTPS proxies:', results[0][0])

# Some recently seen proxies
results = query_database("""SELECT ip, port, proxy_type, status, last_seen
                            FROM proxies
                            WHERE last_seen IS NOT NULL AND status IS 200
                            ORDER BY last_seen DESC
                            LIMIT 10
                        """)
print('\nSome recently seen proxies:')
print(tabulate(results))
