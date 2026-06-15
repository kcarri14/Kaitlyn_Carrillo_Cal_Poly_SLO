.text
.global addnums
.global subnums
.global multnums
.global divnums
.global andnums
.global ornums
.global xornums

addnums:
add a0, a0, a1 #add numbers together
mv t3, a0 #move answer to t3
ret

subnums:
sub a0, a0, a1 #subtract numbers 
mv t3, a0 #move answer to t3
ret
multnums:
li t4, 0
li t5, 0
li t6, 0

loop_mult:
bge t5, a1, end_mult
add t4, t4, a0
addi t5, t5, 1
j loop_mult

end_mult:
mv t3, t4
ret

divnums:
mv t4, a0      # Move the first number to temporary register t0
mv t5, a1      # Move the second number to temporary register t1
li a0, 0       # Initialize result register a0 to 0
beqz t5, div_end  # If second number is 0, end division

div_loop:
blt t4, t5, div_end  # If first number is less than second, end division
addi a0, a0, 1       # Increment the quotient
sub t4, t4, t5       # Subtract the second number from the first
j div_loop           # Repeat the loop

div_end:
mv t3, a0
ret

andnums:
and a0, a0, a1 #and numbers together
mv t3, a0 #move answer to t3
ret
ornums:
or a0, a0, a1 #or numbers together
mv t3, a0 #move answer to t3
ret
xornums:
xor a0, a0, a1 #xor numbers together
mv t3, a0 #move answer to t3
ret



.data
