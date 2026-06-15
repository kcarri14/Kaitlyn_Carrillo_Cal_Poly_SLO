#io
#Kaitlyn Carrillo

.text
.global printstring
.global printchar
.global readchar
.global exit
.global readstring
.global clear_buffer
.global sort_and_print


#print string
printstring:
li a7, 4
ecall
ret
 
#print char
printchar:
li a7, 11
ecall
ret

#read char  
readchar:
li a7, 12		
ecall
ret
 
#read string 
readstring:
la s1, input_buffer
addi sp, sp, -16               #set stack pointer
sw ra, 0(sp)                   #store ra into stack pointer
sw s0, 4(sp)			#store s0 into stack pointer

read_string:
jal readchar
mv t0, a0
li t6, 10
beq t0, t6, done
sb t0, 0(s1)
addi s1, s1, 1
j read_string 

done:
sb x0, 0(s1)            # Terminate string with null character
lw s0, 4(sp)		#load s0 out of stack pointer
lw ra, 0(sp)		#load ra out of stack pointer
addi sp, sp , 16        #reset stack pointer
ret

clear_buffer:
li t0, 20                      # Set counter for 20 bytes
mv t1, a0
clear_loop:
sb x0, 0(t1)                   # Store null character (zero) in buffer
addi t1, t1, 1                 # Move to next buffer position
addi t0, t0, -1                 # Decrement counter
bnez t0, clear_loop            # Repeat until counter is zero
ret                            # Return from subroutine



sort_and_print:
# Save ra and s0
addi sp, sp, -16               #set stack pointer
sw ra, 0(sp)                   #store ra into stack pointer
sw s0, 4(sp)			#store s0 into stack pointer
la s0, input_buffer            # Load address of input buffer

# Determine the length of the string
li t0, 0                       # Initialize length counter
loop1:
lb t1, 0(s0)                   # Load character from buffer
beqz t1, loop1_done           # If null character, end loop
addi t0, t0, 1                 # Increment length counter
addi s0, s0, 1                 # Move to next character
j loop1                  # Repeat loop

loop1_done:
mv t1, t0                      # Move length to t1
# Bubble sort the string in place
la s0, input_buffer            # Reset buffer pointer to start
loop2_outer:
addi t1, t1, -1                # Decrement length counter
blez t1, loop2_outer_done      # If length <= 0, sorting is done
la s0, input_buffer            # Reset buffer pointer to start
mv t2, t1                      # Set inner loop counter

loop2_inner:
lb t3, 0(s0)                   # Load current character
addi s0, s0, 1                 # Move to next character
lb t4, 0(s0)                   # Load next character
beqz t4, inner_done            # If next character is null, end inner loop
blt t3, t4, no_swap            # If current char < next char, do not swap
sb t4, -1(s0)                  # Swap characters
sb t3, 0(s0)
no_swap:
addi t2, t2, -1                # Decrement inner loop counter
bnez t2, loop2_inner     # Repeat inner loop if not zero

inner_done:
j loop2_outer            # Repeat outer loop

loop2_outer_done:
# Print the sorted string
la s0, input_buffer            # Load address of input buffer for printing

print_sorted:
lb t2, 0(s0)                   # Load character from buffer
beqz t2, end_print_sorted      # If null character, end loop
li a7, 11                      # ECALL for printchar
mv a0, t2                      # Move character to a0
ecall
addi s0, s0, 1                 # Move to next character
j print_sorted                 # Repeat loop

end_print_sorted:
li a0, 10                      # Print newline
li a7, 11                      # ECALL for printchar
ecall
# Restore ra and s0
lw s0, 4(sp)		#load s0 out of stack pointer
lw ra, 0(sp)		#load ra out of stack pointer
addi sp, sp , 16        #reset stack pointer
ret                            # Return from subroutine

#exit
exit:
li a7, 10
ecall 
ret 


