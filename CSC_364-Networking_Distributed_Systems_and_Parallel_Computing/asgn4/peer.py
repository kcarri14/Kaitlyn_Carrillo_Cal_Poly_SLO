import socket
import sys
import threading
import struct 
import json
import os
import time

#gets chunks of files from peer and loads them into the file correctly
def retrieve_file(peer, directories):
    output_file = None

    while True:
        connection = peer.recv(4096)
        if not connection:
            return None
        message =  json.loads(connection.decode())

        if message is None:
            break

        if message["type"] == "T":
            filename = message["filename"]
            chunk_number = message["chunk_number"]
            chunk_size = message["chunk_size"]
            checksum = message["checksum"]

            chunk = peer.recv(chunk_size)
            #does checksum
            payload_checksum = sum(chunk) % 65535
            if checksum != payload_checksum:
                print(f"bad checksum sequence: {chunk_number}")
                continue
            #creates a file in the directory of the peer
            if output_file is None:
                output_path = os.path.join(directories, filename)
                output_file = open(output_path, "wb")

            output_file.write(chunk)
            #sends an ack back to the peer to let them know that they got that chunk
            acknowledgement = {"type": "A", "filename": filename, "chunk_number": chunk_number}
            data = json.dumps(acknowledgement).encode()
            peer.sendall(data)
        #once file is fully sent this breaks and closes the file
        if message["type"] == "D":
            break

        if output_file:
            output_file.close()


def send_request(peer, filename, directories):
    #sends the request for what file the peer doesnt have
    other_host = peer["host"]
    other_port = peer["port"]
    message = {
        "type": "R",
        "filename" : filename
    }

    try:
        other_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        other_peer.connect((other_host, other_port))
        data = json.dumps(message).encode()
        other_peer.sendall(data)

        retrieve_file(other_peer, directories)

        other_peer.close()
    except Exception as e:
        print(f"Error in send request: {e}")

def handle_peers(connection, peer_id, peer_host, peer_port, directories, file_table, requested_files, offered_to):
    try:
        message = json.loads(connection.recv(1024).decode())
        connection.settimeout(2)
        if message is None:
            connection.close()
            return
        #checks the type to respond correctly
        if message["type"] == "O":
            oPid = message["peer_id"]
            oHost = message["host"]
            oPort = message["port"]
            files = message["files"]

            offer_peer = {
                    "peer_id": oPid,
                    "host": oHost,
                    "port": oPort
                }
            #offers the offered peer its files so that both get all of them
            if oPid not in offered_to:
                offered_to.append(oPid)
                send_offer(offer_peer, peer_id, peer_host, peer_port, directories)
            #creates a thread for each file the other peer doesnt have 
            for filename in files:
                file_table[filename] = offer_peer
                if filename not in os.listdir(directories) and filename not in requested_files: 
                    requested_files.append(filename)    

                    request_thread = threading.Thread(
                        target=send_request,
                        args=(file_table[filename], filename, directories),
                        daemon=True
                    )
                    request_thread.start()
        #transfers the files to the new peer
        elif message["type"] == "R":
            filename = message["filename"]
            path = os.path.join(directories, filename)

            number_chunks = 0
            max_retries = 3

            with open(path, "rb") as f:
                while True:
                    chunk = f.read(1024)
                    #print("read chunk")
                    if not chunk:
                        break
                    #check sum for validation 
                    checksum = sum(chunk) % 65535

                    transfer_message = { "type" : "T", "filename" : filename, "chunk_number" : number_chunks, "chunk_size" : len(chunk), "checksum" : checksum}

                    #handles retransmissions of data
                    retries = 0
                    acknowledged = False

                    while retries < max_retries and not acknowledged:
                        try:
                            tm_data = json.dumps(transfer_message).encode()
                            connection.sendall(tm_data)
                            time.sleep(0.5)

                            connection.sendall(chunk)
                            # Wait for ACK
                    
                            data = connection.recv(4096)
                            if not data:
                                print(f"No acknowledgements received for chunk {number_chunks}")
                                retries += 1
                                continue
                            ack = json.loads(data.decode())
                        
                            if ack and ack["type"] == "A" and ack["filename"] == filename and ack["chunk_number"] == number_chunks:
                                print("Received acknowledgment for chunk", number_chunks)
                                
                                acknowledged = True
                            else:
                                transfer_message = { "type" : "T", "filename" : filename, "chunk_number" : number_chunks, "chunk_size" : len(chunk), "checksum" : checksum}
                                tm_data = json.dumps(transfer_message).encode()
                                connection.sendall(tm_data)
                                time.sleep(0.5)
                                connection.sendall(chunk)
                        except socket.timeout:
                            retries += 1
                        except Exception as e:
                            retries += 1
                    if not acknowledged:
                        return
                    
                    number_chunks +=1
            #sends a done message to let the other peer know when the whole file has been sent   
            done_message = {
                "type" : "D",
                "filename" : filename
            }
            d_data = json.dumps(done_message).encode()
            connection.sendall(d_data)

        elif message["type"] == "A":
            print("Received acknowledgment")

    except Exception as e:
        print(f"Error in handle peers: {e}")

    connection.close()

def deal_w_peers(peer_id, peer_host, peer_port, host, directories, file_table, requested_files, offered_to):
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.bind((host, peer_port))
    peer_socket.listen(5)
    #creates a thread to handle the messages sent back to the peer
    while True:
        connection, addr = peer_socket.accept()
        t = threading.Thread(target=handle_peers,args=(connection, peer_id, peer_host, peer_port,directories, file_table, requested_files, offered_to), daemon = True)
        t.start()

def send_offer(peer, peer_id, host, peer_port, directory):
    other_host = peer["host"]
    other_port = peer["port"]

    files = os.listdir(directory)

    message = {
        "type": "O",
        "peer_id" : peer_id,
        "host" : host,
        "port" : peer_port,
        "files" : files
    }
    #sends offers of all of the files the peer has
    try:
        other_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        other_peer.connect((other_host, other_port))
        data = json.dumps(message).encode()
        other_peer.sendall(data)
        other_peer.close()
    except Exception as e:
        print(f"Error in send offer: {e}")


def main():
    # inputs from the command line
    if(len(sys.argv) != 6):
        print("Usage: python3 peery.py <peer_id> <peer_port> <server_host> <server_port <directory>")
        return
    peer_id = sys.argv[1]
    peer_port = int(sys.argv[2])
    server_host = sys.argv[3]
    port = int(sys.argv[4])
    directories = sys.argv[5]
    host = "localhost"
    server_address = (server_host, port)

    #needs to be encoded to be sent and packed in json later
    encoded_id = peer_id.encode()

    file_table = {}
    requested_files = []
    offered_to = []

    #threads to deal with new peers
    t = threading.Thread(target=deal_w_peers, args=(peer_id, host, peer_port, host, directories, file_table, requested_files, offered_to))
    t.start()

    #start socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_address)

    #send data to server
    message = struct.pack("!32sI", encoded_id, peer_port)
    client.sendall(message)

    #get table back from server and go through and send offers to get files
    table_data = client.recv(4096).decode()
    table = json.loads(table_data)
    for peer in table:
        if id == peer_id:
            continue
        
        send_offer(peer, peer_id, host, peer_port, directories)

    t.join()

    
if __name__ == "__main__":
    main()


