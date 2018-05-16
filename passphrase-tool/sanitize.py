import argparse
import sys, os

# TODO Remove words with numbers or special characters in them

def sanitize(filename):
    wordlist = []
    
    with open(filename, 'r') as lines:
        unique = []
        for line in lines:
            if line not in unique and len(line) > 3:
                unique += [line.lower()]
    
        for i in range(len(unique)):
            word = unique[i].strip()
            if i < len(unique):
                word = word[0:-1]
    
            wordlist.append(word)
    
    with open(filename + ".bak", 'w') as of:
        of.write(filename + ".bak")
    
    with open(filename, 'w') as of:
        of.write("".join(unique))

def main(argv):
    parser = argparse.ArgumentParser(
        description="""Sanitize wordlist. Remove leading and trailing spaces, words less than 3 chars and make all words lowercase."""
    )
    parser.add_argument("filename")
    args = parser.parse_args()
    sanitize(args.filename)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0) # pylint: disable=protected-access
