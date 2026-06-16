import socket
import struct
import random
import sys
def main():
    #parse arguments
    host = sys.argv[1]
    port = int(sys.argv[2])
    lost_probability = float(sys.argv[3])

    #start server and bind
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))

    print("Server listening on localhost:5550")

    #stores next sequence it is expecting from client
    expected_seq = 0
    #buffer for packets
    received_buffer = {}

    batch = []
    with open("receive.txt", "wb") as output_file:
        #keep receiving packets
        while True:
            message, addr = server.recvfrom(2048)
            if len(message) < 6:
                continue
            
            #unpack the message
            sequence_number = struct.unpack("!I", message[:4])[0]
            last = struct.unpack("!B", message[4:5])[0]
            checksum = struct.unpack("!H", message[5:7])[0]
            payload = message[7:]
            #check the checksum to make sure no corruption
            payload_checksum = sum(payload) % 65535
            if checksum != payload_checksum:
                print(f"bad checksum sequence: {sequence_number}")
                continue

            batch.append((sequence_number,payload))

            if last == 0:
                continue
            else:
                for sequence_number, payload in batch:
                    #simulates random packet loss by picking a number between 0 and 1
                    if random.random() < lost_probability:
                        print("Packet loss")
                        continue

                    #add payload into buffer
                    received_buffer[sequence_number] = payload
                    #put the payloads into output file in correct order
                    #if missing a packet it will wait til that packet arrives
                    while expected_seq in received_buffer:
                        chunk = received_buffer.pop(expected_seq)
                        output_file.write(chunk)
                        output_file.flush()
                        expected_seq += len(chunk)
                    #send ack to client
                    
                    ack_packet = struct.pack("!I", expected_seq)
                    server.sendto(ack_packet, addr)

            # print(f"received seq: {sequence_number}, sent ack = {expected_seq}")

if __name__ == "__main__":
    main()
