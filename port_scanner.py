import socket

def get_open_ports(target, port_range):
    open_ports = []
    rServerIP = socket.gethostbyname(target)
    for port in range(port_range):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((rServerIP, port))
        print('Open ports for ')
        if result == 0:
            print(f"Port {port}:      Open")



    return(open_ports)