from common import *
import concurrent.futures as cf


SERVERS = [
    ('localhost', 1062, 1536),
    ('localhost', 1063, 1537) ]

CPUU_QUERY_INTERVAL = len(SERVERS)  # seconds

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

    time.sleep(1)

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
  ip, _, port = SERVERS[i]

  while not exit_event.is_set():
    start = time.time()
    conn = None
    try:
      conn = socket.create_connection((ip, port), timeout=1)
      usage = recv(conn)
      usage = float(usage)
      print(f'cpuu querier {i}: {usage}%')

      servers_cpuu[i] = usage
    except OSError as e:
      servers_cpuu[i] = 1e10  # force server to be removed from rr
      print(f'cpuu querier {i}: error: {e}')

    if conn:
      conn.close()

    delta = time.time() - start
    if delta < CPUU_QUERY_INTERVAL:
      time.sleep(CPUU_QUERY_INTERVAL - delta)


def handle_client(conn):
  sock = None
  try:
    addr = decide_server()
    sock = socket.create_connection(addr)
  except OSError as e:
    print(f'handler: error: {e}')
    conn.close()
    return

  try:
    msg = recv(conn)
    send(sock, msg)
    msg = recv(sock)
    send(conn, msg)
  except OSError as e:
    print(f'handler: error: {e}')

  sock.close()
  conn.close()


def listen_to_clients():
  sock, addr = None, None
  try:
    addr = (sys.argv[1], int(sys.argv[2]))
    sock = socket.create_server(addr)
    sock.settimeout(1)
    sock.listen()
  except Exception as e:
    print(f'listener: error: {e}')
    print('listener: could not start')
    exit_event.set()
    return

  print(f'listener: started on {addr}')

  with cf.ThreadPoolExecutor(max_workers=10) as tpe:
    while not exit_event.is_set():
      conn, caddr = None, None
      try:
        conn, caddr = sock.accept()
      except TimeoutError:
        continue
      
      tpe.submit(handle_client, conn)

    print('listener: stopped')
    sock.close()


if __name__ == '__main__':
  main()
