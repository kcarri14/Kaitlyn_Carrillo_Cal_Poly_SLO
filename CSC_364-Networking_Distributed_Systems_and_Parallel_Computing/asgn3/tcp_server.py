import socket
import struct
import random
import sys
import time

def main():
    #parse arguments
    host = sys.argv[1]
    port = int(sys.argv[2])
    lost_probability = float(sys.argv[3])

    #start server and bind
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))
    server.settimeout(0.1)
    print(f"Server listening on localhost:{port}")

    #stores next sequence it is expecting from client
    expected_seq = 0
    #buffer for packets
    received_buffer = {}
    timeout_seq = 548864   
    timeout_done = False    

    with open("receive.txt", "wb") as output_file:
        #keep receiving packets
        while True:
            batch = []
            start_time = time.time()

            while time.time() - start_time < 0.1:
                try:
                    message, addr = server.recvfrom(2048)
                    batch.append(message)
                except socket.timeout:
                    break

            if not batch:
                continue

            for message in batch:
                #simulates random packet loss by picking a number between 0 and 1
                if random.random() < lost_probability:
                    print("Packet loss")
                    continue
                #unpack the message
                sequence_number = struct.unpack("!I", message[:4])[0]
                checksum = struct.unpack("!H", message[4:6])[0]
                payload = message[6:]
                #check the checksum to make sure no corruption
                payload_checksum = sum(payload) % 65535
                if checksum != payload_checksum:
                    print(f"bad checksum sequence: {sequence_number}")
                    continue
                print(f"received seq: {sequence_number //1024}")
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
            if expected_seq >= timeout_seq and not timeout_done:
                print(f"manual timeout: skipping ACK for expected_seq={expected_seq}")
                timeout_done = True
            else:
                ack_packet = struct.pack("!I", expected_seq)
                server.sendto(ack_packet, addr)
                #print(f"received seq: {sequence_number // 1024}, sent ack = {expected_seq // 1024}")

if __name__ == "__main__":
    main()

