'''guardar registros de tempos em tempos (na faixa de segundos)
do uso da cpu em cada servidor. Depois fazer algum cálculo em cima
desses valores pra decidir qual servidor vai ser usado'''

'''Threads ou Forks para tratar as conexões com os clientes???'''
from common import *


if len(sys.argv) != 3:
  sys.exit('Pass ip and port')


SERVERS = [
    ('localhost', 1062, 1536),
    ('localhost', 1063, 1537) ]

exit_event = Event()
ip, port = sys.argv[1:]
hists = []


def main():
  cpuu_query_ths = []

  for i in range(len(SERVERS)):
    th = Thread(target=query_cpuu, args=[i], daemon=True)
    th.start()
    cpuu_query_ths.append(th)
    hists.append([])

  listener = Thread(target=listen_to_clients, daemon=True)
  listener.start()

  try:
    while True:
      pass
  except KeyboardInterrupt:
    print('bye...')

  exit_event.set()

  for i in range(len(SERVERS)):
    cpuu_query_ths[i].join()
  listener.join()



a = False
def decide_server():
  global a
  a = not a
  if a:
    return IP1, CALC_PORT1
  return IP2, CALC_PORT2


def query_cpuu(i):
  ipi, _, porti = SERVERS[i]

  while not exit_event.is_set():
    start = time.time()
    conn = None
    try:
      conn = socket.create_connection((ipi, porti))
      usage = recv(conn)
      usage = float(usage)
      print(f'cpuu {i} query: {usage}%')

      elapsed = time.time()
      hists[i].append((usage, elapsed))
    except OSError as e:
      print(f'cpuu {i} query: error: {e}')

    if conn:
      conn.close()

    delta = time.time() - start
    if delta < 1:
      time.sleep(1 - delta)


def handle_client(conn, addr):
  conn.close()
  # sock = None
  # try:
  #   ip, port = decide_server()
  #   sock = socket.create_connection((ip, port))
  # except OSError as e:
  #   conn.close()
  #   print(e)
  #   return
  #
  # try:
  #   msg = recv(conn)
  #   send(sock, msg)
  #   msg = recv(sock)
  #   send(conn, msg)
  # except OSError as e:
  #   print(e)
  #
  # sock.close()
  # conn.close()


def listen_to_clients():
  sock = None
  try:
    global port
    port = int(port)
    sock = socket.create_server((ip, port))
    sock.settimeout(1)
    sock.listen()
  except Exception as e:
    print(f'listener: error: {e}')
    print('listener: could not start')
    return

  while not exit_event.is_set():
    conn, addr = None, None
    try:
      conn, addr = sock.accept()
    except TimeoutError:
      continue

    handler = Thread(target=handle_client, args=(conn, addr), daemon=True)
    handler.start()


if __name__ == '__main__':
  main()
