# TODO Chars argument

import string
from tqdm import *
import getopt
import sys
import itertools

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hl:t:",["length=","tld="])
    except getopt.GetoptError:
        print('usage: domain-checker.py -l <length> -t <tld>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: domain-checker.py -l <length> -t <tld>')
            sys.exit()
        elif opt in ("-l", "--length"):
            length = int(arg)
        elif opt in ("-t", "--tld"):
            tld = str(arg)

    # Build list of tuples containing alphabet
    probs = ()
    for i in range(length):
        probs += (string.ascii_lowercase,)

    # Build list of domains
    domains = []
    for prob in itertools.product(*probs):
        domain = ''.join(prob) + tld
        domains.append(domain)

    print(domains)
    print("Checking %s domains..." % len(domains))

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
