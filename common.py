import socket
import json
import sys
import time

from threading import Thread, Event


CHUNK = 1024
ENCODING = 'utf-8'

TIMEOUT = 1
CPUU_FETCH_INTERVAL = 1


def send(sock, msg):
  msg = str(msg)
  msg = msg.encode(ENCODING)
  return sock.send(msg)

def recv(sock):
  msg = sock.recv(CHUNK)
  msg = msg.decode(ENCODING)
  return msg
