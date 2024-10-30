from common import *
import os
import signal
import psutil


def sigchld_handler(num, bruh):
  os.wait()


# Entrypoint

def main():
  if len(sys.argv) != 4:
    print('Pass ip, calc_port and cpu_port as arguments!')
    print('Example: python server.py 127.0.0.1 5000 5001')
    return

  ip, port1, port2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

  # This fixes zombie child processes never terminating
  signal.signal(signal.SIGCHLD, sigchld_handler)

  try:
    if os.fork() == 0:
      cpu_usage(ip, port2)
    else:
      calculator(ip, port1)
  except KeyboardInterrupt:
    pass

# calculator service

def calculator(ip, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(1)
  sock.bind((ip, port))
  sock.listen()

  def calculator_rsp(req):
    rsp = { 'status': 0 }
    try:
      expr = f'{req["a"]} {req["op"]} {req["b"]}'

      rsp['result'] = eval(expr)
    except Exception as e:
      rsp['status'] = 1
      rsp['result'] = str(e)

    return rsp

  while True:
    conn, addr = blocking_accept(sock)
    print(f'Received connection from {addr} to calculate something.')

    if os.fork() > 0:  # Parent keeps listening for connections
      continue

    try:
      req = conn.recv(CHUNK)
      req = req.decode(ENCODING)
      req = json.loads(req)
      print(f'Received {req} from {addr}.')
     
      rsp = calculator_rsp(req)
      rsp = json.dumps(rsp)
      rsp = rsp.encode(ENCODING)
      conn.send(rsp)
      print(f'Responded {addr} with {rsp}.')
    except TimeoutError:
      print('Socket timed out')

    conn.close()
    return


# cpu usage service

def cpu_usage(ip, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(1)
  sock.bind((ip, port))
  sock.listen(0)

  while True:
    conn, addr = blocking_accept(sock)
    print(f'Received connection from {addr} to get CPU usage.')

    try:
      usage = psutil.cpu_percent(interval=None)
      usage = str(usage)
      usage = usage.encode(ENCODING)
      conn.send(usage)
      print(f'Sent current CPU usage ({usage}%).')
    except TimeoutError:
      print('Socket timed out')

    conn.close()


if __name__ == '__main__':
  main()
