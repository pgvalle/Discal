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
