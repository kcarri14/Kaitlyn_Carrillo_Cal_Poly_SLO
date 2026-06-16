README

RUNNING THE BOT
Run Phase 1 only (commands + basic hello):

   python3 lab5-phase1.py

Run Phase 3 (commands + greeting FSM + weather/location queries):

   python3 lab5-phase3.py

The bot will print "Connecting to: irc.libera.chat" and then begin
running. It will automatically join #csc482 and start its greeting
timer.


TESTING IN THE BROWSER
1. Go to: https://web.libera.chat/
2. Enter any nickname (e.g. "tester")
3. Join channel: #csc482
4. Address the bot with:   kaitlyn-bot: hello


SUPPORTED COMMANDS
All commands must be prefixed with the bot's name and a colon:

   kaitlyn-bot: die              — bot quits IRC and exits
   kaitlyn-bot: forget           — resets all memory and state
   kaitlyn-bot: who are you?     — bot identifies itself
   kaitlyn-bot: usage            — same as above
   kaitlyn-bot: users            — lists all users in the channel
   kaitlyn-bot: hello            — starts greeting conversation
   kaitlyn-bot: hi               — same as above


PHASE III QUERIES (weather/location)
Ask the bot about any city in the world:

   kaitlyn-bot: what's the weather in Tokyo?
   kaitlyn-bot: what time is it in London?
   kaitlyn-bot: what is the population of Paris?


CONFIGURATION
To change the bot nickname, channel, or server, edit the config
block near the top of the script:

   server   = "irc.libera.chat"
   port     = 6667
   channel  = "#csc482"
   botnick  = "kaitlyn-bot"



