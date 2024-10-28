from common import *

if len(sys.argv) != 3:
  print('Pass ip and port as arguments!')
  print('Example: python client.py 127.0.0.1 5000')
  quit()

ip, port = sys.argv[1], int(sys.argv[2])

def loop():
  try:
    while True:
      a = float(input('type first number: '))
      op = input('type operation: ')
      b = float(input('type second number: '))

      req = json.dumps({ 'a': a, 'b': b, 'op': op })

      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4 tcp socket
      sock.connect((ip, port))
      send(sock, req)

      rsp = recv(sock)
      print(rsp)

      sock.close()
  except KeyboardInterrupt:
    print('\nBye...')
  except Exception as e:
    print(e)

loop()
