from common import *
import os
import signal
import psutil

def sigchld_handler(num, bruh):
  print('A child process terminated')
  os.wait()

def main():
  if len(sys.argv) != 4:
    print('You must pass exactly 3 arguments: ip, port1 and port2.')
    print('port1 is for the calculator. port2 is for the cpu usage.')
    print('Example: python server.py 127.0.0.1 5000 5001')
    return

  ip, port1, port2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
  sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # This fixes zombie child processes never terminating
  signal.signal(signal.SIGCHLD, sigchld_handler)

  try:
    if os.fork() == 0:
      cpu_usage(sock2)
    else:
      calculator(sock1)
  except KeyboardInterrupt:
    pass
  except Exception as e:
    print(e)
  finally:
    sock1.close()
    sock2.close()


# calculator service

def calculator(sock):
  sock.settimeout(1)
  sock.bind((ip, port))
  sock.listen()

  def calculator_rsp(req):
    rsp = { 'status': 0 }
    try:
      req = req.decode(ENCODING)
      req = json.loads(req)
    
      expr = f'{req["a"]} {req["op"]} {req["b"]}'

      rsp['result'] = eval(expr)
    except Exception as e:
      rsp['status'] = 1
      rsp['result'] = str(e)

    rsp = json.dumps(rsp)
    rsp = rsp.encode(ENCODING)
    return rsp

  while True:
    try:
      conn, addr = accept_no_timeout(sock)
      print(f'Received connection from {addr} to calculate something.')

      pid = os.fork()
      if pid > 0:  # Parent keeps listening for connections.
        continue

      req = conn.recv(CHUNK)
      print(f'Received {req} from {addr}.')

      rsp = calculator_rsp(req)
      conn.send(rsp)
      print(f'Sent {rsp} to {addr}.')

    except TimeoutError:
      print('Socket timeout')
    except OSError:
      print('Unknown error')
    finally:
      conn.close()

    if pid == 0:
      return


# cpu usage service

def cpu_usage(sock):
  sock.settimeout(1)
  sock.bind((ip, port))
  sock.listen()

  while True:
    try:
      conn, addr = accept_no_timeout(sock)
      print(f'Received connection from {addr} to get CPU usage.')

      usage = psutil.cpu_percent(interval=None)
      msg = str(usage)
      msg = msg.encode(ENCODING)
      conn.send(msg)
      print(f'Sent CPU usage ({usage}%) to {addr}.')
    except TimeoutError:
      print('Socket timeout')
    except OSError:
      print('Unknown error')
    finally:
      conn.close()


if __name__ == '__main__':
  main()
