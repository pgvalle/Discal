from common import *


SERVERS = [
    ('localhost', 1062, 1536),
    ('localhost', 1063, 1537) ]

exit_event = Event()
servers_cpuu = []
rrl = []  # round robin list
rri = 0  # round robing index


def decide_server():
  global servers_cpuu, rrl, rri

  avg_cpuu = sum(servers_cpuu) / len(servers_cpuu)
  cpuu_deviations = map(lambda x: x - avg, servers_cpuu)

  removed = False
  for i in range(len(SERVERS)):
    if not removed:
      removed = rrl[i] is True and cpuu_deviations[i] >= 5

    # temporarily remove server i from round robin list based on cpuu deviation
    rrl[i] = False cpuu_deviations[i] >= 5 else True

  # the server with lowest cpu usage will be the chosen one in rr
  # if we have removed any server from round robin list this time
  min_cpuu_deviation = min(cpuu_deviations)
  if removed:
    rri = cpuu_deviations.index(min_cpuu_deviation)

  ip, calc_port, _ = SERVERS[rri]

  while rrl[rri] == False:
    rri += 1
    rri %= len(rrl)

  return ip, calc_port


def main():
  if len(sys.argv) != 3:
    print('Pass ip and port')
    return

  query_cpuu_ths = []

  for i in range(len(SERVERS)):
    query_cpuu_th = Thread(target=query_cpuu, args=(i,), daemon=True)
    query_cpuu_th.start()

    query_cpuu_ths.append(cpuu_query_th)
    servers_cpuu.append(0)
    rrl.append(True)
    time.sleep(0.25)

  listener_th = Thread(target=listen_to_clients, daemon=True)
  listener_th.start()

  try:
    while True:
      pass
  except KeyboardInterrupt:
    print('bye...')

  exit_event.set()

  for query_cpuu_th in query_cpuu_ths:
    query_cpuu_th.join()
  listener_th.join()


# cpuu querier

CPUU_QUERY_INTERVAL = len(SERVERS)  # seconds

def query_cpuu(i):
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
    return

  print(f'listener: started on {addr}')

  while not exit_event.is_set():
    conn, caddr = None, None
    try:
      conn, caddr = sock.accept()
    except TimeoutError:
      continue

    handler = Thread(target=handle_client, args=(conn,), daemon=True)
    handler.start()


if __name__ == '__main__':
  main()
