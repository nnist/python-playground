import itertools
import urllib.request
import os

print("Downloading Omegle chat logs...")

f = str(0)

url = "http://l.omegle.com/"

numberofImagesWanted = 10

for j in range(0, numberofImagesWanted):
    stuff = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    for L in range(5, 10):
    	for i in itertools.combinations_with_replacement(stuff, L):
    		finalurl = url + str(''.join(i)) + ".png"
    		j = j + 1
    		if j == numberofImagesWanted + 1:
    			exit(0)

    		omRequest = urllib.request.Request(finalurl)
    		try:
    			req = urllib.request.urlopen(omRequest)
    			print('Downloaded', finalurl)
    			path = "images"
    			if not os.path.exists(path):
    				os.makedirs(path)
    			filename = os.path.join(path, str(''.join(i)) + ".png")
    			output = open(filename, "wb")
    			output.write(req.read())
    			output.close()
    		except urllib.error.URLError as e:
    			print('Failed to download', finalurl, e)
