.text


main:
li s10, -1
li s11, 1
#head
li a0, 30
li a1, 100
li a2, 20
jal circle

#body
li a0, 30
li a1, 30
li a2, 80
li a3, 30
jal line

#left leg
li a0, 20
li a1, 30
li a2, 1
li a3, 30
jal line

#right leg
li a0, 40
li a1, 30
li a2, 1
li a3, 30
jal line

#left arm
li a0, 15
li a1, 30
li a2, 60
li a3, 50
jal line

#right arm
li a0, 30
li a1, 45
li a2, 50
li a3, 60
jal line

#left eye
li a0, 24
li a1, 105
li a2, 3
jal circle

#right eye
li a0, 36
li a1, 105
li a2, 3
jal circle

#mouth center
li a0, 25
li a1, 35
li a2, 90
li a3, 90
jal line

#mouth left
li a0, 25
li a1, 20
li a2, 90
li a3, 95
jal line

#mouth right
li a0, 35
li a1, 40
li a2, 90
li a3, 95
jal line



plot:
addi sp, sp, -12
sw ra, 8(sp)
sw a0, 4(sp)
sw a1, 0(sp)
la t0, bitmap_base
lw t0, 0(t0)
li t3, 256
sub a1, t3, a1
slli t1, a1, 8
add t1, t1, a0
slli t1, t1, 2
add t1, t1, t0
li t2, 0xFFFFFF
sw t2, 0(t1)
lw a0, 4(sp)
lw a1, 0(sp)
lw ra, 8(sp)
addi sp, sp 12
ret

abs:
bgez a0, abs_end
mul a0, a0, s10
ret

abs_end:
ret

circle:
# a0 = xc
# a1 = yc
# a2 = r


addi sp, sp, -32
sw ra, 0(sp)   
sw a0, 4(sp)     	#a0 = xc
sw a1, 8(sp)	 	# a1 = yc
sw a2, 12(sp)    	# a2 = r

li t0, 0     		#x= 0 = t0
mv t1, a2		# y = r = t1
add s2, a2, a2		# s2 = 2 * r
addi t2, s2, -3 	# g = 3 - 2 * r =t2
not t2,t2
addi t2, t2, 1 
add s3, s2, s2  	# s2 = 4 * r
addi t3, s3, -10	# diagonalInc = 10 - 4 * r = t3
not t3,t3
addi t3,t3,1
li t4, 6		# rightInc = 6 =t4

sw t0, 16(sp)		#Save x
sw t1, 20(sp)		#Save y
sw t2, 24(sp)		#Save g
sw t3, 28(sp)		#Save diagonalInc
sw t4, 32(sp)		#Save rightInc
circle_loop:

lw t0, 16(sp)		#load x
lw t1, 20(sp)		#load y

bgt t0, t1, circle_end	#while x<= y
lw t5, 4(sp)		# xc
lw t6, 8(sp)		#yc

add a0, t5, t0   	#(xc+x)
add a1, t6, t1		#(yc+y)

jal plot 

lw t5, 4(sp)
lw t6, 8(sp)
lw t0, 16(sp)
lw t1, 20(sp)
add a0, t5, t0		#(xc+x)
mul t1, t1, s10
add a1, t6, t1		#(yc-y)

jal plot 

lw t5, 4(sp)
lw t6, 8(sp)
lw t0, 16(sp)
lw t1, 20(sp)
mul t0, t0, s10
add a0, t5, t0		#(xc-x)
add a1, t6, t1		#(yc+y)

jal plot

lw t5, 4(sp)
lw t6, 8(sp)
lw t0, 16(sp)
lw t1, 20(sp)
mul t0, t0, s10
add a0, t5, t0		#(xc-x)
mul t1, t1, s10
add a1, t6, t1		#(yc-y)

jal plot 

lw t5, 4(sp)
lw t6, 8(sp)
lw t0, 16(sp)
lw t1, 20(sp)
add a0, t5, t1		#(xc+y)
add a1, t6, t0		#(yc+x)

jal plot 

lw t5, 4(sp)
lw t6, 8(sp)
lw t0, 16(sp)
lw t1, 20(sp)
add a0, t5, t1		#(xc+y)
mul t0, t0, s10
add a1, t6, t0		#(yc-x)

jal plot 

lw t5, 4(sp)
lw t6, 8(sp)
lw t0, 16(sp)
lw t1, 20(sp)
mul t1, t1, s10
add a0, t5, t1		#(xc-y)
add a1, t6, t0		#(yc+x)

jal plot 

lw t5, 4(sp)
lw t6, 8(sp)
lw t0, 16(sp)
lw t1, 20(sp)
mul t1, t1, s10
add a0, t5, t1		#(xc-y)
mul t0, t0, s10
add a1, t6, t0		#(yc-x)

jal plot 

lw t2, 24(sp)
bltz t2, rightstep


diagonal_step:
lw t1, 20(sp)
lw t2, 24(sp)
lw t3, 28(sp)
add t2, t2, t3
addi t3, t3, 8
addi t1, t1, -1
sw t1, 20(sp)
sw t2, 24(sp)
sw t3, 28(sp)
j circle_update

rightstep:
lw t2, 24(sp)
lw t3, 28(sp)
lw t4, 32(sp)
add t2, t4, t2
addi t3, t3, 4
sw t2, 24(sp)
sw t3, 28(sp)
sw t4, 32(sp)
circle_update:
lw t0, 16(sp)
lw t4, 32(sp)
addi t4, t4, 4
addi t0, t0, 1
sw t0, 16(sp)
sw t4, 32(sp)

j circle_loop

circle_end:
lw ra, 0(sp)
lw a0, 4(sp)
lw a1, 8(sp)
lw a2, 12(sp)
addi sp, sp 32
ret

line:
# a0 = x0
# a1 = x1
# a2 = y0
# a3 = y1

addi sp, sp, -48
sw ra, 0(sp)   
sw a0, 4(sp)    	#x0 	 
sw a1, 8(sp)		#x1	 	
sw a2, 12(sp)   	#y0 	
sw a3, 16(sp)		#y1

#abs(y1-y0)
lw t0, 12(sp)
lw t1, 16(sp)
mul t0, t0, s10
add t2, t1, t0		#t0 = y1-y0
mv a0, t2
jal abs
mv t2, a0
sw t2, 20(sp)

#abs(x1-x0)
lw t0, 4(sp)
lw t1, 8(sp)
mul t0, t0, s10
add t2, t1, t0		#t1 = x1 - x0
mv a0, t2
jal abs
mv t2, a0
sw t2, 24(sp)

#if abs(y1-y0) > abs(x1 - x0)
lw t0, 20(sp)
lw t1, 24(sp)
bgt t0, t1, line_swap
li t2, 0                #st = t2
sw t2, 28(sp)
j check_x0_x1

line_swap:
li t2, 1
sw t2, 28(sp)

#if st==1, swap(x0,y0) and swap(x1,y1)
check_x0_x1:
lw t2, 28(sp)
beq t2, zero, line_next

#swap x0 and y0
lw a0, 4(sp)
lw a2, 12(sp)
mv t3, a0		#t3 temporary register, move x0 into t3
mv a0, a2  		#move y0 into a0 
mv a2, t3		#move x0 into a2

sw a0, 4(sp)
sw a2, 12(sp)

#swap x1 and y1
li t3, 0
lw a1, 8(sp)
lw a3, 16(sp)
mv t3, a1		#t3 temporary register, move x1 into t3
mv a1, a3  		#move y1 into a1 
mv a3, t3		#move x1 into a3

sw a1, 8(sp)
sw a3, 16(sp)

line_next:
#if x0 >x1, swap(x0, x1) and swap(y0, y1)
lw t0, 4(sp)
lw t1, 8(sp)
blt t0, t1, line_calc

lw a0, 4(sp)
lw a1, 8(sp)
mv t3, a0		#t3 temporary register, move x0 into t3
mv a0, a1  		#move x1 into a0 
mv a1, t3		#move x0 into a2

sw a0, 4(sp)
sw a1, 8(sp)

lw a2, 12(sp)
lw a3, 16(sp)
mv t3, a2		#t3 temporary register, move y0 into t3
mv a2, a3  		#move y1 into a0 
mv a3, t3		#move y0 into a2

sw a2, 12(sp)
sw a3, 16(sp)

line_calc:
#error
li t4, 0 		#t4 = error
sw t4, 32(sp)
#y=y0
lw t5, 12(sp)		#y = t5
sw t5, 36(sp)

#deltax
lw a0, 4(sp)
lw a1, 8(sp)
mul a0, a0, s10
add t6, a1, a0
sw t6, 40(sp)

#deltay
lw t0, 12(sp)
lw t1, 16(sp)
mul t0, t0, s10
add t2, t1, t0		#t0 = y1-y0
mv a0, t2
jal abs
mv t2, a0
sw t2, 20(sp)

#if y0 < y1, ystep =1 else ystep = -1
lw t5, 4(sp)
sw t5, 48(sp)
lw a2, 12(sp)
lw, a3, 16(sp)
blt a2, a3, line_ystep
li t6, -1  		# t6 or 44(sp) = y_step
sw t6, 44(sp)
j loop

line_ystep:
li t6, 1
sw t6, 44(sp)


loop:
lw t0, 48(sp)
lw t1, 8(sp)
bgt t0, t1, line_end

lw t2, 28(sp)
beq t2, zero, plot2

lw t5, 36(sp)
lw t3, 48(sp) #x = t3
mv a0, t5
mv a1, t3
jal plot
j line_plt

plot2:
lw t5, 36(sp)
lw t3, 48(sp) #x = t3
mv a0, t3
mv a1, t5
jal plot


line_plt:
lw t1, 32(sp)
lw t2, 20(sp)
add t1, t1, t2		#error = error +deltay
sw t1, 32(sp)

lw t1, 32(sp)
slli t3, t1, 1		# 2*error
lw t5, 40(sp)
blt t3, t5, increment_x

#y=y+y_step
lw t4, 36(sp)
lw t5, 44(sp)
add t4, t4, t5
sw t4, 36(sp)


lw t4, 32(sp)
lw t5, 40(sp)
mul t5, t5, s10
add t4, t4, t5
sw t4, 32(sp)


increment_x:
lw t0, 48(sp)
addi t0, t0, 1
sw t0, 48(sp)
j loop

line_end:
lw ra, 0(sp)            # Restore return address
lw a0, 4(sp)            # Restore x0
lw a1, 8(sp)            # Restore x1
lw a2, 12(sp)           # Restore y0
lw a3, 16(sp)           # Restore y1
addi sp, sp, 48         # Deallocate stack space
ret




.data
bitmap_base: .word 0x10010000