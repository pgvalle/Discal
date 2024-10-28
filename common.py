import sys, site, socket, json

CHUNK = 1024
ENCODING = 'utf-8'

def send(sock, msg):
  encoded_msg = msg.encode(ENCODING)
  return sock.send(encoded_msg)

def recv(sock):
  encoded_msg = sock.recv(CHUNK)
  return encoded_msg.decode(ENCODING)
