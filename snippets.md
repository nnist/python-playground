# Python snippets
## Connect to server
```python
from struct import pack
import socket
 
host = 'localhost'
port = 1337
 
# Create socket and connect
s = socket.socket()
s.connect((host, port))
 
# Receives up to 1024 bytes
data = s.recv(1024)
print "Received data: " + repr(data)
 
# Send response
s.send("Hello World!\n")
 
# Close connection
s.close()
```

## Encoding/decoding/conversions
```python
>>> myb64 = 'I <3 CTF'.encode('base64')
 
>>> myb64
'SSA8MyBDVEY=\n'
 
>>> myb64.decode('base64')
'I <3 CTF'
 
>>> myhex = 'I <3 CTF'.encode('hex')
 
>>> myhex
'49203c3320435446'
 
>>> myhex.decode('hex')
'I <3 CTF'
 
>>> int(0x10)
16
 
>>> int('10', 16)
16
 
>>> int('10', 10)
10
 
>>> int('10', 2)
2
 
>>> int(0x10)
16
 
>>> hex(16)
'0x10'
 
>>> ord('a')
97
```

## Hashing
```python
import hashlib
 
md5 = hashlib.md5()
md5.update('hello world')
 
sha1 = hashlib.sha1()
sha1.update('hello world')
 
sha256 = hashlib.sha256()
sha256.update('hello world')
 
print md5.hexdigest()
print sha1.hexdigest()
print sha256.hexdigest()
```
