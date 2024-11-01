from common import *
from threading import Thread, Event
import os
import psutil


exit_event = Event()


def main():
  if len(sys.argv) != 4:
    sys.exit('Pass ip and 2 ports')

  ip, port1, port2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

  try:
    calc = Thread(target=calculator, args=(ip, port1), daemon=True)
    cpu_usg = Thread(target=cpu_usage, args=(ip, port2), daemon=True)

    calc.start()
    cpu_usg.start()

    while True:
      pass
  except KeyboardInterrupt:
    pass

  exit_event.set()

  calc.join()
  cpu_usg.join()


# calculator service

def calculator(ip, port):
  sock = socket.create_server((ip, port))
  sock.settimeout(1)

  def calculator_handler(conn, addr):
    try:
      req = recv(conn)
      print(f'Received {req} from {addr}')

      rsp = calculator_rsp(req)
      send(conn, rsp)
      print(f'Sent {rsp} to {addr}')
    except OSError as e:
      print(e)

    conn.close()

  def calculator_rsp(req):
    rsp = { 'status': 0 }
    try:
      req = json.loads(req)
      expr = f'{req["a"]} {req["op"]} {req["b"]}'

      rsp['result'] = eval(expr)
    except Exception as e:
      rsp['status'] = 1
      rsp['result'] = str(e)

    return json.dumps(rsp)
    

  while not exit_event.is_set():
    # try to accept connections with timeout
    # so that thread has a chance to terminate
    conn, addr = None, None
    try:
      conn, addr = sock.accept()
      print(f'{addr} connected to calculator service')
    except TimeoutError:
      continue

    handler = Thread(target=calculator_handler, args=[conn, addr], daemon=True)
    handler.start()

  sock.close()


# cpu usage service

def cpu_usage(ip, port):
  sock = socket.create_server((ip, port))
  sock.settimeout(1)

  while not exit_event.is_set():
    # try to accept connections with timeout
    # so that thread has a chance to terminate
    conn, addr = None, None
    try:
      conn, addr = sock.accept()
      print(f'{addr} connected to CPU usage service')
    except TimeoutError:
      continue

    usage = psutil.cpu_percent(interval=None)
    try:
      send(conn, usage)
      print(f'Sent {addr} current CPU usage')
    except OSError as e:
      print(e)

    conn.close()

  sock.close()


if __name__ == '__main__':
  main()
