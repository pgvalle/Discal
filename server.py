from common import *
import os
import psutil


# must have ip, port1 and port2
if len(sys.argv) != 4:
  print('Pass ip, calc_port and cpu_port as arguments!')
  print('Example: python server.py 127.0.0.1 5000 5001')
  quit()

# port1 is the calculator service port. port2 is the cpu usage service port
ip, port1, port2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])


# calculator service

def calculate(req):
    try:
      req_dict = json.loads(req)
      a = req_dict['a']
      b = req_dict['b']
      op = req_dict['op']
      result = eval(f'{a} {op} {b}')

      return { 'status': 0, 'result': result }
    except Exception as e:
      return { 'status': 1, 'result': str(e) }

def calculator():
  l = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  l.bind((ip, port1))
  l.listen()

  try:
    while True:
      conn, addr = l.accept()

      # Child process. Receive request, respond then exit.
      if os.fork() == 0:
        req = recv(conn)
        print(f'Received {req} from {addr}', end='. ')

        rsp_dict = calculate(req)
        rsp = json.dumps(rsp_dict)
        print(f'Responding with {rsp}.')

        # Network errors may happen.
        try:
          send(conn, rsp)
        except Exception as e:
          print(e)

        conn.close()
        break
  except KeyboardInterrupt:
    l.close()


# cpu usage service

def cpu_usage():
  l = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  l.bind((ip, port2))
  l.listen()

  try:
    while True:
      conn, addr = l.accept()

      # Child process. Send cpu usage then exit.
      if os.fork() == 0:
        usage = psutil.cpu_percent(interval=None)
        print(f'Telling {addr} CPU usage now is {usage}%')

        # Network errors may happen.
        try:
          send(conn, str(usage))
        except Exception as e:
          print(e)

        conn.close()
        break
  except KeyboardInterrupt:
    l.close()


if __name__ == '__main__':
  if os.fork() == 0:
    cpu_usage()
  else:
    calculator()
