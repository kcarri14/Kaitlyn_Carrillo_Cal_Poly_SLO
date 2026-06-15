.text 
main:
#print welcome
la a0, welcome
jal printstring
#print operations
la a0, operations_string
jal printstring

li t0 'y'  #initalize choice
li t1, 0
Loop:
#print number of operations
la a0 empty_line
jal printstring
la a0 Number_of_operations
jal printstring
mv a0, t1
jal printint

addi t1, t1, 1
#print enter call for first number
la a0 empty_line
jal printstring
la a0, number1
jal printstring
#reads integer
jal readint
mv s0, a0

#print enter call for second number
la a0, number2
jal printstring
#reads integer
jal readint
mv s1, a0

#print enter call for operations
la a0, operation_selection
jal printstring
#reads string
jal readint
mv s2, a0

li t2, 1
beq s2, t2, operation_add
li t2, 2
beq s2, t2, operation_sub
li t2, 3
beq s2, t2, operation_mult
li t2,4
beq s2, t2, operation_div
li t2, 5
beq s2, t2, operation_and
li t2, 6
beq s2, t2, operation_or
li t2, 7
beq s2, t2, operation_xor

la a0, invalid_op
jal printstring
j continue_program

operation_add:
mv a0, s0
mv a1, s1
jal addnums
j print_results

operation_sub:
mv a0, s0
mv a1, s1
jal subnums
j print_results

operation_mult:
mv a0, s0
mv a1, s1
jal multnums
j print_results

operation_div:
mv a0, s0
mv a1, s1
jal divnums
j print_results

operation_and:
mv a0, s0
mv a1, s1
jal andnums
j print_results

operation_or:
mv a0, s0
mv a1, s1
jal ornums
j print_results

operation_xor:
mv a0, s0
mv a1, s1
jal xornums
j print_results

print_results:
# Print the result
la a0, result_string
jal printstring
mv a0, t3
jal printint

continue_program:
# Prompt for continuation
la a0, empty_line #print empty line
jal printstring
la a0, continue
jal printstring
la a0, choice #reads the choice inputted
jal readchar
lb a0, choice #reads first char
bne a0, t0, exit_program  
j Loop

exit_program:
la a0, empty_line #print empty line
jal printstring
la a0, Number_of_operations
jal printstring
mv a0, t1
jal printint
jal exit


.data
welcome: .string "Welcome to the Calculator Program \n"
operations_string: .string "Operations- 1. add, 2. Subtract, 3. Multiply, 4. Divide, 5. And, 6. Or, 7. XOR \n"
Number_of_operations: .string "Number of Operations performed: "
number1: .string "Enter number: "
number2: .string "Enter second number: "
operation_selection: .string "Select Operation: "
choice: .space 20
result_string: .string "Result: "
continue: .string "Continue (y/n): "
empty_line: .string " \n"
invalid_op: .string "Invalid Operation"
