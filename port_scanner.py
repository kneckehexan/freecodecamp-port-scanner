import socket
import sys
import re
from common_ports import ports_and_services as ps

def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    for port in range(port_range[0], port_range[1]+1): # Adding 1, as its not inclusive right.
        try: 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0) # Setting a timer on the lookup.
            result = s.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            s.close()
        except KeyboardInterrupt:
            print('\nCtrl+C pressed. Aborting program.')
            sys.exit()
        except socket.gaierror as e:
            if e.errno == -2:
                if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target):
                    return "Error: Invalid IP address"
                else:
                    return 'Error: Invalid hostname'
        except socket.error as e:
            pass # Not sure about this one, but for the tests to continue running, keep it.
    
    if verbose:
        ip = socket.gethostbyname(target)
        if ip == target:
            try:
                url = socket.gethostbyaddr(target)[0]
            except socket.herror as e:
                if e.errno == 1:
                    url = ''
        else:
            url = target


        if url == '':
            r = "Open ports for {}\n".format(ip)
        else:
            r = "Open ports for {} ({})\n".format(url, ip)
        r += "PORT     SERVICE\n"
        for i, p in enumerate(open_ports):
            if p in ps:
                service = ps[p]
            else:
                service = 'unknown' # Incase service isn't in the provided list.
            offset = 9 - len(str(p))
            if i == len(open_ports)-1:
                r += f"{p}" + " " *offset + f"{service}"
            else:
                r += f"{p}" + " " *offset + f"{service}\n"
        return(r)

    return(open_ports)