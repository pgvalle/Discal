from common import *

# (host, calculator_port, cpu_usage_port)
SERVERS = [
    ('localhost', 1062, 1536),
    #('localhost', 1064, 1538),
    #('localhost', 1065, 1539),
    ('localhost', 1063, 1537) ]

CPUU_INTERVAL = len(SERVERS)  # seconds

exit_event = Event()
servers_cpuu = []
rrl = []  # round robin list
rri = 0  # round robing index

def main():
    if len(sys.argv) < 3:
        print('Pass ip and listening port')
        return

    cpuu_ths = []

    for i in range(len(SERVERS)):
        cpuu_th = Thread(target=cpuu, args=[i], daemon=True)
        cpuu_th.start()

        cpuu_ths.append(cpuu_th)
        servers_cpuu.append(0)
        rrl.append(True)

        time.sleep(0.25)

    listener_th = Thread(target=listen_to_clients, daemon=True)
    listener_th.start()

    try:
        while not exit_event.is_set():
            pass
    except KeyboardInterrupt:
        print('bye...')

    exit_event.set()

    for cpuu_th in cpuu_ths:
        cpuu_th.join()
    listener_th.join()

def decide_server():
    global servers_cpuu, rrl, rri

    avg_cpuu = sum(servers_cpuu) / len(servers_cpuu)
    cpuu_deviations = list(map(lambda x: x - avg_cpuu, servers_cpuu))

    for i in range(len(SERVERS)):
        rrl[i] = cpuu_deviations[i] < 5

    ip, calc_port, _ = SERVERS[rri]

    rri += 1
    rri %= len(rrl)
    while not rrl[rri]:
        rri += 1
        rri %= len(rrl)

    return ip, calc_port

# cpuu querier

def cpuu(i):
    host, _, port = SERVERS[i]

    while not exit_event.is_set():
        start = time.time()
        cconn = None  # server connection
        try:
            cconn = socket.create_connection((host, port), timeout=1)
            usage = recv(cconn)
            usage = float(usage)
            print(f'{host}:{port} is using {usage}% of cpu')

            servers_cpuu[i] = usage
        except OSError as e:
            servers_cpuu[i] = None  # force server to be removed from rr
            print(f'{host}:{port} : {e}')

        if cconn:
            cconn.close()

        delta = time.time() - start
        if delta < CPUU_INTERVAL:
            time.sleep(CPUU_INTERVAL - delta)


def handle_client(cconn):
    sconn = None
    try:
        addr = decide_server()
        sconn = socket.create_connection(addr)

        msg = recv(cconn)
        send(sconn, msg)
        msg = recv(sconn)
        send(cconn, msg)
    except OSError as e:
        print(f'client handler: error: {e}')

    if sconn:
        sconn.close()
    cconn.close()


def listen_to_clients():
    sock = None
    host, port = None, None
    try:
        host, port = sys.argv[1], int(sys.argv[2])
        sock = socket.create_server(host, port)
    except Exception as e:
        print(f'client listener: error: {e}')
        print('client listener: could not start')
        exit_event.set()  # main service can't start, then exit program
        return

    sock.settimeout(1)
    sock.listen()
    print(f'client listener: listening on {host}:{port}')

    with cf.ThreadPoolExecutor(max_workers=10) as tpe:
        while not exit_event.is_set():
            cconn, caddr = None, None  # client connection and address
            try:
                cconn, caddr = sock.accept()
            except TimeoutError:
                continue
            
            tpe.submit(handle_client, cconn)

        sock.close()
        print('client listener: stopped')


if __name__ == '__main__':
    main()
