.text

main:
li a6, 1
li a7, 4
la a0, number
ecall
jal factorial



factorial:
beq a0, a6, base_case
addi sp, sp, -16
sw ra, 0(sp)
sw a0, 4(sp)
addi a0, a0, -1
jal factorial
lw a1, 4(sp)
lw ra, 0(sp)
mul a0, a0, a1
addi sp, sp, 16
ret

base_case:
li a0, 1
ret

.data
number: "Enter Number: "
array: .space 20
