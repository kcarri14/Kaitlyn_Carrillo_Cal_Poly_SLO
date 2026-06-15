#Kaitlyn Carrillo

.text
main:
li t0, 0 		#counter
li t1, 0xFFFF0010	#right
li t2, 0xFFFF0011	#left

li s0, 63		#0
sb s0, 0(t1)
sb s0, 0(t2)

li s1, 6		#1
li s2, 91		#2
li s3, 79		#3
li s4, 102		#4
li s5, 109		#5
li s6, 125		#6
li s7, 7		#7
li s8, 127		#8
li s9, 111		#9

loop1:
li a7, 	12
ecall

li t6, 113
beq a0, t6, exit

li t6, 32
beq a0, t6, increment_counter

j loop1

increment_counter:
addi t0, t0, 1
li t3, 100
rem t0, t0, t3

li s10, 10
div t4, t0, s10  	#Left digit(t4 = counter /10)
rem t5, t0, s10		#Right digit(t5 = counter % 10)

mv a0, t4
jal convert
mv t4, a0
mv a0, t5
jal convert
mv t5, a0

sb t5, 0(t1)
sb t4, 0(t2)

j loop1
 

convert:
beq a0, zero, set0
li s11, 1
beq a0, s11, set1
li s11, 2
beq a0, s11, set2
li s11, 3
beq a0, s11, set3
li s11, 4
beq a0, s11, set4
li s11, 5
beq a0, s11, set5
li s11, 6
beq a0, s11, set6
li s11, 7
beq a0, s11, set7
li s11, 8
beq a0, s11, set8
li s11, 9
beq a0, s11, set9

set0:
mv a0, s0
ret
set1:
mv a0, s1
ret
set2:
mv a0, s2
ret
set3:
mv a0, s3
ret
set4:
mv a0, s4
ret
set5:
mv a0, s5
ret
set6:
mv a0, s6
ret
set7:
mv a0, s7
ret
set8:
mv a0, s8
ret
set9:
mv a0, s9
ret

exit:
li a7, 10		#exit program
ecall

.data

