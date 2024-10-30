import sys
import socket
import json

CHUNK = 1024
ENCODING = 'utf-8'

# Blocking accept regardless of socket.setblocking.
# With this only recv and send are blocking.
def blocking_accept(sock):
  while True:
    try:
      return sock.accept()
    except TimeoutError:
      pass

def nothrow_send(sock, msg):
  try:
    msg = msg.encode(ENCODING)
    return sock.send(msg)
  except OSError:
    print(e)

def nothrow_recv(sock):
  try:
    msg = sock.recv(CHUNK)
    return msg.decode(ENCODING)
  except OSError:
    print(e)
