import socket
import sys
import time
import select

class IRC:
 
    irc = socket.socket()
  
    def __init__(self):
        # Deefine the socket
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def command(self,msg):
        self.irc.send(bytes(msg + "\n", "UTF-8"))
 
    def send(self, channel, msg):
        # Transfer data
        self.command("PRIVMSG " + channel + " :" + msg)
 
    def connect(self, server, port, channel, botnick, botpass, botnickpass):
        # Connect to the server
        print("Connecting to: " + server)
        self.irc.connect((server, port))

        # Perform user authentication
        self.command("USER " + botnick + " " + botnick +" " + botnick + " :python")
        self.command("NICK " + botnick)
        #self.irc.send(bytes("NICKSERV IDENTIFY " + botnickpass + " " + botpass + "\n", "UTF-8"))
        time.sleep(5)

        # join the channel
        self.command("JOIN " + channel)
 
    def get_response(self):
        time.sleep(1)
        # Get the response
        resp = self.irc.recv(2040).decode("UTF-8")
 
        if resp.find('PING') != -1:
           self.command('PONG ' + resp.split()[1]  + '\r') 
 
        return resp

    def get_users(self):
        self.command(f"NAMES {channel}")
        names = []
        end = time.time() + 2  # wait up to 2 seconds

        while time.time() < end:
            r, _, _ = select.select([self.irc], [], [], 0.5)
            if not r:
                continue

            text = self.irc.recv(4096).decode("utf-8", errors="ignore")

            for line in text.split("\r\n"):
                if " 353 " in line and " :" in line:
                    names += [n.lstrip("@+%~&") for n in line.split(" :", 1)[1].split()]

                if " 366 " in line:  # end of names list
                    return names

        return names


import os
import random

## IRC Config
server = "irc.libera.chat" 	# Provide a valid server IP/Hostname
port = 6667
channel = "#csc482"
botnick = "kaitlyn-bot"
botnickpass = ""		# in case you have a registered nickname 		
botpass = ""			# in case you have a registered bot	

irc = IRC()
irc.connect(server, port, channel, botnick, botpass, botnickpass)
memory = {}
names =[]
while True:
    text = irc.get_response()
    print("RECEIVED ==> ",text) 
    text = text.lower()
    if "privmsg" in text and channel in text and botnick.lower()+":" in text and "hello" in text:
        irc.send(channel, "hi back!")

    if "privmsg" in text and channel in text and botnick.lower()+":" in text and "die" in text:
        irc.send(channel, "I shall!")
        irc.command("QUIT")
        sys.exit()

    if "privmsg" in text and channel in text and botnick.lower()+":" in text and "forget" in text:
        memory.clear()
        irc.send(channel, "forgetting everything!")

    if "privmsg" in text and channel in text and botnick.lower()+":" in text and ("who are you?" in text or "usage" in text):
        irc.send(channel, f"My name is {botnick}. I was created by Kaitlyn Carrillo, CSC 482 -01")
        irc.send(channel, "I can answer questions about mice! Ask me: \"Can a mouse defeat a cat in battle?\"")
    
    if "privmsg" in text and channel in text and botnick.lower()+":" in text and "users" in text:
        users = irc.get_users()
        irc.send(channel, ", ".join(users))


#to run this, run "python3 lab5-phase1.py" and go to browser and type "https://web.libera.chat"
#connect to the libra chat with a nickname and the channel "#CSC482"
#then type "kaitlyn-bot: hello" into the chat to get it to respond

        
