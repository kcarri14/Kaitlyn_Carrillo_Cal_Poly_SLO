# Server can accept connections.
#     Server handles Login and Logout from users, and keeps records of which users are logged in.
#     Server handles Join and Leave from users, keeps records of which channels a user belongs to, and keeps records of which users are in a channel.
#     Server handles the Say message.
#     Server correctly handles List and Who.

import socket
import threading
import queue
import struct
import time
import sys


messages = queue.Queue()
clients= {}
client_address ={}
channel_list = {}

def keep_alive():
    while True:
        time.sleep(5)
        now = time.time()
        #checks for each client if they have been inactive for more than 2 minutes
        for client, info in list(clients.items()):
            if now - info["last_seen"] > 120:
                addr = clients[client]["addr"]
                for channel in list(clients[client]["channels"]):
                    if channel in channel_list:
                        channel_list[channel].discard(client)
                    if channel in channel_list and not channel_list[channel]:
                        channel_list.pop(channel)
                clients.pop(client)
                client_address.pop(addr, None)
                print("popped a client")

def main():
    #parse arguments
    host = sys.argv[1]
    port = int(sys.argv[2])

    #start server and bind
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))

    #start thread
    t = threading.Thread(target=keep_alive)
    t.start()

    print("Server listening on localhost:5555")
    try:
        while True:
            message, addr = server.recvfrom(1024)
            if len(message) < 4:
                continue
            message_type = struct.unpack("!I", message[:4])[0]
            #print(message_type)
            #login response
            if message_type == 0:
                if len(message) < 36:
                    continue
                username = struct.unpack("!32s", message[4:36])[0].split(b'\x00', 1)[0].decode()
                if username in clients:
                    err = "Username already in use"[:64].encode()
                    binary_data = struct.pack("!I64s", 3, err)
                    server.sendto(binary_data, addr)
                    continue
                clients[username] = {"addr": addr, "channels": set(), "last_seen": time.time()}
                client_address[addr] = username
                # print("IM IN LOGIN")
            #logout response
            elif message_type == 1:
                username = client_address.get(addr)
                addr = clients[username]["addr"]
                for ch in list(clients[username]["channels"]):
                    if ch in channel_list:
                        channel_list[ch].discard(username)
                        if not channel_list[ch]:
                            channel_list.pop(ch)
                clients.pop(username)
                client_address.pop(addr, None)
                # print("IM EXITING")
            #join response
            elif message_type == 2:
                if len(message) < 36:
                    continue
                channel_name = struct.unpack("!32s", message[4:36])[0].split(b'\x00', 1)[0].decode()
                username = client_address.get(addr)
                if username is None:
                    continue
                clients[username]["last_seen"] = time.time()
                channel_list.setdefault(channel_name, set()).add(username)
                clients[username]["channels"].add(channel_name)
                #print("IM IN JOIN")
            #leave response
            elif message_type == 3:
                if len(message) < 36:
                    continue
                channel_name = struct.unpack("!32s", message[4:36])[0].split(b'\x00', 1)[0].decode()
                username = client_address.get(addr)
                if username is None:
                    continue
                clients[username]["last_seen"] = time.time()
                if channel_name not in clients[username]["channels"]:
                    err = f"Not on channel {channel_name}"[:64].encode()
                    binary_data = struct.pack("!I64s", 3, err)
                    server.sendto(binary_data, addr)
                    continue
                clients[username]["channels"].discard(channel_name)
                if channel_name in channel_list:
                    channel_list[channel_name].discard(username)
                    #if no users in channel list then discard channel
                    if not channel_list[channel_name]:
                        channel_list.pop(channel_name)
                # print("IM IN LEAVE")
            #say response
            elif message_type == 4:
                if len(message) < 100:
                    continue
                channel_name = struct.unpack("!32s", message[4:36])[0].split(b'\x00', 1)[0].decode()
                text = struct.unpack("!64s", message[36:100])[0].split(b'\x00', 1)[0].decode()
                username = client_address.get(addr)
                if username is None:
                    continue
                clients[username]["last_seen"] = time.time()
                if channel_name not in clients[username]["channels"]:
                    err = f"Not on channel {channel_name}"[:64].encode()
                    binary_data = struct.pack("!I64s", 3, err)
                    server.sendto(binary_data, addr)
                    continue
                client_channel_list = list(channel_list.get(channel_name, set()))
                for cc in client_channel_list:
                    if cc in clients:
                        binary_data = struct.pack("!I32s32s64s", 0, channel_name.encode(), username.encode(), text.encode())
                        server.sendto(binary_data, clients[cc]["addr"])
                # print("IM IN SAY")
            #list response
            elif message_type == 5:
                username = client_address.get(addr)
                if username is None:
                    continue
                clients[username]["last_seen"] = time.time()
                number_channels = len(channel_list.keys())
                packed = struct.pack("!II", 1, number_channels)
                for ch in channel_list.keys():
                    packed += struct.pack("!32s", ch.encode())
                server.sendto(packed, addr)
                # print("IM IN LIST")
            #who response
            elif message_type == 6:
                
                username = client_address.get(addr)
                if username is None:
                    continue
                clients[username]["last_seen"] = time.time()
                channel_name = struct.unpack("!32s", message[4:36])[0].split(b'\x00', 1)[0].decode()
                #print(channel_name)
                if channel_name not in channel_list:
                    err = f"Channel {channel_name} does not exist"[:64].encode()
                    binary_data = struct.pack("!I64s", 3, err)
                    server.sendto(binary_data, addr)
                    continue
                number_username= len(channel_list[channel_name])
                packed = struct.pack("!II32s", 2, number_username, channel_name.encode())
                for ch in channel_list[channel_name]:
                    packed += struct.pack("!32s", ch.encode())
                #print("sent data back")
                server.sendto(packed, addr)
                # print("IM IN WHO")
            #keep alive message was sent by client
            elif message_type == 7:
                username = client_address.get(addr)
                if username is None:
                    continue
                clients[username]["last_seen"] = time.time()
            
    except Exception as e:
        print("Server Error: ", e)

if __name__ == "__main__":
    main()