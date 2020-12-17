import socket

VERSION = '1.0'
USAGE = 'dnXclient -i <IP address of remote server> -p <port number of remote server>'

# Get command line options
options, arguments = getopt.getopt(
    sys.argv[1:],
    'vhip:',
    ['version", "help", "ipserver=", "portserver=']
)
ipserver = 'localhost'
portserver = '8123'
for o, a in options:
    if o in ("-v", "--version"):
        print(VERSION)
        sys.exit()
    if o in ("-h", "--help"):
        print(USAGE)
        sys.exit()
    if o in ("-i", "--ipserver="):
        ipserver = a
    if o in ("-p", "--portserver"):
        portserver = a
if not arguments or len(arguments) > 4:
    raise SystemExit(USAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8123)
print('Connecting to %s port %s' % server_address)
sock.connect(server_address)
try:
    
    while True:
        data = sock.recv(64)     
        print(data)

finally:
    print('Finished')
    sock.close()