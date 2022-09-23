
#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip


def main():

    host = 'www.google.com'
    port = 80

    # open a socket for client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
    
        print("Starting proxy server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode
        proxy_start.listen(2)
        
        # continuously listen for connections
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            
            # open socket for google
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(host)
                proxy_end.connect((remote_ip, port))
                p = Process(target=handle_echo, args=(proxy_end,addr, conn))
                p.daemon = True
                p.start()
                print("Started process", p)
            conn.close()
            
def handle_echo(proxy_end, addr, conn):
    # send data
    full_data = conn.recv(BUFFER_SIZE)
    print("Sending received data", full_data, "to Google.")
    proxy_end.sendall(full_data)
    proxy_end.shutdown(socket.SHUT_WR)
    
    data = proxy_end.recv(BUFFER_SIZE)
    print("Sending received data", data, "to client.")
    conn.send(data)

if __name__ == "__main__":
    main()
