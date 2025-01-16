from common import *
import psutil

VALID_OPERATIONS = ['+', '-', '*', '/', '**', '%']

exit_event = Event()  # to cleanly exit threads (properly free ports)

def main():
    if len(sys.argv) < 4:
        print('Pass ip, calc port and cpuu port')
        return

    calc_th = Thread(target=calc, daemon=True)
    cpuu_th = Thread(target=cpuu, daemon=True)

    calc_th.start()
    cpuu_th.start()

    try:
        while not exit_event.is_set():
            pass
    except KeyboardInterrupt:
        print('bye...')

    exit_event.set()
    calc_th.join()
    cpuu_th.join()

# calculator service

def calc_rsp(req):
    def error2int(e):
        chars = list(str(e))
        ords = map(lambda c: ord(c), chars)
        return int(sum(ords) / len(ords))

    try:
        req = json.loads(req)  # json.JSONDecodeError

        # KeyError, ValueError or TypeError
        v1 = float(req['v1'])
        v2 = float(req['v2'])
        op = req['op']

        if not op in VALID_OPERATIONS:
          return json.dumps({
              'status': 1,
              'result': 'invalid operation' })
        
        expr = f'{v1} {op} {v2}'
        print(f'calc: {expr}')
        return json.dumps({
            'status': 0,
            'result': eval(expr) })

    except Exception as e:
        ecode = error2int(e)
        print(f'calc: error {ecode}: {e}')
        return json.dumps({
            'status': ecode,
            'result': str(e) })


def calc_handler(conn):
    try:
        req = recv(conn)
        rsp = calc_rsp(req)
        send(conn, rsp)
    except OSError as e:
        print(f'calc: error: {e}')

    conn.close()


def calc():
    try:
        host, port = sys.argv[1], int(sys.argv[2])
        sock = socket.create_server((host, port))
    except Exception as e:
        print(f'calc: error: {e}')
        print('calc: could not start service')
        exit_event.set()  # the main service can't start, so just quit the program
        return
    
    sock.settimeout(1)
    sock.listen()
    print(f'calc: started on {host}:{port}')

    with cf.ThreadPoolExecutor(max_workers=10) as tpe:
        while not exit_event.is_set():
            # accept connections catching TimeoutError so that the thread may terminate
            try:
                conn, _ = sock.accept()
            except TimeoutError:
                continue

            tpe.submit(calc_handler, conn)

        sock.close()
        print('calc: stopped')


# cpu usage service

def cpuu_handler(conn):
    usage = psutil.cpu_percent()
    try:
        send(conn, usage)
    except OSError as e:
        print(f'cpuu: error: {e}')

    conn.close()

def cpuu():
    try:
        host, port = sys.argv[1], int(sys.argv[3])
        sock = socket.create_server((host, port))
    except Exception as e:
        print(f'cpuu: error: {e}')
        print('cpuu: could not start service')
        return
    
    sock.settimeout(1)
    sock.listen(0)
    print(f'cpuu: listening on {host}:{port}')

    while not exit_event.is_set():
        # accept connections catching TimeoutError so that the thread may terminate
        try:
            conn, _ = sock.accept()
        except TimeoutError:
            continue

        cpuu_handler(conn)

    sock.close()
    print('cpuu: stopped')

if __name__ == '__main__':
    main()
