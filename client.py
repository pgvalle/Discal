from common import *


def validate_args():
  if len(sys.argv) != 3:
    sys.exit('Pass an ip and a port')

  port = sys.argv[2]
  try:
    port = int(port)
  except ValueError:
    sys.exit('Could not convert port to number')

  ip = sys.argv[1]
  return ip, port


def main():
  ip, port = validate_args()

  try:
    while True:
      a = float(input('First number: '))
      op = input('Operation: ')
      b = float(input('Second number: '))

      req = json.dumps({ 'a': a, 'b': b, 'op': op })

      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4 tcp socket
      sock.connect((ip, port))
      send(sock, req)

      rsp = recv(sock)
      rsp_dict = json.loads(rsp)
      print('Response:', rsp_dict)

      sock.close()
  except KeyboardInterrupt:
    pass
  except Exception as e:
    print(e)


if __name__ == '__main__':
  main()
