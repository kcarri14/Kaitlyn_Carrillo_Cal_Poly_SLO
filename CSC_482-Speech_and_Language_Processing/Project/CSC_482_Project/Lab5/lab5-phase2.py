import socket
import sys
import time
import select

class IRC:
 
    irc = socket.socket()
  
    def __init__(self):
        # Define the socket
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
        #time.sleep(1)
        # Get the response
        try:
            resp = self.irc.recv(2040).decode("UTF-8")
        except socket.timeout:
            return ""
 
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

def reset_timer():
    global random_time, t1, t2, t3, no_response_counter
    random_time = random.randint(1, 15)  # re-roll delay each cycle (optional but usually desired)
    base = waiting_time + random_time
    now = time.time()
    t1 = now + base
    t2 = t1 + base
    t3 = t2 + base
    no_response_counter = 0



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
irc.irc.settimeout(1.0)
start_time = time.perf_counter()
waiting_time = 15
random_time = random.randint(1, 15)
t1 = time.time() + waiting_time + random_time
t2 = t1 + waiting_time + random_time
t3 = t2 + waiting_time + random_time
user = None

#print(waiting_time + random_time)
no_response_counter = 0
first_hello = 0
memory = {}
names =[]
inital_outreach = ["hi", "hello", "hey", "hola"]
secondary_outreach = ["I said HELLO", "I said HI", "Excuse me, hello?", "Are you there?", "HIIIIIIIII", "hellooooooo"]
outreach_reply = ["hi", "hello back at you!", "hello", "HOLA"]
inquiry = ["how are you?", "how's it going?", "what's up?", "what's happening"]
inquiry_reply_2 = ["i'm good", "i'm fine", "i'm ok"]
inquiry_2 = ["how about you?", "and yourself?"]
inquiry_reply_1 = ["I'm good", "I'm fine, thanks for asking", "I'm ok"]
frustrated = ["Ok, forget you", "Screw you!", "Whatever!"]

state = "START"
while True:
    #print(state)
    #this does the timer function for the hello if nobody responds
    now = time.time()
    
    #print(now)
    if no_response_counter == 0 and now >= t1:
        rand = random.randint(0, len(inital_outreach) -1)
        saying = inital_outreach[rand]
        irc.send(channel, saying)
        no_response_counter += 1
        first_hello = 1
        state = "INITAL OUTREACH"

    if no_response_counter == 1 and now >= t2:
        rand = random.randint(0, len(secondary_outreach) -1)
        saying = secondary_outreach[rand]
        irc.send(channel, saying)
        no_response_counter += 1
        state = "SECOND OUTREACH"

    if no_response_counter == 2 and now >= t3:
        state = "GIVE UP FRUSTRATED"
        irc.send(channel, random.choice(frustrated))
        irc.command("QUIT")
        sys.exit()
    
    text = irc.get_response()
    text = text.lower()
    #print(text)
    #print(f"RECEIVED: {text}")
    name = None
    if text.startswith(":") and "!" in text:
        name = text[1:].split("!", 1)[0]

    if user is None and name is not None and name != botnick:
        user = name
    #print(user)
    if name == user:
        if "privmsg" in text and channel in text and botnick.lower()+":" in text and "die" in text:
            irc.send(channel, f"{name}: I shall!")
            irc.command("QUIT")
            sys.exit()

        if "privmsg" in text and channel in text and botnick.lower()+":" in text and "forget" in text:
            memory.clear()
            irc.send(channel, f"{name}: forgetting everything!")

        if "privmsg" in text and channel in text and botnick.lower()+":" in text and ("who are you?" in text or "usage" in text):
            irc.send(channel, f"{name}: My name is {botnick}. I was created by Kaitlyn Carrillo, CSC 482 -01")
            irc.send(channel, "I can answer questions about mice! Ask me: \"Can a mouse defeat a cat in battle?\"")

        if "privmsg" in text and channel in text and botnick.lower()+":" in text and "users" in text:
            users = irc.get_users()
            irc.send(channel,f"{name}: {", ".join(users)}")
        #first messanger
        msg = text.split(" :", 1)[1].strip() if " :" in text else ""
        msg_l = msg.lower()



        #second messanger
        if ("privmsg" in text and channel.lower() in text and (botnick.lower() + ":") in msg_l) and no_response_counter == 0:
            after = msg_l.split(botnick.lower() + ":", 1)[1].strip() 
            first = after.split()[0] if after else ""
            #print(first)
            #print(after)
            if first in inital_outreach:
                irc.send(channel, f"{name}: {random.choice(outreach_reply)}")
                state = "OUTREACH REPLY"
                reset_timer()
            
            if after in inquiry and state == "OUTREACH REPLY":
                irc.send(channel, f"{name}: {random.choice(inquiry_reply_2)}")
                irc.send(channel, f"{name}: {random.choice(inquiry_2)}")
                state = "INQUIRY"
                reset_timer()
            
            if after in inquiry and state == "INQUIRY 2":
                irc.send(channel, f"{name}: {random.choice(inquiry_reply_1)}")
                irc.command("QUIT")
                sys.exit()

        if ("privmsg" in text and channel.lower() in text and (botnick.lower() + ":") in msg_l) and no_response_counter == 1 and first_hello == 1:
            after = msg_l.split(botnick.lower() + ":", 1)[1].strip() 
            first = after.split()[0] if after else ""
            #print(first)
            #print(after)
            if first in inital_outreach:
                irc.send(channel, f"{name}: {random.choice(inquiry)}")
                state = "INQUIRY 2"
                reset_timer()
            

#to run this, run "python3 lab5-phase1.py" and go to browser and type "https://web.libera.chat"
#connect to the libra chat with a nickname and the channel "#CSC482"
#then type "kaitlyn-bot: hello" into the chat to get it to respond

        
        
#for phase 3, I am thinking we have it where the chat can given longtiude
#and latitude of a city given and the weather currently there
#i think this will fulfill the phase easily