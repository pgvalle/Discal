from common import *
import random


def main():
  if len(sys.argv) != 3:
    print('Pass ip and port')
    return

  try:
    addr = (sys.argv[1], int(sys.argv[2]))

    while True:
      v1 = random.randint(0, 100)
      op = random.choice(VALID_OPERATIONS)
      v2 = random.randint(0, 100)

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
      
      if sock:
        sock.close()
  except KeyboardInterrupt:
    print('bye...')


if __name__ == '__main__':
  main()
