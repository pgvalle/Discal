from common import *
from threading import Thread, Event
import os
import psutil


exit_event = Event()


def main():
  calc = Thread(target=calculator, daemon=True)
  calc.start()

  cpuu = Thread(target=cpu_usage, daemon=True)
  cpuu.start()

  try:
    while True:
      pass
  except KeyboardInterrupt:
    pass

  exit_event.set()
  calc.join()
  cpu_usg.join()


def create_server_socket(ip, port):
  sock = None
  try:
    sock = socket.create_server((ip, port))
    sock.listen()
  except OSError as e:
    print(e)

  return sock


# calculator service

def calculator_respond(req):
  rsp = { 'status': 0 }
  try:
    req = json.loads(req)
    expr = f'{req["a"]} {req["op"]} {req["b"]}'

    rsp['result'] = eval(expr)
  except Exception as e:
    rsp['status'] = 1
    rsp['result'] = str(e)

  return json.dumps(rsp)


def calculator_handler(conn, addr):
  try:
    req = recv(conn)
    print(f'Received {req} from {addr}')

    rsp = calculator_respond(req)
    send(conn, rsp)
    print(f'Sent {rsp} to {addr}')
  except OSError as e:
    print(e)

  conn.close()


def calculator(ip, port):
  sock = create_server(ip, port)
  if sock == None:
    return

  print('Calculator service started')

  while not exit_event.is_set():
    # try to accept connections with timeout
    # so that thread has a chance to terminate
    conn, addr = None, None
    try:
      conn, addr = sock.accept()
      print(f'{addr} connected to calculator service')
    except TimeoutError:
      continue

    handler = Thread(target=calculator_handler, args=(conn, addr), daemon=True)
    handler.start()

  print('Calculator service stopped')
  sock.close()


# cpu usage service

def cpu_usage(ip, port):
  sock = create_server_socket(ip, port)
  if sock == None:
    return

  print('CPU usage service started')

  while not exit_event.is_set():
    # try to accept connections with timeout
    # so that thread has a chance to terminate
    conn, addr = None, None
    try:
      conn, addr = sock.accept()
      print(f'{addr} connected to CPU usage service')
    except TimeoutError:
      continue

    try:
      usage = psutil.cpu_percent(interval=None)
      send(conn, usage)
      print(f'Sent {addr} current CPU usage')
    except OSError as e:
      print(e)

    conn.close()

  print('CPU usage service stopped')
  sock.close()


if __name__ == '__main__':
  main()
