from common import *
import random
import signal
import os
import math


def main():
  if len(sys.argv) < 3:
    print('Pass ip, and port.')
    print('Optionally, pass the number of spammer procs (default=5).')
    return

  num_childs = 4
  try:
    num_childs = int(sys.argv[3]) - 1
  except:
    pass

  while num_childs > 0:
    pid = os.fork()
    if pid == 0:
      break
    else:
      num_childs -= 1

  spam(num_childs)


def spam(i):
  print(f'spammer {i}: spamming')

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
    print(f'spammer {i}: bye...')
  except Exception as e:
    print(e)


if __name__ == '__main__':
  main()
