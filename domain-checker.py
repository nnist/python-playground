# TODO Length argument
# TODO Top level domain argument
# TODO Chars argument

from tqdm import *
import getopt
import sys

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hl:",["length="])
    except getopt.GetoptError:
        print('usage: domain-checker.py -l <length>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: domain-checker.py -l <length>')
            sys.exit()
        elif opt in ("-l", "--length"):
            length = int(arg)

    # Build list of tuples containing alphabet
    probs = ()
    for i in range(length):
        probs += (string.ascii_lowercase,)

    # Build list of domains
    domains = []
    for prob in itertools.product(*probs):
        print(prob)
        domains += ''.join(prob)

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
