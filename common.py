import sys
import socket
import json


BALANCER_IP = 'localhost'
BALANCER_PORT = 1536

IP1 = 'localhost'
CALC_PORT1 = 1537
CPUU_PORT1 = 1538

IP2 = 'localhost'
CALC_PORT2 = 1539
CPUU_PORT2 = 1540

CHUNK = 1024
ENCODING = 'utf-8'

TIMEOUT = 1
CPUU_FETCH_INTERVAL = 1


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
