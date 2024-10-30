from common import *


if len(sys.argv) != 3:
  print('Pass ip and port as arguments!')
  print('Example: python client.py 127.0.0.1 5000')
  quit()

ip, port = sys.argv[1], int(sys.argv[2])


def main():
  try:
    while True:
      a = float(input('First number: '))
      op = input('Operation: ')
      b = float(input('Second number: '))

      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect((ip, port))

      try:
        req = json.dumps({ 'a': a, 'b': b, 'op': op })
        req = req.encode(ENCODING)
        sock.send(req)

        rsp = sock.recv(CHUNK)
        rsp = rsp.decode(ENCODING)
        rsp = json.loads(rsp)
        print(rsp['result'])
      except TimeoutError:
        print('Socket error')

      sock.close()
  except KeyboardInterrupt:
    pass
  except Exception as e:
    print(e)


if __name__ == '__main__':
  main()
