.text
.global printint
.global printstring
.global readchar
.global readint
.global exit


printint:
li a7, 1
ecall
ret
printstring:
li a7, 4
ecall
ret
readchar:
li a7, 8
li a1, 2 #length of choice
ecall
ret

readint:
li a7, 5
ecall
ret

exit: #exiting program
li a7 ,4 #print string
la a0, empty_line #print empty line
ecall #calls it
li a7 ,4 #print string
la a0, exiting #prints exiting message
ecall #calls it
li a7, 10 #exit program command
ecall #calls it
ret
.data
exiting: .string "Exiting"
empty_line: .string " \n"
