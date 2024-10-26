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

            msg = json.dumps({ 'a': a, 'b': b, 'op': op })
            encoded_msg = msg.encode(ENCODING)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4 tcp socket

            sock.connect((ip, port))
            sock.send(encoded_msg)
            encoded_rsp = sock.recv(CHUNK)
            rsp = rsp.decode(ENCODING)
            sock.close()

            print(f'result: {rsp['result']}')
    except KeyboardInterrupt:
        print('\nBye')
    except Exception as e:
        print(e)

loop()
