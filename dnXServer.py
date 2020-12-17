#Based on https://code.activestate.com/recipes/491264-mini-fake-dns-server/

import socket

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
      packet+=self.query[:2] + "\x81\x80"
      packet+=self.query[4:6] + self.query[4:6] + '\x00\x00\x00\x00' # Questions and Answers Counts
      packet+=self.query[12:]                                        # Original Domain Name Question
      packet+='\xc0\x0c'                                             # Pointer to domain name
      packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
      packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) # 4bytes of IP
    return packet

if __name__ == '__main__':
  response_ip='162.0.228.2'
  print('dsXServer:: domain.query. 60 IN A %s' % response_ip)
  
  udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udps.bind(('',53))

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_address = ('localhost', 8123)
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