import socket
import struct
import time 
import matplotlib.pyplot as mp

#tracks the last ack received
last_ack_received = 0 
#stores acks that have ben received
ack_packets = set()
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
        mp.savefig("cwnd_vs_rtt_1.png")
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
        mp.savefig("retrans_vs_rtt_1.png")
        mp.close()
        

def main():
    host = "localhost"
    port = 5550
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

    # divide the file into chunks and get all data for all packets packed and ready to send
    with open("./file.txt", "rb") as f:
       while True: 
            chunk = f.read(1024)
            #print("read chunk")
            if not chunk:
                break
            
            packets[sequence_number] = chunk
            #print("packet")
            sequence_number += len(chunk)
            #print(sequence_number)
    #oldest unacknowledged byte
    oldest = 0
    #next sequence number to send
    next_seq = 0
    #stores times packets are sent
    send_times = {}
    #need for graphing later
    cwnd_history = []
    retransmission_history = []
    #counts successful acks in round
    rtt = 0
    #tracks retranmission
    retransmissions_this_round = 0
    round_end = oldest + (int(cwnd) * 1024)

    #print("before the big while")
    #once the oldest unacknowledged byte is the sequence number
    while oldest < sequence_number:
        packets_sent_this_round = 0
        round_limit = int(cwnd)
        #send packets while there are still packets and amount of unack data is less than cwnd *1024
        while next_seq < sequence_number and packets_sent_this_round < round_limit and (next_seq - oldest) < cwnd * 1024:
                chunk = packets[next_seq]
                if packets_sent_this_round == round_limit - 1 or next_seq + len(chunk) >= sequence_number:
                     last = 1
                else:
                     last = 0

                if next_seq in packets:
                    
                    checksum = sum(chunk) % 65535
                    binary_data = struct.pack("!IBH", next_seq, last, checksum) + chunk
                    soc.sendto(binary_data, server_address)
                    send_times[next_seq] = time.time()
                    with open("cwnd_history.txt", "a") as f:
                        print(f"packet sent: {next_seq}, during cwnd:{cwnd}\n", file=f)
                    next_seq += 1024
                    packets_sent_this_round +=1
                
                #move to next packet
                
                
        #print("before try")
        #wait to receive an ack from receiver
        #if no ack within 500 ms, then socke timeout triggers the except
        try:
            message, _ = soc.recvfrom(1024)
            if len(message) < 4:
                continue
            #print("before message unpack")
            ack_number = struct.unpack("!I", message[:4])[0]
            #print("if ack_number is greater than base")
            #if ack is greater than the oldest then data was successful
            number_packets_received = (ack_number - oldest) // 1024
            if number_packets_received < 1:
                 print("ERROR")
    
            if ack_number > oldest:
                oldest = ack_number
                dup_ack_count.clear()
                #slow_start
                if cwnd < ssthresh:
                    cwnd += number_packets_received
                else: #congestion avoidance
                    cwnd += 1

                rtt += 1
                cwnd_history.append((rtt, cwnd))
                retransmission_history.append((rtt, retransmissions_this_round))
                retransmissions_this_round = 0


                with open("cwnd_history.txt", "a") as f:
                        print(f"ack_received: {ack_number}, {(rtt, cwnd)}\n", file=f)
            #if not then duplicate ack is acknowledged
            else:
                #triple duplicate ack
                #print("else")
                #store the number of duplicate ack in dictionary for lookup later
                dup_ack_count[ack_number] = dup_ack_count.get(ack_number, 0) + 1
#keep track of the ack_number and oldest and and add as many ack_number 
                with open("cwnd_history.txt", "a") as f:
                        print(f"dup: {dup_ack_count[ack_number], ack_number}\n", file=f)
                #fast retransmit if triple dup ack
                if dup_ack_count[ack_number] == 3:
                    with open("cwnd_history.txt", "a") as f:
                        print(f"trip_dup: {dup_ack_count[ack_number], ack_number}\n", file=f)
                    ssthresh = max(cwnd // 2, 1)
                    cwnd = cwnd//2
                    
                    if ack_number in packets:
                        chunk = packets[ack_number]
                        checksum = sum(chunk) % 65535

                        binary_data = struct.pack("!IBH", ack_number, 1, checksum) + packets[ack_number]
                        soc.sendto(binary_data, server_address)

                        send_times[ack_number] = time.time()
                        retransmissions_this_round += 1

        except socket.timeout:
            with open("cwnd_history.txt", "a") as f:
                    print(
        f"TIMEOUT oldest={oldest}, next_seq={next_seq}, "
        f"cwnd={cwnd}, ssthresh={ssthresh}, "
        f"in_flight={(next_seq - oldest) // 1024}",
        file=f
    )
            ssthresh = max(cwnd / 2, 1)
            cwnd = 1
            #resend packets
            next_seq = oldest
            retransmissions_this_round +=1

    make_graphs(cwnd_history, retransmission_history)
    # with open("cwnd_history.txt", "w") as f:
    #     for rtt, cwnd in cwnd_history:
    #         f.write(f"{rtt},{cwnd}\n")

    # with open("retransmission_history.txt", "w") as f:
    #     for rtt, cwnd in retransmission_history:
    #         f.write(f"{rtt},{cwnd}\n")
    soc.close()

if __name__ == "__main__":
    main()