import sys
import socket
import threading
import random
import struct
import time

last_sent_time = time.time()

def receive(client):
    while True:
        try:
            message, _ = client.recvfrom(1024)
            if len(message) < 4:
                continue
            message_type = struct.unpack("!I", message[:4])[0]
            print("receiving messages")
            #say response
            if message_type == 0:
                if len(message) < 132:
                    continue
                #separate texts and print out
                channel = struct.unpack("!32s", message[4:36])[0].split(b'\x00', 1)[0].decode()
                username = struct.unpack("!32s", message[36:68])[0].split(b'\x00', 1)[0].decode()
                text = struct.unpack("!64s", message[68:132])[0].split(b'\x00', 1)[0].decode()
                print(f"[{channel}][{username}]: {text}")
            #list response
            if message_type == 1:
                #find the total number of channels
                total = struct.unpack("!I", message[4:8])[0]
                offset = 8
                print("Exisiting Channels: ")
                #go through the rest of the message to unpack the channels with the offset
                for _ in range(total):
                    if offset + 32 > len(message):
                        continue
                    text = struct.unpack("!32s", message[offset:offset+32])[0].split(b'\x00', 1)[0].decode()
                    print(f"    {text}")
                    offset+=32
               
            #who repsonse
            if message_type == 2:
                #find the total number of usernames
                #print("We are in who response")
                total = struct.unpack("!I", message[4:8])[0]
                #find the channel name
                channel_name = struct.unpack("!32s", message[8:40])[0].split(b'\x00', 1)[0].decode()
                offset = 40
                #print(f"Users on {channel_name}: ")
                #go through the rest of the message to unpack the channels with the offset
                for _ in range(total):
                    if offset + 32 > len(message):
                        continue
                    text = struct.unpack("!32s", message[offset:offset+32])[0].split(b'\x00', 1)[0].decode()
                    print(f"    {text}")
                    offset+=32
                    
            #error response
            if message_type == 3:
                if len(message) < 68:
                    continue
                error_message = struct.unpack("!64s", message[4:68])[0].split(b'\x00', 1)[0].decode()
                print(f"Error: {error_message}")
        except:
            pass

def keep_alive(client, server_address):
    #global variable to track last sent message
    global last_sent_time
    while True:
        time.sleep(1)
        idle_time = time.time() - last_sent_time
        #checks if its been 1 minute between a response
        if idle_time >= 60:
            #if so send a message to keep the client alive
            binary_data = struct.pack("!I", 7)
            client.sendto(binary_data, server_address)
            last_sent_time = time.time()

def main():
# Client connects, logs in, and joins “Common”.
    global last_sent_time
    if(len(sys.argv) != 4):
        print("Usage: ./client -host -port -username")
        exit()
    
    #parse arguments
    host = sys.argv[1]
    port = int(sys.argv[2])
    username = sys.argv[3][:32].encode()
    server_address = (host, port)
    active_channel = "Common"
    channel_set = {"Common"}

    #start socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #creat and start threads
    t = threading.Thread(target=receive, args=(soc,), daemon=True)
    t2 = threading.Thread(target=keep_alive, args=(soc,server_address), daemon=True)
    t2.start()
    t.start()

    #login
    binary_data = struct.pack("!I32s", 0, username)
    soc.sendto(binary_data, server_address)
    last_sent_time = time.time()
    # #join common   
    binary_data = struct.pack("!I32s", 2, active_channel.encode())
    soc.sendto(binary_data, server_address)
    last_sent_time = time.time()
    
    while True:
        message = input("> ")
        #exit
        if message == ("/exit"):
            binary_data = struct.pack("!I", 1)
            soc.sendto(binary_data, server_address)
            last_sent_time = time.time()
            break
        #list
        elif message == "/list":
            binary_data = struct.pack("!I", 5)
            soc.sendto(binary_data, server_address)
            last_sent_time = time.time()
        #join
        elif message.startswith("/join"):
            if (message == "/join"):
                print("Usage: /join channel")
                continue
            channel = message[message.index(" ")+1:]
            if len(channel) > 32:
                print("Warning! Channel name must be less than 32 characters")
            binary_data = struct.pack("!I32s", 2, channel[:32].encode())
            channel_set.add(channel)
            active_channel = channel
            soc.sendto(binary_data, server_address)
            last_sent_time = time.time()
        #leave
        elif message.startswith("/leave"):
            if (message == "/leave"):
                print("Usage: /leave channel")
                continue
            channel = message[message.index(" ")+1:]
            binary_data = struct.pack("!I32s", 3, channel.encode())
            if channel in channel_set:
                channel_set.discard(channel)
                if not channel_set[channel]:
                    channel_set.pop(channel)
            if active_channel == channel:
                active_channel = None
            soc.sendto(binary_data, server_address)
            last_sent_time = time.time()
        #who
        elif message.startswith("/who"):
            if (message == "/who"):
                print("Usage: /who channel")
                continue
            channel = message[message.index(" ")+1:]
            if len(channel) > 32:
                print("Warning! Channel name must be less than 32 characters")
            #print("sending data")
            binary_data = struct.pack("!I32s", 6, channel[:32].encode())
            #print("sending data")
            soc.sendto(binary_data, server_address)
            #print("sending data")
            last_sent_time = time.time()
        #switch
        elif message.startswith("/switch"):
            if (message == "/switch"):
                print("Usage: /switch channel")
                continue
            channel = message[message.index(" ")+1:]
            if channel in channel_set:
                active_channel = channel
                print(active_channel)
            else:
                print("Must join channel before switching to it")
                continue
        #messages to send
        else:
            if active_channel == None:
                print("Must join be on a channel to talk")
                continue
            else:
                binary_data = struct.pack("!I32s64s", 4, active_channel.encode(), message[:64].encode())
                soc.sendto(binary_data, server_address)
                last_sent_time = time.time()
        #this is so that things can be printed out and then the prompt comes back
        time.sleep(0.5)

    soc.close()

if __name__ == "__main__":
    main()

# Client reads lines from the user and parses commands.
# Client correctly sends Say message.
# Client uses select() to wait for input from the user and the server.
# Client correctly sends Join, Leave, Login, and Logout and handles Switch.
# Client correctly sends List and Who.