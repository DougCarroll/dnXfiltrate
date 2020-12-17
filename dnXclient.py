import socket

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