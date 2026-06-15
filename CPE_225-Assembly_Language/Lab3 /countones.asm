.text
#Name: Kaitlyn Carrillo
main:
#print welcome
li a7, 4  #print string
la a0, welcome #prints "Welcome" message
ecall #calls it

li t0, 'y'  #Initalize the choice

.loop1:#print the enter
li a7 ,4 #print string
la a0, empty_line #print empty line
ecall #calls it
li a7, 4  #print string 
la a0, enter #prints "enter" message
ecall #calls it

#reads the integer that the user put in 
li a7, 5 #reads integer
ecall #calls it
mv s0, a0 #moves the number into s0 after ecall

#Call countSetBits function
mv a0, s0 #move number to a0 for argument passing
li a1, 0 #initalize count to 0
li t1, 0 #mask
li t2, 32 #biggest number of bits

.countSetBits: #count loop
beq a0, zero, .loop2 #if number is zero, end loop
andi t3, a0, 1 #Mask the least significant bit
add a1, a1, t3 #Add the masked bit to the count
srli a0, a0, 1 #shift number to the right
addi t1, t1, 1 #increment mask
blt t1, t2, .countSetBits # countinue loop if mask is less than the biggest number of bits

.loop2:#Print the number of bits set
li a7, 4 #print string
la, a0, numberbits #prints "Please enter a number
ecall  #calls it
mv a0, a1 #moves the number into a0 so that we can print it
li a7, 1 #prints integer
ecall #calls it

#Print continue
li a7 ,4 #print string
la a0, empty_line #print empty line
ecall #calls it
li a7, 4  #print string
la a0, continue #prints continue message
ecall #calls it

li a7, 8 #read string
la a0, choice #reads the choice inputted
li a1, 2 #length of choice
ecall #calls it
lb a0, choice #reads first char

bne a0, t0, .exit   #if the choice is not equal then exit the program
j .loop1 #if the choice is equal go back to loop1


.exit: #exiting program
li a7 ,4 #print string
la a0, empty_line #print empty line
ecall #calls it
li a7 ,4 #print string
la a0, exiting #prints exiting message
ecall #calls it
li a7, 10 #exit program command
ecall #calls it


.data
welcome: .string "Welcome to the CountOnes program. \n"   #string to welcome
enter: .string "Please enter a number: \n"                  #string to enter
numberbits: .string "The number of bits set is: \n"       #string to set bits
continue: .string "Continue (y/n)?: \n"                    #string to continue
exiting: .string "Exiting \n"           		 #string to exit
choice: .space 20 					 #string to give space for choice
empty_line: .string " \n"				 #string to gmove to the next line

