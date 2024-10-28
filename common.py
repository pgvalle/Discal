import sys, site, socket, json

MATH_ERROR = 1
UNKNOWN_ERROR = 2

CHUNK = 1024
ENCODING = 'utf-8'

def send(sock, msg):
  encoded_msg = msg.encode(ENCODING)
  return sock.send(encoded_msg)

def recv(sock):
  encoded_msg = sock.recv(CHUNK)
  return encoded_msg.decode(ENCODING)
