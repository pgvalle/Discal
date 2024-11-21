from common import *


def main():
    if len(sys.argv) < 3:
        print('Pass ip and connection port')
        print('Optionally pass the number of spammers (default=4)')
        return

    num_procs = 4
    try:
        num_procs = int(sys.argv[3])
    except:
        pass

    while num_procs > 1:
        pid = os.fork()
        if pid == 0:
            break
        else:
            num_procs -= 1

    spam(num_procs)


def spam(i):
    print(f'spammer {i}: spamming')

    try:
        addr = (sys.argv[1], int(sys.argv[2]))

        while True:
            v1 = random.randint(0, 10)
            op = random.choice(['+', '-', '*', '/', '**', '%'])
            v2 = random.randint(0, 10)

            sock = None
            try:
                sock = socket.create_connection(addr, timeout=1)
                req = { 'v1': v1, 'op': op, 'v2': v2 }
                req = json.dumps(req)
                send(sock, req)

                rsp = recv(sock)
            except OSError as e:
                print(f'spammer {i}: error: {e}')
            
            if sock:
                sock.close()
    except KeyboardInterrupt:
        print(f'spammer {i}: bye...')
    except Exception as e:
        print(f'spammer {i}: error: {e}')


if __name__ == '__main__':
    main()
