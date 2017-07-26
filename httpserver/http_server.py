import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()

# Calls a new python command to run a http server, does not appear to need admin rights
# import subprocess
#
# subprocess.call(['python', '-m', 'http.server', '8000', '--bind', '127.0.0.1'])
