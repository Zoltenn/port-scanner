import socket, threading, time

def scanner(ip, ports, tcp=True, udp=False):
    # start timer
    start = time.time()
    open_ports = {}

    # tcp section
    if tcp and not udp:
        if hasattr(ports, '__iter__'):
            # multiple port numbers passed
            threads = []
            for i in range(len(ports)):
                t = threading.Thread(target=tcp_scan, args=(ip, ports[i], open_ports))
                threads.append(t)

            for i in range(len(threads)):
                threads[i].start()
            
            for t in threads:
                t.join()

        elif type(ports) is int:
            # single port passed
            tcp_scan(ip, ports)

        else:
            print('Please ensure ports numbers are integers or an iterable series of them.')
    
    # TODO: udp section
    elif udp and not tcp:
        print('Feature not yet supported')
        return ValueError
    
    # stop timer
    end = time.time()
    return open_ports, end-start

def tcp_scan(ip: str, port: int, open_ports):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set socket option to reuse identical sockets
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(0.5)
        s.connect((ip, port))
        open_ports[port] = 'open'
    except:
        open_ports[port] = 'closed'


def udp_scan(ip: str, port: int):
    # TODO: udp scanner utility
    pass


ip = input('Input target IP: ')
ports = range(65536)
port_dict, time = scanner(ip, ports)

print('\n' + 'Scanner finished in ' + str(time) + ' seconds')
for k,v in port_dict.items():
    if v == 'open':
        print('Port ' + str(k), ' is ' + v)
