from common import *
import tkinter as tk


window = tk.Tk()

host_label = tk.Label(window, text='host')
host_var = tk.StringVar()
host_entry = tk.Entry(window, textvariable=host_var)

port_label = tk.Label(window, text='port')
port_var = tk.StringVar()
port_entry = tk.Entry(window, textvariable=port_var)

v1_label = tk.Label(window, text='v1')
v1_var = tk.StringVar()
v1_entry = tk.Entry(window, textvariable=v1_var)

v2_label = tk.Label(window, text='v2')
v2_var = tk.StringVar()
v2_entry = tk.Entry(window, textvariable=v2_var)

op_label = tk.Label(window, text='op')
op_var = tk.StringVar()
op_entry = tk.Entry(window, textvariable=op_var)

result_label = tk.Label(window, text='???')


def request():
    sock = None
    try:
        host = host_var.get()
        port = int(port_var.get())
        sock = socket.create_connection((host, port), timeout=1)
    except Exception as e:
        result_label.config(text='???')
        print(f'error: {e}')
        return

    try:
        req = {
            'v1': v1_var.get(),
            'op': op_var.get(),
            'v2': v2_var.get() }
        req = json.dumps(req)
        send(sock, req)

        rsp = recv(sock)
        rsp = json.loads(rsp)
        result_label.config(text=rsp['result'])
    except OSError as e:
        print(f'error {e}')
        result_label.config(text='???')

    if sock:
        sock.close()
    

send_button = tk.Button(window, text='send', command=request)


def main():
    host_label.grid(row=0,column=0)
    host_entry.grid(row=0,column=1)
    host_var.set('localhost')

    port_label.grid(row=1,column=0)
    port_entry.grid(row=1,column=1)
    port_var.set('1061')

    v1_label.grid(row=0,column=2)
    v1_entry.grid(row=0,column=3)

    v2_label.grid(row=1,column=2)
    v2_entry.grid(row=1,column=3)

    op_label.grid(row=2,column=2)
    op_entry.grid(row=2,column=3)

    result_label.grid(row=3,column=3)

    send_button.grid(row=2,column=1)

    window.title('client')
    window.mainloop()


if __name__ == '__main__':
    main()
