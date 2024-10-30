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
    except socket.timeout:
      pass

def send(sock, msg):
  try:
    msg = msg.encode(ENCODING)
    return sock.send(msg)
  except Exception as e:
    print(e)

def recv(sock):
  try:
    msg = sock.recv(CHUNK)
    return msg.decode(ENCODING)
  except Exception as e:
    print(e)
