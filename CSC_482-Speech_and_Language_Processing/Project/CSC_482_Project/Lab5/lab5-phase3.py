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
        #time.sleep(1)
        # Get the response
        try:
            resp = self.irc.recv(2040).decode("UTF-8")
        except socket.timeout:
            return ""
 
        if resp.find('PING') != -1:
           self.command('PONG ' + resp.split()[1]  + '\r') 
 
        return resp

    def get_users(self, channel):
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

import random
import spacy
import openmeteo_requests
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

def get_city(query):
    doc = nlp(query)
    for ent in doc.ents:
        if ent.label_ in ("GPE", "LOC"):
            return ent.text
    return None

def get_location(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
    }

    # get longitude and latitude
    res = requests.get(url, params=params).json()
    if not res.get("results"):
        return None

    ret = {}
    loc_info = res.get("results")[0]

    ret.update({"timezone" : loc_info.get("timezone")})
    ret.update({"population" : loc_info.get("population")})
    ret.update({"country" : loc_info.get("country")})
    ret.update({"latitude" : loc_info.get("latitude")})
    ret.update({"longitude" : loc_info.get("longitude")})
    print(ret)
    return ret

def get_weather(city):
    openmeteo = openmeteo_requests.Client()
    weather_url = "https://api.open-meteo.com/v1/forecast"
    location = get_location(city)

    if not location:
        return f"Could not get the weather for {city}."
    lat = location.get("latitude")
    long = location.get("longitude")

    weather_params = {
        "latitude": lat,
        "longitude": long,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation_probability", 
        ],
    }

    res = openmeteo.weather_api(weather_url, params=weather_params)[0]
    current = res.Current()

    # get first hourly point
    temp_c = current.Variables(0).Value()
    humidity = current.Variables(1).Value()
    feels_like = current.Variables(2).Value()
    precipitation = current.Variables(3).Value()

    feels_like = (feels_like * 9/5) + 32
    temp_f = (temp_c * 9/5) + 32

    return (f"The temperature in {city.title()} is {temp_f:.1f} °F and {temp_c:.1f} °C right now but it feels like {feels_like:.1f}°F. "
            f"There is a humidity of {humidity:.1f}% and a {precipitation:.1f}% chance of rain.")

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

# wait to join before starting timer
join_confirmed = False
while not join_confirmed:
    text = irc.get_response()
    if not text:
        continue
    if "366" in text:
        join_confirmed = True

start_time = time.perf_counter()
waiting_time = 15
random_time = random.randint(1, 15)
t1 = time.time() + waiting_time + random_time
t2 = t1 + waiting_time + random_time
t3 = t2 + waiting_time + random_time
user = None

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
other_user = None

loc_words = {"timezone", "time zone", "time", "date", "where", "population", "country"}
weather_words = {"weather", "tempearture", "humidity", "rain", "snow", "snowing", "raining", "storm", "hot", "cold"}
nlp = spacy.load("en_core_web_lg")

state = "START"
print("starting")
while True:
    #this does the timer function for the hello if nobody responds
    now = time.time()

    if no_response_counter == 0 and now >= t1:
        rand = random.randint(0, len(inital_outreach) -1)
        saying = inital_outreach[rand]
        users = irc.get_users(channel)
        users.remove("kaitlyn-bot") # prevent bot from addressing itself
        other_user = random.choice(users)
        irc.send(channel, f"{other_user}: {saying}")
        no_response_counter += 1
        first_hello = 1
        state = "INITAL OUTREACH"

    if no_response_counter == 1 and now >= t2:
        rand = random.randint(0, len(secondary_outreach) -1)
        saying = secondary_outreach[rand]
        irc.send(channel, f"{other_user}: {saying}")
        no_response_counter += 1
        state = "SECOND OUTREACH"

    if no_response_counter == 2 and now >= t3:
        state = "GIVE UP FRUSTRATED"
        irc.send(channel, random.choice(frustrated))
        irc.command("QUIT")
        sys.exit()
    
    text = irc.get_response()
    text = text.lower()
    
    name = None
    if text.startswith(":") and "!" in text:
        name = text[1:].split("!", 1)[0]

    if "privmsg" in text and channel in text and botnick.lower()+":" in text:
        if user is None and name is not None and name != botnick:
            user = name
            if other_user is not None and name != other_user:
                other_user = name
            if state == "START":
                state = "OUTREACH REPLY"

    if name == user:
        if "privmsg" in text and channel in text and botnick.lower()+":" in text and "die" in text:
            irc.send(channel, f"{name}: I shall!")
            irc.command("QUIT")
            sys.exit()

        if "privmsg" in text and channel in text and botnick.lower()+":" in text and "forget" in text:
            memory.clear()
            # completely restart 
            no_response_counter = 0
            first_hello = 0
            other_user = None
            names.clear()
            state = "START"
            random_time = random.randint(1, 15)
            random_time = random.randint(1, 15)
            t1 = time.time() + waiting_time + random_time
            t2 = t1 + waiting_time + random_time
            t3 = t2 + waiting_time + random_time
            irc.send(channel, "forgetting everything!")
            user = None

        if "privmsg" in text and channel in text and botnick.lower()+":" in text and ("who are you?" in text or "usage" in text):
            irc.send(channel, f"My name is {botnick}. I was created by Kaitlyn Carrillo, Ellie Pearson, Harini Baskar, and Siri Gunturi, CSC 482-03")
            irc.send(channel, "I can answer questions about the weather and places! Ask me: \"What time is it in Los Angeles?\" or \"What's the weather in London?\"")
        
        if "privmsg" in text and channel in text and botnick.lower()+":" in text and "users" in text:
            users = irc.get_users(channel)
            irc.send(channel, ", ".join(users))

        if "privmsg" in text and channel in text and botnick.lower()+":" in text and any(w in text for w in loc_words):
            asker = text.split("!")[0][1:]
            city = get_city(text)
            if not city:
                irc.send(channel, f"{asker}: Sorry, I don't recognize this location")
            else:
                resp = get_location(city)
                if not resp:
                    irc.send(channel, f"{asker}: Sorry, I don't recognize this location")
                else:
                    timezone = resp.get("timezone")
                    if timezone is None:
                        formatted_time = "an unknown time"
                    else:
                        current_time = datetime.now(tz=ZoneInfo(timezone))
                        formatted_time = current_time.strftime("%B %d, %Y at %I:%M %p %Z")
                    msg = f"{city.title()}, {resp.get("country")} has a population of {resp.get("population")} and it is currently {formatted_time}."
                    irc.send(channel, f"{asker}: {msg}")

        if "privmsg" in text and channel in text and botnick.lower()+":" in text and any(w in text for w in weather_words):
            asker = text.split("!")[0][1:]
            city = get_city(text)
            if not city:
                irc.send(channel, "Could not find the weather for this location.")
            else:
                irc.send(channel, f"{asker}: {get_weather(city)}")
            state = ""
        
        #first messager
        msg = text.split(" :", 1)[1].strip() if " :" in text else ""
        msg_l = msg.lower()


        #second messanger
        if ("privmsg" in text and channel.lower() in text and (botnick.lower() + ":") in msg_l) and no_response_counter == 0:
            after = msg_l.split(botnick.lower() + ":", 1)[1].strip() 
            first = after.split()[0] if after else ""

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
            if first in inital_outreach:
                irc.send(channel, f"{name}: {random.choice(inquiry)}")
                state = "INQUIRY 2"
                reset_timer()
        

#to run this, run "python3 lab5-phase3.py" and go to browser and type "https://web.libera.chat"
#connect to the libra chat with a nickname and the channel "#CSC482"
#then type "kaitlyn-bot: hello" into the chat to get it to respond