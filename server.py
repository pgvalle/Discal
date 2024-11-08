from common import *
import psutil


exit_event = Event()  # to cleanly exit threads (properly free ports)


def main():
  if len(sys.argv) != 4:
    print('Pass ip, calc_port and cpuu_port')
    return

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
  v1, op, v2 = None, None, None
  try:
    req = json.loads(req)  # JSONDecodeError
    # KeyError
    v1 = req['v1']
    op = req['op']
    v2 = req['v2']

    if not op in VALID_OPERATIONS:
      return { 'status': 3, 'result': 'invalid operation' }

    v1 = float(v1)  # ValueError or TypeError
    v2 = float(v2)

    expr = f'{v1} {op} {v2}'
    v2 = eval(expr)  # Arithmetic Error
    print(f'calc: {expr}')
  except json.JSONDecodeError as e:
    return { 'status': 2, 'result': str(e) }
  except KeyError as e:
    return { 'status': 4, 'result': str(e) }
  except ArithmeticError as e:
    return { 'status': 1, 'result': str(e) }
  except Exception as e:
    return { 'status': 5, 'result': str(e) }

  return { 'status': 0, 'result': v2 }

def calc_conn_handler(conn):
  try:
    req = recv(conn)
    rsp = calc_rsp(req)
    rsp = json.dumps(rsp)
    send(conn, rsp)
    print(f'calc: {rsp}')
  except OSError as e:
    print(f'calc: error: {e}')

  conn.close()

def calc():
  sock, addr = None, None
  try:
    addr = (sys.argv[1], int(sys.argv[2]))
    sock = socket.create_server(addr)
    sock.settimeout(1)
    sock.listen()
  except Exception as e:
    print(f'calc: error: {e}')
    print('calc: could not start service')
    return

  print(f'calc: started on {addr}')

  while not exit_event.is_set():
    # accept connections with timeout so that this thread may terminate
    conn, caddr = None, None
    try:
      conn, caddr = sock.accept()
    except TimeoutError:
      continue

    handler = Thread(target=calc_conn_handler, args=(conn,), daemon=True)
    handler.start()

  print('calc: stopped')
  sock.close()


# cpu usage service

def cpuu():
  sock, addr = None, None
  try:
    addr = (sys.argv[1], int(sys.argv[3]))
    sock = socket.create_server(addr)
    sock.settimeout(1)
    sock.listen()
  except Exception as e:
    print(f'cpuu: error: {e}')
    print('cpuu: could not start service')
    return

  print(f'cpuu: started on {addr}')

  while not exit_event.is_set():
    # accept connections with timeout so that this thread may terminate
    conn, caddr = None, None
    try:
      conn, caddr = sock.accept()
    except TimeoutError:
      continue

    try:
      usage = psutil.cpu_percent()
      send(conn, usage)
      print(f'cpuu: {usage}%')
    except OSError as e:
      print(f'cpuu: error: {e}')

    conn.close()

  print('cpuu: stopped')
  sock.close()


if __name__ == '__main__':
  main()
