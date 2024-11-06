from common import *


if len(sys.argv) != 3:
  sys.exit('Pass ip and port')


ip, port = sys.argv[1:]


def main():
  try:
    global port
    port = int(port)

    while True:
      a = float(input('a: '))
      op = input('op: ')
      b = float(input('b: '))

      sock = socket.create_connection((ip, port))

      req = json.dumps({ 'a': a, 'b': b, 'op': op })
      send(sock, req)

      rsp = recv(sock)
      rsp = json.loads(rsp)
      print('Response:', rsp)

      sock.close()
  except KeyboardInterrupt:
    print('bye...')
  except Exception as e:
    print(f'error: {e}')


if __name__ == '__main__':
  main()
