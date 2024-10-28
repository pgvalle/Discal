from common import *
import psutil, threading


# must have ip, port1 and port2
if len(sys.argv) != 4:
  print('Pass ip, calc_port and cpu_port as arguments!')
  print('Example: python server.py 127.0.0.1 5000 5001')
  quit()

# port1 is the calculator service port. port2 is the cpu usage service port
ip, port1, port2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])


# calculator service (main)
  
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock1.bind((ip, port1))
sock1.listen()

def calculator_log(msg):
  print('calculator:', msg)

def calculator():
  while True:
    sock, addr = sock1.accept()
    calculator_log(f'Received connection from {addr}')

    req = recv(sock)
    calculator_log(f'Message received: {req}')

    # calculate ...

    rsp = json.dumps({ 'status': 0, 'result': 0 })
    send(sock, rsp)


# cpu usage service (auxiliar)

sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cpu usage
sock2.bind((ip, port2))
sock2.listen()

def cpu_usage_log(msg):
  print('cpu usage:', msg)

def cpu_usage():
  while True: 
    sock, addr = sock2.accept()
    cpu_usage_log(f'Received connection from {addr}')

    usage = psutil.cpu_percent(interval=None)
    cpu_usage_log(f'Current cpu usage is {usage}')

    msg = str(usage)
    send(sock, msg)


cpu_usage_thread = threading.Thread(target=cpu_usage)
cpu_usage_thread.start()

try:
  calculator()
except KeyboardInterrupt:
  sock1.close()
  calculator_log('Bye')
except Exception as e:
  print(e)

try:
  cpu_usage_thread.join()
except KeyboardInterrupt:
  sock2.close()
  cpu_usage_log('Bye')
except Exception as e:
  print(e)
