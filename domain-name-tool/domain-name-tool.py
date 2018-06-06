# https://en.wikipedia.org/wiki/Domain_hack
# TODO unit tests

import datetime
<<<<<<< HEAD
import string
=======
>>>>>>> d767e9555590e83bea91c07f2bc0224aeab654d3
import argparse
import sys
import os
import time
<<<<<<< HEAD
import itertools
import urllib.request
import subprocess
from urllib.error import URLError, HTTPError
=======
import whois
>>>>>>> d767e9555590e83bea91c07f2bc0224aeab654d3

def main(argv):
    parser = argparse.ArgumentParser(
        description="""Finds domain hacks and tests them to see if
        they are registered."""
    )
    parser.add_argument(
        "min",
        help="Minimum length of domain",
        default=4, type=int
    )
    parser.add_argument(
        "max",
        help="Maximum length of domain",
        default=5, type=int
    )
    parser.add_argument(
        "tld",
        help="Top level domain to use",
        default=".com"
    )
    parser.add_argument(
        "-f",
        help="Dictionary file to use",
        dest="file", default="dictionary.txt"
    )
    parser.add_argument(
        "-d",
        help="Delay",
        dest="delay", default=2.0, type=float
    )

    args = parser.parse_args()
    length_min = args.min
    length_max = args.max
    tld = args.tld
    dict_file = args.file
    chars = "abcdefghijklmnopqrstuvwxyz"
    delay = args.delay

    # Load dictionary, check for lines ending with tld
    domains = []
    with open(dict_file) as f:
        for line in f:
            line = line[0:-1].lower()
            if(line.endswith(tld)) and '-' not in line:
                if(len(line) >= length_min and len(line) <= length_max):
                    domain = line[0:-(len(tld))] + "." + tld
                    domains.append(domain)

    print("Checking %s domains..." % len(domains))

    f = open('log.txt', 'a')
    f.write('\n{}\n'.format(datetime.datetime.now()))

    # Try to get whois information for domain to see if it is available or not
    for i in range(len(domains)):
        print("[" + str(i+1) + "/" + str(len(domains)) + "] " + domains[i], end=" -> ", flush=True)
        try:
            domain = domains[i]
            process = subprocess.run(['whois', domain], timeout=1, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=True, universal_newlines=True)
            output = process.stdout
            if 'NOT AVAILABLE' in output or 'NOT ALLOWED' in output\
            or 'active' in output:
                print("\033[31mnot available\033[0m")
                f.write('{} is not available\n'.format(domains[i]))
            elif 'NOT FOUND' in output or 'AVAILABLE' in output\
            or 'is free' in output:
                print("\033[32mavailable\033[0m")
                f.write('{} is available\n'.format(domains[i]))
            elif 'exceeded' in output:
                print('throttled')
            else:
                print("\033[33munknown\033[0m")
                f.write('{} might be available\n'.format(domains[i]))
                print(process.stdout)
            
            time.sleep(delay)
        except subprocess.CalledProcessError as ex:
            print('error')
        except subprocess.TimeoutExpired as ex:
            print('timeout')
    
    f.close()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
