from common import *


def main():
  try:
    while True:
      a = float(input('a: '))
      op = input('op: ')
      b = float(input('b: '))

      sock = socket.create_connection((BALANCER_IP, BALANCER_PORT))

      req = json.dumps({ 'a': a, 'b': b, 'op': op })
      send(sock, req)

      rsp = recv(sock)
      rsp = json.loads(rsp)
      print('Response:', rsp)

      sock.close()
  except KeyboardInterrupt:
    pass
  except Exception as e:
    print(e)


if __name__ == '__main__':
  main()
