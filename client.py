from common import *


def main():
  if len(sys.argv) != 3:
    print('You must pass exactly 2 arguments: ip and port.')
    print('Example: python client.py 127.0.0.1 5000')
    return

  ip, port = sys.argv[1], int(sys.argv[2])

  while True:
    try:
      a = float(input('First number: '))
      op = input('Operation: ')
      b = float(input('Second number: '))

      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(1)
      sock.connect((ip, port))

      req = json.dumps({ 'a': a, 'b': b, 'op': op })
      req = req.encode(ENCODING)
      sock.send(req)
      print(f'Sent {req}.')

      rsp = sock.recv(CHUNK)
      print(f'Received {rsp}.')
      rsp = rsp.decode(ENCODING)
      rsp = json.loads(rsp)
    except TimeoutError:
      print('Socket timeout')
    except OSError:
      print('Unknown error')
    except Exception as e:
      print(e)

    sock.close()


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  except Exception as e:
    print(e)
