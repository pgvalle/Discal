import sys
import socket
import json

CHUNK = 1024
ENCODING = 'utf-8'

# Blocking accept regardless of socket.setblocking.
# With this only recv and send are blocking.
def accept_no_timeout(sock):
  while True:
    try:
      return sock.accept()
    except TimeoutError:
      pass

