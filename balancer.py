from common import *

'''guardar registros de tempos em tempos (na faixa de segundos)
do uso da cpu em cada servidor. Depois fazer algum cálculo em cima
desses valores pra decidir qual servidor vai ser usado'''

'''Threads ou Forks para tratar as conexões com os clientes???'''
from common import *
from threading import Thread, Event
import datetime
import time


exit_event = Event()

cpuu_hist1 = []
cpuu_hist2 = []


def main():
  try:
    sock = socket.create_server((BALANCER_IP, BALANCER_PORT))

    listener = Thread(target=listen2clients, args=[sock], daemon=True)
    cpuu1 = Thread(target=query_cpuu1, daemon=True)
    cpuu2 = Thread(target=query_cpuu2, daemon=True)

    listener.start()
    cpuu1.start()
    cpuu2.start()

    while True:
      pass
  except KeyboardInterrupt:
    sock.close()
    exit_event.set()
    listener.join()
    cpuu1.join()
    cpuu2.join()
  except OSError as e:
    print(e)


a = False
def decide_server():
  global a
  a = not a
  if a:
    return IP1, CALC_PORT1
  return IP2, CALC_PORT2


def query_cpuu1():
  while not exit_event.is_set():
    conn = None
    try:
      conn = socket.create_connection((IP1, CPUU_PORT1), timeout=1)
    except OSError as e:
      print(e)
      continue

    try:
      usage = recv(sock)

      usage = float(usage)
      date = datetime.now()
      cpuu_hist1.append((usage, date))
    except OSError as e:
      print(e)

    conn.close()
    time.sleep(1)


def query_cpuu2():
  while not exit_event.is_set():
    conn = None
    try:
      conn = socket.create_connection((IP2, CPUU_PORT2), timeout=1)
    except OSError as e:
      print(e)
      continue

    try:
      usage = recv(sock)

      usage = float(usage)
      date = datetime.now()
      cpuu_hist2.append((usage, date))
    except OSError as e:
      print(e)

    conn.close()
    time.sleep(1)


def handle_client(conn, addr):
  sock = None
  try:
    ip, port = decide_server()
    sock = socket.create_connection((ip, port))
  except OSError as e:
    conn.close()
    print(e)
    return

  try:
    msg = recv(conn)
    send(sock, msg)
    msg = recv(sock)
    send(conn, msg)
  except OSError as e:
    print(e)

  sock.close()
  conn.close()


def listen2clients(sock):
  while not exit_event.is_set():
    try:
      conn, addr = sock.accept()
    except TimeoutError:
      continue

    handler = Thread(target=handle_client, args=(conn, addr), daemon=True)
    handler.start()


if __name__ == '__main__':
  main()
