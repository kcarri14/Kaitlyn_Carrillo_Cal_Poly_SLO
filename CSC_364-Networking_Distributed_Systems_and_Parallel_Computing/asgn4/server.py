import socket
import struct
import random
import sys
import time
import json
import threading

def handle_peers(connection, addr, table, ports_in_use):
    message = connection.recv(1024)
    peer_id = struct.unpack("!32s", message[:32])[0].decode().strip("\x00")
    peer_port = struct.unpack("!I", message[32:36])[0]
    
    new_peer = {
        "peer_id": peer_id,
        "host": addr[0],
        "port": peer_port
    }
    #checks if another peer is using the same port
    if peer_port not in ports_in_use:
        table.append(new_peer) 
    ports_in_use.append(peer_port)
    #print(table) 
    #sends table to the peers
    pack_table = json.dumps(table).encode()
    connection.sendall(pack_table)

def main():
    #parse arguments
    if(len(sys.argv) != 2):
        print("Usage: python3 server.py <host> <peer>")
        return 
    
    host = sys.argv[1]
    port = int(sys.argv[2])

    #start server and bind
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    #keeps track of the peers and the ports in use
    table = []
    ports_in_use = []

    #thread to handle each peer
    while True:
        try:
            connection, addr = server.accept()
            t = threading.Thread(target=handle_peers, args=(connection, addr, table, ports_in_use), daemon=True)
            t.start()
        except Exception:
            return

if __name__ == "__main__":
    main()