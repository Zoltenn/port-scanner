import socket, threading, time

def scanner(ip, ports, tcp=True, udp=False) -> tuple:
    '''
    Scans port(s) of the target IP.

    Parameters
        ----------\n
        ip : str
            Target IP for which to port scan
        ports : int or an iterable type of int 
            A port number, or list of, to scan on target IP
        tcp : bool
            Set True for TCP port scanning; Default = True
        udp : bool
            UDP scanning feature is not yet supported.

    Returns
        -------
        tuple(dict, float)
            A dictionary of <port:status>, a float of time elapsed during scan
    '''
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

            for t in threads:
                t.start()
            
            for t in threads:
                t.join()

        elif type(ports) is int:
            # single port passed
            tcp_scan(ip, ports)

        else:
            print('Please ensure ports numbers are integers or an iterable series of them.')
    
    # TODO: udp section
    elif udp and not tcp:
        return print('UDP feature not yet supported')

    elif tcp and udp:
        return print('UDP feature not yet supported')

    else:
        return print('Please choose')
    
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
    # TODO:  udp scanner utility
    pass


ip = input('Input target IP: ')
ports = range(65536)
port_dict, time = scanner(ip, ports)

count = 0
for k,v in port_dict.items():
    if v == 'open':
        count += 1
        print('Port ' + str(k), ' is ' + v)
print('\n', count, 'TCP ports are open.')
print('Scanner finished in ' + str(time) + ' seconds')

