.text
main:
#print welcome
li a7, 4  #print string
la a0, welcome #prints "Welcome" message
ecall #calls it

li t0, 'y'  #Initalize the choice

.loop1:
#print the enter
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

#Call countleadingZeros function
mv a0, s0 #move number to a0 for argument passing
li a1, 0 #initalize count to 0
li t1, 0x80000000 #mask
li t3, 32 #number of bits

.countLeadingZeros:
and t2, a0, t1           # Mask the most significant bit
bnez t2, .loop2     # If the masked bit is not zero, exit loop
addi a1, a1, 1           # Increment count
slli a0, a0, 1           # Shift mask to the left
addi t3,t3, -1 
bnez t3, .countLeadingZeros  # Continue loop if mask is not zero

.loop2:
#Print the number of bits set
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

#exiting program
.exit:
li a7 ,4 #print string
la a0, empty_line #print empty line
ecall #calls it
li a7 ,4 #print string
la a0, exiting #prints exiting message
ecall #calls it
li a7, 10 #exit program command
ecall #calls it


.data
welcome: .string "Welcome to the CountOnes program. \n"
enter: .string "Please enter a number: \n"
numberbits: .string "The number of bits set is: \n"
continue: .string "Continue (y/n)?: \n"
exiting: .string "Exiting \n"
choice: .space 20
empty_line: .string " \n"

