from common import *
import psutil


if len(sys.argv) != 4:
  sys.exit('Pass ip, calc_port and cpuu_port')


exit_event = Event()  # to cleanly exit threads (properly free ports)
ip, calc_port, cpuu_port = sys.argv[1:]


def main():
  calc_th = Thread(target=calc, daemon=True)
  calc_th.start()

  cpuu_th = Thread(target=cpuu, daemon=True)
  cpuu_th.start()

  try:
    while True:
      pass
  except KeyboardInterrupt:
    print('bye...')

  exit_event.set()
  calc_th.join()
  cpuu_th.join()


# calculator service

def calc_rsp(req):
  rsp = { 'status': 0 }
  try:
    req = json.loads(req)
    expr = f'{req["a"]} {req["op"]} {req["b"]}'

    rsp['result'] = eval(expr)
  except Exception as e:
    rsp['status'] = 1
    rsp['result'] = str(e)

  return json.dumps(rsp)


def calc_conn_handler(conn, addr):
  try:
    req = recv(conn)
    print(f'calc: {addr} sent {req}')

    rsp = calc_rsp(req)
    send(conn, rsp)
    print(f'calc: {rsp} sent to {addr}')
  except OSError as e:
    print(f'calc: error: {e}')
  finally:
    conn.close()


def calc():
  sock = None
  try:
    global calc_port
    calc_port = int(calc_port)
    sock = socket.create_server((ip, calc_port))
    sock.settimeout(1)
    sock.listen()
  except Exception as e:
    print(f'calc: error: {e}')
    print(f'calc: could not start service')
    return

  print(f'calc: started on port {calc_port}')

  while not exit_event.is_set():
    # accept connections with timeout so that this thread may terminate
    conn, addr = None, None
    try:
      conn, addr = sock.accept()
      print(f'calc: {addr} connected')
    except TimeoutError:
      continue

    handler = Thread(target=calc_conn_handler, args=(conn, addr), daemon=True)
    handler.start()

  print('calc: stopped')
  sock.close()


# cpu usage service

def cpuu():
  sock = None
  try:
    global cpuu_port
    cpuu_port = int(cpuu_port)
    sock = socket.create_server((ip, cpuu_port))
    sock.settimeout(1)
    sock.listen()
  except Exception as e:
    print(f'cpuu: error: {e}')
    print(f'cpuu: could not start service')
    return

  print(f'cpuu: started on port {cpuu_port}')

  while not exit_event.is_set():
    # accept connections with timeout so that this thread may terminate
    conn, addr = None, None
    try:
      conn, addr = sock.accept()
      print(f'cpuu: {addr} connected')
    except TimeoutError:
      continue

    try:
      usage = psutil.cpu_percent(interval=None)
      send(conn, usage)
      print(f'cpuu: sent to {addr}')
    except OSError as e:
      print(f'cpuu: error: {e}')
    finally:
      conn.close()

  print('cpuu: stopped')
  sock.close()


if __name__ == '__main__':
  main()
