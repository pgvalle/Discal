from common import *
import psutil, threading, signal


# must have ip, port1 and port2
if len(sys.argv) != 4:
  print('Pass ip, calc_port and cpu_port as arguments!')
  print('Example: python server.py 127.0.0.1 5000 5001')
  quit()

# port1 is the calculator service port. port2 is the cpu usage service port
ip, port1, port2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])


# calculator service

l1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
l1.bind((ip, port1))
l1.listen()

def calculate(req):
    try:
      req_dict = json.loads(req)
      a = req_dict['a']
      b = req_dict['b']
      op = req_dict['op']
      result = eval(f'{a} {op} {b}')

      return { 'status': 0, 'result': result }
    except Exception as e:
      print(e)
      return { 'status': 1, 'result': str(e) }

def calc():
  while True:
    conn, addr = l1.accept()
    print('Calculator: Received connection from', addr)

    req = recv(conn)
    print('Calculator: Message received:', req)

    rsp_dict = calculate(req)
    rsp = json.dumps(rsp_dict)
    send(conn, rsp)

    conn.close()

calc_th = threading.Thread(target=calc)
calc_th.daemon = True
calc_th.start()


# cpu usage service

l2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
l2.bind((ip, port2))
l2.listen()

def cpu_usg():
  while True:
    conn, addr = l2.accept()
    print('CPU Usage: Received connection from', addr)

    usage = psutil.cpu_percent(interval=None)
    print(f'CPU Usage: usage is {usage}%')

    msg = str(usage)
    send(conn, msg)

    conn.close()

cpu_usg_th = threading.Thread(target=cpu_usg)
cpu_usg_th.daemon = True
cpu_usg_th.start()


try:
  calc_th.join()
  cpu_usg_th.join()
except KeyboardInterrupt:
  l1.close()
  l2.close()
  print('\nBye...')
