# https://en.wikipedia.org/wiki/Domain_hack

import datetime
import whois
import string
import getopt
import sys
import time
import itertools
import urllib.request
from urllib.error import URLError, HTTPError

def main(argv):
    length_min = 2
    length_max = 4
    tld = ".com"
    dict_file = "dictionary.txt"
    chars = "abcdefghijklmnopqrstuvwxyz"
    delay = 2.0

    try:
        opts, args = getopt.getopt(argv,"hl:L:t:c:f:d:",["length-min=","length-max","tld=", "chars=", "file=", "delay="])
    except getopt.GetoptError:
        print('usage: domain-checker.py -l <min> -L <max> -t <tld> -c <chars> -f <file> -d <delay>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: domain-checker.py -l <min> -L <max> -t <tld> -c <chars> -f <file> -d <delay>')
            sys.exit()
        elif opt in ("-l", "--length-min"):
            length_min = int(arg)
        elif opt in ("-L", "--length-max"):
            length_max = int(arg)
        elif opt in ("-t", "--tld"):
            tld = str(arg)
        elif opt in ("-c", "--chars"):
            chars = str(arg)
        elif opt in ("-f", "--file"):
            dict_file = str(arg)
        elif opt in ("-d", "--delay"):
            delay = float(arg)

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
        # TODO Fix Socket Error: timed out
        try:
            w = whois.whois(domains[i])
            time.sleep(delay)
        except KeyboardInterrupt:
            print('\nInterrupted by user.')
            sys.exit(0)
        except:
            print("\033[32mavailable\033[0m")
            f.write('{} is available\n'.format(domains[i]))
        else:
            if(all(x==None for x in w.values())):
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
