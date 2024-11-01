import sys
import socket
import json

CHUNK = 1024
ENCODING = 'utf-8'

# Nonblocking accept regardless of socket.setblocking.
# With this only recv and send are blocking.
def accept(sock):
  while True:
    try:
      return sock.accept()
    except TimeoutError:
      pass

def send(sock, msg):
  msg = str(msg)
  msg = msg.encode(ENCODING)
  return sock.send(msg)

def recv(sock):
  msg = sock.recv(CHUNK)
  msg = msg.decode(ENCODING)
  return msg
