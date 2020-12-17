import socket
import os
import sys

VERSION = '1.0'
USAGE = 'dnXclient <IP address of remote server> <port number of remote server>'

serverIP = 'localhost'
serverPort = 8123

# Get command line options
if len(sys.argv) > 3:
    print(USAGE)
if len(sys.argv) == 2:
    serverIP = sys.argv[1]
if len(sys.argv) == 3:
    serverIP = sys.argv[1]
    serverPort = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (serverIP, serverPort)
print('Connecting to %s port %s' % server_address)
sock.connect(server_address)
try:
    
    while True:
        data = sock.recv(64)     
        print(data)

finally:
    print('Finished')
    sock.close()