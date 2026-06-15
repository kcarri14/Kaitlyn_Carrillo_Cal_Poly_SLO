import random

mons_list = ["Dragon", "Zombie", "Ghost", "Minotaur"]
def random_arrow():
  return random.randint(1, 10)

def random_sword():
  return random.randint(1,10)

def random_magic():
  return random.randint(1,10)

def random_hammer():
  return random.randint(1,10)

 

print("Welcome to Hero's and Monsters!")
print("-------------------------------")
print("You are the Hero and must choose the correct weapons to defeat the monsters.")
print(" ")
print("Your Weapons are: ")
print("1. Arrow")
print("2. Sword")
print("3. Magic")
print("4. Hammer")
print(" ")
arrow_count = random_arrow()
sword_count = random_sword()
magic_count = random_magic()
hammer_count = random_hammer()

dragon_count = 0
zombie_count = 0
ghost_count = 0
minotaur_count = 0

while True:
    print(" ")
    print("You're weapons for this game are:")
    print("Arrow Count:",int(arrow_count))
    print("Sword Count:",int(sword_count))
    print("Magic Count:",int(magic_count))
    print("Hammer Count:",int(hammer_count))
    print(" ")
    monster = random.choice(mons_list)
    print("The Monster you have to slay is:", monster)
    user = input("Input your Weapon: ")
    if monster == "Zombie":
      if user.lower() == "sword":
        sword_count -= 1
        zombie_count += 1
        if sword_count == 0:
            print("Oh no! You ran out of swords!")
            continue
        elif sword_count == -1:
           zombie_count -= 1
           print("Since you ran out of swords, the zombie got you! You died!")
           print("Here is your final kill count:")
           print("Dragon:", dragon_count)
           print("Zombie:", zombie_count)
           print("Ghost:", ghost_count)
           print("Minotaur", minotaur_count)
           break
        else:
            print("You've slayed the Zombie!")
            continue
      else:
        print("Oh no the zombie got you!")
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
           print("Since you ran out of arrows, the dragon got you! You died!")
           print("Here is your final kill count:")
           print("Dragon:", dragon_count)
           print("Zombie:", zombie_count)
           print("Ghost:", ghost_count)
           print("Minotaur", minotaur_count)
           break
        else:
            print("You've slayed the Dragon!")
            continue
      else:
        print("Oh no the dragon got you!")
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
            print("Oh no! You ran out of magic!")
            continue
        elif magic_count == -1:
           magic_count -= 1
           print("Since you ran out of magic, the ghost got you! You died!")
           print("Here is your final kill count:")
           print("Dragon:", dragon_count)
           print("Zombie:", zombie_count)
           print("Ghost:", ghost_count)
           print("Minotaur", minotaur_count)
           break
        else:
            print("You've slayed the ghost!")
            continue
      else:
        print("Oh no the ghost got you!")
        print("Here is your final kill count:")
        print("Dragon:", dragon_count)
        print("Zombie:", zombie_count)
        print("Ghost:", ghost_count)
        print("Minotaur", minotaur_count)
        break
    elif monster == "Minotaur":
      if user.lower() == "hammer":
        hammer_count -= 1
        minotaur_count += 1
        if hammer_count == 0:
            print("Oh no! You ran out of hammers!")
            continue
        elif hammer_count == -1:
           minotaur_count += 1
           print("Since you ran out of hammers, the Minotaur got you! You died!")
           print("Here is your final kill count:")
           print("Dragon:", dragon_count)
           print("Zombie:", zombie_count)
           print("Ghost:", ghost_count)
           print("Minotaur", minotaur_count)
           break
        else:
            print("You've slayed the Minotaur!")
            continue
      else:
        print("Oh no the minotaur got you!")
        print("Here is your final kill count:")
        print("Dragon:", dragon_count)
        print("Zombie:", zombie_count)
        print("Ghost:", ghost_count)
        print("Minotaur", minotaur_count)
        break
    else:
      print("That's not a weapon! You've been killed")
    
 