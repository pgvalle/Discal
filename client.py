from common import *
import tkinter as tk


window = tk.Tk()

# text widgets
host_label = tk.Label(window, text='host')
port_label = tk.Label(window, text='port')
v1_label = tk.Label(window, text='v1')
op_label = tk.Label(window, text='op')
v2_label = tk.Label(window, text='v2')
result_label = tk.Label(window, text='???')

# variables to store input from input boxes
host_var = tk.StringVar()
port_var = tk.StringVar()
v1_var = tk.StringVar()
op_var = tk.StringVar()
v2_var = tk.StringVar()

# input boxes
host_entry = tk.Entry(window, textvariable=host_var)
port_entry = tk.Entry(window, textvariable=port_var)
v1_entry = tk.Entry(window, textvariable=v1_var)
op_entry = tk.Entry(window, textvariable=op_var)
v2_entry = tk.Entry(window, textvariable=v2_var)

req_button = tk.Button(window, text='send')


def main():
    # positioning text widgets
    host_label.grid(row=0, column=0)
    port_label.grid(row=1, column=0)
    v1_label.grid(row=0, column=2)
    op_label.grid(row=2, column=2)
    v2_label.grid(row=1, column=2)
    result_label.grid(row=3, column=3)

    # positioning input boxes
    host_entry.grid(row=0, column=1)
    port_entry.grid(row=1, column=1)
    v1_entry.grid(row=0, column=3)
    op_entry.grid(row=2, column=3)
    v2_entry.grid(row=1, column=3)

    # configuring request button
    req_button.grid(row=2, column=1)
    req_button.config(command=request)
    
    # default values for host and port
    host_var.set('localhost')
    port_var.set('1061')

    # window settings
    window.title('DiscalC')
    window.mainloop()


def request():
    sock = None
    try:
        host = host_var.get()
        port = int(port_var.get())
        sock = socket.create_connection((host, port), timeout=1)

        req = json.dumps({
            'v1': v1_var.get(),
            'op': op_var.get(),
            'v2': v2_var.get() })
        send(sock, req)

        rsp = recv(sock)
        rsp = json.loads(rsp)
        result_label.config(text=rsp['result'])
    except Exception as e:
        print(f'error: {e}')
        result_label.config(text='???')

    if sock:
        sock.close()


if __name__ == '__main__':
    main()
