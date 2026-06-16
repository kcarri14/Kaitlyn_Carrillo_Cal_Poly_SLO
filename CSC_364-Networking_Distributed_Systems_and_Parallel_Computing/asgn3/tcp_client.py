import socket
import threading
import struct
import time 
import matplotlib.pyplot as mp
import sys
#keeps track of dup acks
dup_ack_count = {}

#creates graphs from the cwnd and retransmission history
def make_graphs(cwnd_history, retransmission_history):
    if cwnd_history:
        x_values = []
        y_values = []
        for x, y in cwnd_history:
            x_values.append(x)
            y_values.append(y)

        mp.figure()
        mp.plot(x_values, y_values)
        mp.xlabel("RTT")
        mp.ylabel("cwnd size")
        mp.title("cwnd vs. RTT")
        mp.savefig("cwnd_vs_rtt.png")
        mp.close()
    if retransmission_history:
        x_values = []
        y_values = []
        for x, y in retransmission_history:
            x_values.append(x)
            y_values.append(y)

        mp.figure()
        mp.plot(x_values, y_values)
        mp.xlabel("RTT")
        mp.ylabel("Retransmissions")
        mp.title("Retransmissions vs. RTT")
        mp.savefig("retrans_vs_rtt.png")
        mp.close()
        

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    server_address = (host, port)

    #start socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.settimeout(0.5)
    # start at seqence 0
    sequence_number = 0
    #list of data to be sent
    packets = {}
    #starting cwnd and ssthresh
    cwnd = 1
    ssthresh = 16
    in_frt = False
    # divide the file into chunks and get all data for all packets packed and ready to send
    with open(sys.argv[3], "rb") as f:
       while True: 
            chunk = f.read(1024)
            #print("read chunk")
            if not chunk:
                break
            checksum = sum(chunk) % 65535
            binary_data = struct.pack("!IH", sequence_number, checksum) + chunk
            packets[sequence_number] = binary_data
            #print("packet")
            sequence_number += len(chunk)
            #print(sequence_number)
    #oldest unacknowledged byte
    oldest = 0
    #next sequence number to send
    next_seq = 0
    #need for graphing later
    cwnd_history = []
    retransmission_history = []
    #counts successful acks in round
    rtt = 0
    #tracks retranmission
    retransmissions = 0
    ack_list = []

    frt_ack = 0

    cwnd_history.append((rtt, cwnd))
    file1 = open("cwnd_history.txt", "w")

    #print("before the big while")
    #once the oldest unacknowledged byte is the sequence number
    while oldest < sequence_number:
        #send packets while there are still packets and amount of unack data is less than cwnd *1024
        # print(f"next_seq: {next_seq}")
        # print(f"")
        while next_seq < sequence_number and (next_seq - oldest) < cwnd * 1024:            
            if next_seq in packets:
                soc.sendto(packets[next_seq], server_address)
                with open("cwnd_history.txt", "a") as f:
                        print(f"packet sent: {next_seq}, during cwnd:{cwnd}\n", file=f)
            #move to next packet
            next_seq += 1024
            
        #print("before try")
        #wait to receive an ack from receiver
        #if no ack within 500 ms, then socke timeout triggers the except
        try:
            message, _ = soc.recvfrom(1024)
            if len(message) < 4:
                continue
            #print("before message unpack")
            ack_number = struct.unpack("!I", message[:4])[0]
            # if ack_number != next_seq:
            #      continue
            ack_list.append(ack_number)
            #print("if ack_number is greater than base")
            #if ack is greater than the oldest then data was successful
            number_packets_received = max(1, (ack_number - oldest) // 1024)
            with open("cwnd_history.txt", "a") as f:
                    print(f"number_acks_received = {number_packets_received}",file=f)
            if ack_number > oldest:
                oldest = ack_number

                if next_seq < oldest:
                    next_seq = oldest

                dup_ack_count.clear()
                in_frt = False
                #slow_start
                if cwnd < ssthresh:
                    cwnd *= 2
                else: #congestion avoidance
                    cwnd += 1
                
                rtt += 1
                cwnd_history.append((rtt, cwnd))
                retransmission_history.append((rtt, retransmissions))
                
                with open("cwnd_history.txt", "a") as f:
                        print(f"ack_received: {ack_number}, {(rtt, cwnd)}\n", file=f)
                 
                    
            #if not then duplicate ack is acknowledged
            else:
                if ack_number != oldest:
                    continue

                if in_frt and ack_number == frt_ack:
                    continue
                #triple duplicate ack
                #print("else")
                #store the number of duplicate ack in dictionary for lookup later
                dup_ack_count[ack_number] = dup_ack_count.get(ack_number, 0) + 1
                if ack_number == oldest and dup_ack_count[ack_number] != 3:
                    
                    # print(f"dup_ack: {rtt, ack_number, dup_ack_count[ack_number]}")
                    with open("cwnd_history.txt", "a") as f:
                            print(f"dup: {dup_ack_count[ack_number], ack_number}\n", file=f)
                    
                    if ack_number in packets:
                        next_seq = oldest
                        retransmissions +=1
                        continue

                #fast retransmit if triple dup ack
                if dup_ack_count[ack_number] == 3 and not in_frt:
                    with open("cwnd_history.txt", "a") as f:
                        print(f"trip_dup: {dup_ack_count[ack_number], ack_number}\n", file=f)
                    frt_ack = ack_number
                    ssthresh = max(cwnd // 2, 1)
                    cwnd = ssthresh
                    
                    if ack_number in packets:
                        soc.sendto(packets[ack_number], server_address)
                        retransmissions += 1
                    dup_ack_count[ack_number] = 0
                    
                    # print(f"ssthresh dup: {ssthresh}")
                    # print(f"cwnd dup: {cwnd}")
                    # print(f"rtt dup: {rtt}")
                    in_frt = True

        except socket.timeout:
            #print("except")
          
           #timeout
           # makes sure the oldest has been sent and if the time between the sent and current is greater than 500
            ssthresh = max(cwnd // 2, 1)
            cwnd = 1

            in_frt = False
            dup_ack_count.clear()
            #resend packets
            # if oldest in packets:
            #     soc.sendto(packets[oldest], server_address)
            next_seq = oldest
            retransmissions += 1
            cwnd_history.append((rtt, cwnd))
            retransmission_history.append((rtt, retransmissions))

            with open("cwnd_history.txt", "a") as f:
                    print(
        f"TIMEOUT oldest={oldest}, next_seq={next_seq}, "
        f"cwnd={cwnd}, ssthresh={ssthresh}, "
        f"in_flight={(next_seq - oldest) // 1024}",
        file=f
    )
            #next_seq = oldest
                # print(f"ssthresh timeout: {ssthresh}")
                # print(f"cwnd timeout: {cwnd}")
                # print(f"rtt timeout: {rtt}")
               


    make_graphs(cwnd_history, retransmission_history)
    # with open("cwnd_history.txt", "w") as f:
    #     for rtt, cwnd in cwnd_history:
    #         f.write(f"{rtt},{cwnd}\n")
    
    # with open("ack_list.txt", "w") as f:
    #     for ack in ack_list:
    #         f.write(f"{ack}\n")

    # with open("retransmission_history.txt", "w") as f:
    #     for rtt, cwnd in retransmission_history:
    #         f.write(f"{rtt},{cwnd}\n")
    soc.close()

if __name__ == "__main__":
    main()