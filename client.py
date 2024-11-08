from common import *


def main():
  if len(sys.argv) != 3:
    print('Pass ip and port')
    return

  try:
    addr = (sys.argv[1], int(sys.argv[2]))

    while True:
      v1 = input('v1: ')
      op = input('op: ')
      v2 = input('v2: ')

      sock = None
      try:
        sock = socket.create_connection(addr)
        req = { 'v1': v1, 'op': op, 'v2': v2 }
        req = json.dumps(req)
        send(sock, req)

        rsp = recv(sock)
        print(f'response: {rsp}')
      except OSError as e:
        print(f'error: {e}')
        continue

      sock.close()
  except KeyboardInterrupt:
    print('bye...')


if __name__ == '__main__':
  main()
