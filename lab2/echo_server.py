#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""  # host is localhost which is why we are leaving it blank
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()  # conn is a socket instance which allows us to communicate with client and addr is address information of the client that is connecting to us
            print("Connected by", addr)
            
            p = Process(target=handle_echo, args=(s,addr, conn))
            p.daemon = True
            p.start()
            conn.close()
            
def handle_echo(s, addr, conn):
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    print("full data", full_data)
    conn.sendall(full_data)

if __name__ == "__main__":
    main()
