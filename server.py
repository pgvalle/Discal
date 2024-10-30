from common import *
import os
import signal
import psutil


def sigchld_handler(num, bruh):
  os.wait()


# Entrypoint

def main():
  # Must have ip, port1 and port2
  if len(sys.argv) != 4:
    print('Pass ip, calc_port and cpu_port as arguments!')
    print('Example: python server.py 127.0.0.1 5000 5001')
    return

  # Port1 is for calculator service. Port2 is for the cpu usage service.
  ip, port1, port2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

  # This fixes zombie child processes never terminating
  signal.signal(signal.SIGCHLD, sigchld_handler)

  # catch KeyboardInterrupt from both services
  try:
    if os.fork() == 0:  # Child. CPU usage service.
      cpu_usage(ip, port2)
    else:  # Parent. Calculator service.
      calculator(ip, port1)
  except KeyboardInterrupt:
    pass

# calculator service

def calculator(ip, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(1)
  sock.bind((ip, port))
  sock.listen()

  # This fixes zombie child processes never terminating
  signal.signal(signal.SIGCHLD, sigchld_handler)

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

  while True:
    conn, addr = accept(sock)
    print(f'Received connection from {addr} to calculate something.')

    if os.fork() == 0:  # Child. Receive request, respond and done.
      req = recv(conn)
      print(f'Received {req} from {addr}.')

      rsp = calculator_rsp(req)
      send(conn, rsp)
      print(f'Responded {addr} with {rsp}.')

      conn.close()
      return


# cpu usage service

def cpu_usage(ip, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(1)
  sock.bind((ip, port))
  sock.listen()

  while True:
    conn, addr = accept(sock)
    print(f'Received connection from {addr} to get CPU usage.')

    if os.fork() == 0:  # Child. Send cpu usage and done.
      usage = psutil.cpu_percent(interval=None)
      usage = str(usage)
      send(conn, usage)
      print(f'Sent {addr} current CPU usage: {usage}%.')

      conn.close()
      return


if __name__ == '__main__':
  main()
