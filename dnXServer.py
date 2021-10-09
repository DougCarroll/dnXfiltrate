#Adapted from on https://code.activestate.com/recipes/491264-mini-fake-dns-server/
#Doug Carroll modified and added to heavily

import socket
import os
import sys

VERSION = '1.0'
USAGE = 'dnXserver  response_ip [command and control port]'

response_ip='127.0.0.1'
server_ip = 'localhost'
server_port = 8123

# Get command line options
if len(sys.argv) > 3:
    print(USAGE)
if len(sys.argv) < 2:
    print(USAGE)
if len(sys.argv) == 2:
    response_ip = sys.argv[1]
if len(sys.argv) == 3:
    response_ip = sys.argv[1]
    server_port = sys.argv[2]

class DNSQuery:
  def __init__(self, query):
    self.query=query
    self.domain=''

    queryType = (ord(query[2]) >> 3) & 15  # Opcode bits
    if queryType == 0:                     # Standard query
      ini=12
      lon=ord(query[ini])
      while lon != 0:
        self.domain+=query[ini+1:ini+lon+1]+'.'
        ini+=lon+1
        lon=ord(query[ini])

  def response(self, ip):
    packet=''
    if self.domain:
      packet+=self.query[:2] + "\x81\x80"                            # Bit 1:    QR: 0=Request, 1=Response
                                                                     # Bit 2-5:  OpCode for Request Type
                                                                     # Bit 6:    AA: 0=From Cache, 1=Authoritative
                                                                     # Bit 7:    TC: 1=Response too large for UDP
                                                                     # Bit 8:    RD: 0=Iterative Response, 1=Recurseive Response
                                                                     # Bit 9:    RA: 1=Server Manages Recursive
                                                                     # Bit 10:   Z: Reserved
                                                                     # Bit 11:   AD: Used by DNSSEC
                                                                     # Bit 12:   CD: Used by DNSSEC
                                                                     # Bit 13-16 Rcode: Error Codes
                                                                     # 10000001 10000000 = 0x81 0x80
      packet+=self.query[4:6] + self.query[4:6] + '\x00\x00\x00\x00' # Questions and Answers Counts
      packet+=self.query[12:]                                        # Original Domain Name Question
      packet+='\xc0\x0c'                                             # Pointer to domain name
      packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
      packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) # 4bytes of IP
      print(packet)
    return packet

if __name__ == '__main__':
  
  print('dsXServer:: domain.query. 60 IN A %s' % response_ip)
  
  udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udps.bind(('',53))

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_address = (server_ip, server_port)
  print('Starting server on %s port %s' % server_address)
  sock.bind(server_address)
  sock.listen(1)
  while True:
      # Wait for connection
      print('Waiting for a connection')
      connection, client_address = sock.accept()
      try:
          print('Connected! Connection from', client_address)
          while 1:
              query, addr = udps.recvfrom(1024)
              p=DNSQuery(query)
              udps.sendto(p.response(response_ip), addr)
              #print('Response to %s : %s -> %s' % (addr[0], p.domain, response_ip))
              connection.send('Response to %s : %s -> %s' % (addr[0], p.domain, response_ip))
          
      except KeyboardInterrupt:
          print('Terminated')
          connection.close()
          udps.close()
