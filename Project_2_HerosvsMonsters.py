import random

mons_list = ["Dragon", "Zombie", "Ghost", "Minotaur"]
def random_arrow():
  return random.randint(1, 10)    #gives the player a random number of arrows for the game

def random_sword():
  return random.randint(1,10)    #gives the player a random number of swords for the game

def random_magic():
  return random.randint(1,10)    #gives the player a random number of magic for the game

def random_hammer():
  return random.randint(1,10)    #gives the player a random number of hammer for the game

   
print("Welcome to Hero's and Monsters!")    #prints welcome message
print("-------------------------------")
print("You are the Hero and must choose the correct weapons to defeat the monsters.")
print("You will learn which weapon kills which monsters as you play the game")
print(" ")
print("Your Weapons are: ")     #gives the player a list of weapons that they will have
print("1. Arrow")
print("2. Sword")
print("3. Magic")
print("4. Hammer")
print(" ")
arrow_count = random_arrow()    #assigns the random interger of arrows to a variable
sword_count = random_sword()    #assigns the random interger of swords to a variable
magic_count = random_magic()    #assigns the random interger of magic to a variable
hammer_count = random_hammer()    #assigns the random interger of hammers to a variable

dragon_count = 0    #assigns the dragon count to 0 at the beginning of each game 
zombie_count = 0    #assigns the zombie count to 0 at the beginning of each game
ghost_count = 0    #assigns the ghost count to 0 at the beginning of each game
minotaur_count = 0    #assigns the minotaur count to 0 at the beginning of each game

while True:
    print(" ")
    print("You're weapons for this game are:")
    print("Arrow Count:",int(arrow_count))      #prints out the random number of arrows for the game
    print("Sword Count:",int(sword_count))      #prints out the random number of swords for the game
    print("Magic Count:",int(magic_count))      #prints out the random number of magic for the game
    print("Hammer Count:",int(hammer_count))      #prints out the random number of hammers for the game
    print(" ")
    monster = random.choice(mons_list)      #randomly picks a monster from the list of monsters
    print("The Monster you have to slay is:", monster)
    user = input("Input your Weapon: ")      #asks the user to input the weapon to slay the monster
    if monster == "Zombie":
      if user.lower() == "sword":     
        sword_count -= 1
        zombie_count += 1
        if sword_count == 0:
            print(" ")
            print("Oh no! You ran out of swords!")
            continue
        elif sword_count == -1:
           zombie_count -= 1
           print(" ")
           print("Since you ran out of swords, the zombie got you! You died!")
           print(" ")
           print("Here is your final kill count:")
           print("Dragon:", dragon_count)
           print("Zombie:", zombie_count)
           print("Ghost:", ghost_count)
           print("Minotaur", minotaur_count)
           break
        else:
            print(" ")
            print("You've slayed the Zombie!")
            continue
      else:
        print(" ")
        print("Oh no the zombie got you!")
        print(" ")
        print("Here is your final kill count:")
        print("Dragon:", dragon_count)
        print("Zombie:", zombie_count)
        print("Ghost:", ghost_count)
        print("Minotaur", minotaur_count)
        break
    elif monster == "Dragon":
      if user.lower() == "arrow":
        arrow_count -= 1
        dragon_count += 1
        if arrow_count == 0:
            print("Oh no! You ran out of arrows!")
            continue
        elif arrow_count == -1:
           dragon_count -= 1
           print(" ")
           print("Since you ran out of arrows, the dragon got you! You died!")
           print(" ")
           print("Here is your final kill count:")
           print("Dragon:", dragon_count)
           print("Zombie:", zombie_count)
           print("Ghost:", ghost_count)
           print("Minotaur", minotaur_count)
           break
        else:
            print(" ")
            print("You've slayed the Dragon!")
            continue
      else:
        print(" ")
        print("Oh no the dragon got you!")
        print(" ")
        print("Here is your final kill count:")
        print("Dragon:", dragon_count)
        print("Zombie:", zombie_count)
        print("Ghost:", ghost_count)
        print("Minotaur", minotaur_count)
        break
    elif monster == "Ghost":
      if user.lower() == "magic":
        magic_count -= 1
        ghost_count += 1
        if magic_count == 0:
            print(" ")
            print("Oh no! You ran out of magic!")
            continue
        elif magic_count == -1:
           magic_count -= 1
           print(" ")
           print("Since you ran out of magic, the ghost got you! You died!")
           print("Here is your final kill count:")
           print("Dragon:", dragon_count)
           print("Zombie:", zombie_count)
           print("Ghost:", ghost_count)
           print("Minotaur", minotaur_count)
           break
        else:
            print(" ")
            print("You've slayed the ghost!")
            continue
      else:
        print(" ")
        print("Oh no the ghost got you!")
        print(" ")
        print("Here is your final kill count:")
        print("Dragon:", dragon_count)
        print("Zombie:", zombie_count)
        print("Ghost:", ghost_count)
        print("Minotaur", minotaur_count)
        break
    elif monster == "Minotaur":
      if user.lower() == "hammer":
        hammer_count -= 1
        if hammer_count == 0:
            print(" ")
            print("Oh no! You ran out of hammers!")
            continue
        elif hammer_count == -1:
           minotaur_count += 1
           print(" ")
           print("Since you ran out of hammers, the Minotaur got you! You died!")
           print(" ")
           print("Here is your final kill count:")
           print("Dragon:", dragon_count)
           print("Zombie:", zombie_count)
           print("Ghost:", ghost_count)
           print("Minotaur", minotaur_count)
           break
        else:
            print(" ")
            print("You've slayed the Minotaur!")
            continue
      else:
        print(" ")
        print("Oh no the minotaur got you!")
        print(" ")
        print("Here is your final kill count:")
        print("Dragon:", dragon_count)
        print("Zombie:", zombie_count)
        print("Ghost:", ghost_count)
        print("Minotaur", minotaur_count)
        break
    else:
      print(" ")
      print("That's not a weapon! You've been killed")
    
 
    
    
   
