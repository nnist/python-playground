# https://en.wikipedia.org/wiki/Domain_hack

import datetime
import argparse
import sys
import os
import time
import whois

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
        print("[" + str(i+1) + "/" + str(len(domains)) + "] " + domains[i],
              end=" -> ", flush=True)
        # TODO Fix Socket Error: timed out
        try:
            w = whois.whois(domains[i])
            time.sleep(delay)
        except KeyboardInterrupt:
            print('\nInterrupted by user.')
            sys.exit(0)
        except Exception as ex:
            print("\033[32mavailable\033[0m")
            f.write('{} is available\n'.format(domains[i]))
        else:
            if all(x == None for x in w.values()):
                print("\033[33munknown\033[0m")
                f.write('{} might be available\n'.format(domains[i]))
            else:
                print("\033[31mregistered\033[0m")
    
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
