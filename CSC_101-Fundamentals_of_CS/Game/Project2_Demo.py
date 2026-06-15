import random

#FUNCTIONS

def random_arrow():
  return random.randint(1, 10)    #gives the player a random number of arrows for the game

def random_sword():
  return random.randint(1,10)    #gives the player a random number of swords for the game

def random_magic():
  return random.randint(1,10)    #gives the player a random number of magic for the game

def random_hammer():
  return random.randint(1,10)    #gives the player a random number of hammers for the game

def random_stake():
  return random.randint(1,10)    #gives the player a random number of stakes for the game

#LISTS AND DICTIONARIES

mons_list = ["Dragon", "Zombie", "Ghost", "Minotaur", "Vampire"]       #list of monsters
monsters = {"Dragon":"arrow", "Zombie":"sword", "Ghost":"magic", "Minotaur":"hammer", "Vampire": "stake"}   #dictionary of monsters and their weaknesses
hero = {"arrow":random_arrow(),"sword":random_sword(),"magic":random_magic(),"hammer":random_hammer(), "stake": random_stake()}   #dictionary of weapons and their random amounts
mons_count = {"arrow": 0, "sword": 0, "magic": 0, "hammer": 0, "stake": 0}      #keeps count of how many monsters are defeated by each type
weapons_list = {"arrow":1, "sword":2,"magic":3, "hammer":4, "stake":5}        #dictionary of weapons

money_count = {"arrow" : 10, "sword": 5, "magic": 2, "hammer": 7, "stake": 4}   #dictionary of how much each weapon costs
money = 0                                                                       #money count starts at 0 with every game
money_total = money_count["arrow"] + money_count["sword"] + money_count["magic"] + money_count["hammer"] + money_count["stake"] #counts up all the money

#prints welcome message and rules

print("Welcome to Hero's and Monsters!")    
print("-------------------------------")
print("You are the Hero and must choose the correct weapons to defeat the monsters.")            
print("You will learn which weapon kills which monsters as you play the game")
print("At the beginning of the game, you will have $0 but as you defeat monsters you will earn money")
print("The money can be used to purchase weapons in the store,") 
print("but beware the weapons are twice as much to purchase than you get for killing the monster.")
print(" ")

#GAME

while True:
    print(" ")
    print("-----------------------------")
    print("You're weapons for this game are:")
    print("Arrow Count:",hero['arrow'])      #prints out the random number of arrows for the game
    print("Sword Count:",hero['sword'])      #prints out the random number of swords for the game
    print("Magic Count:",hero['magic'])      #prints out the random number of magic for the game
    print("Hammer Count:",hero['hammer'])      #prints out the random number of hammers for the game
    print("Stake Count:",hero['stake'])       #prints out the random number of stakes for the game
    print(" ")

    monster = random.choice(mons_list)      #randomly picks a monster from the list of monsters
    
    print("The Monster you have to slay is:", monster)
    print(" ")
    print("Here are your weapons: ")            #gives the player a list of weapons that they will have
    print(" ")
    print("1. Arrow")
    print("2. Sword")
    print("3. Magic")
    print("4. Hammer")
    print("5. Stake")
    print(" ")
    print("You have $", money, "in your account")      #gives the amount of money in their bank account
    print(" ")

    weapon = input("Input your Weapon or if you want to purchase a weapon input 'store': ")     #user inputs if they want to select a weapon to defeat the monsters or go to the store
    
    if weapon.lower() == monsters[monster]:                 #if they go select a weapon this will check to make sure the right weapon was selected
            hero[weapon] -= 1                                   #subtracts the number of the selected weapons from resources
            mons_count[weapon] += 1                             #adds 1 to the monster count for the selected weapon
            money += money_count[weapon]                        # adds the proper amount of money for the monster defeated
            if hero[weapon] == 0:                               # if the weapon selected equals 0, it reminds the user of that
                print("Oh no! You ran out of", weapon)          
            elif hero[weapon] == -1:                           # if the weapon would be -1 because they ran out of weapons, the hero is then defeated since they can purchase weapons at the store if they need
                mons_count[weapon] -= 1                         #makes sure to not count the last monster on the defeated list
                print("Oh no! Since you ran out of", weapon,"you died! You should've purchased some at the store!")
                break
            else:
                print(" ")
                print("You've defeated the", monster, "Good job!" )   #tells the user that they defeated the monster
                print(" ")
                print("You have $", money, "in your account")         #tells user how much is in their bank account
    elif weapon.lower() == "store":                      #if the user selects store this will bring it to the store
        print(" ")
        print("Welcome to the Store! Here you can purchase any weapons you need!")
        print("but everytime you visit the store you may only purchase one weapon")      # gives the weapons and prices that are for sale
        print("1. Arrow - $20")
        print("2. Sword - $10")
        print("3. Magic - $4")
        print("4. Hammer - $14")
        print("5. Stake - $8")
        print(" ")
        print("You have $", money, "in your account")                            #Tells you how much is in your bank account that you can spend
        print(" ")
        choice = input("Please input the weapon that you would like to purchase: ")  #user gets to pick which weapon they want to purchase
        if choice.lower() == "arrow" or "hammer" or "stake" or "magic" or "stake":
          hero[choice] += 1                                        #adds to the weapon list number for the weapon that was chosen
          if money > money_count[choice]*2:                      #makes sure that the user has enough money to purchase weapon
            money -= money_count[choice]*2
            print("You have purchased a", choice, ". Back to the game!")    #tells them what they purchased
            continue
          else:
             hero[choice] -= 1                               #subtracts the weapon that was previously added
             print("You don't have enough money! You don't get the weapon!")      #tells them if they don't have enough money to purchase the weapon they choose
             continue
        else:
          print("That isn't a weapon! You back to the game!")           #if they don't input a weapon, they go back into the game
          continue
    else:
        print(" ")
        print("Oh no! The", monster, "is immune to",weapon,". You've been defeated!")                  #if they don't choose the right weapon, they are defeated
        break   

print(" ")
print("Here is your defeated list: ")                #gives them a list of monsters that they defeated
print("Dragon:", mons_count["arrow"])
print("Zombie:", mons_count["sword"])
print("Ghost:", mons_count["magic"])
print("Minotaur:", mons_count["hammer"])
print("Vampire:", mons_count["stake"])
print("")

#Do not have any functions to test as the functions are just used to generate random ints

         
