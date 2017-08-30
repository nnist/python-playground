import datetime

# Append to file
f = open('text.txt', 'a')
f.seek(0, 0) # Go to beginning of file
f.write('{}\n'.format(datetime.datetime.now()))
f.close()

# Read all lines in file
with open('text.txt', 'r') as f:
    for line in f:
        line = line[0:-1] # Remove line break
        print(line)

