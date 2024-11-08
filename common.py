import socket
import json
import sys
import time
from threading import Thread, Event


VALID_OPERATIONS = ['+', '-', '*', '/', '**', '%']

CHUNK = 1024
ENCODING = 'utf-8'


def send(sock, msg):
  msg = str(msg)
  msg = msg.encode(ENCODING)
  return sock.send(msg)

def recv(sock):
  msg = sock.recv(CHUNK)
  msg = msg.decode(ENCODING)
  return msg
