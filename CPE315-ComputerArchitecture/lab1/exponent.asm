#Name: Kaitlyn Carrillo and Kenton Rhoden
# Section:  01
# Description: This does the exponention of two numbers x and y.

#Java
#import java.util.Scanner;
#public class Main {
#    public static void main(String[] args){
#        System.out,print("This program does the exponenetation of two numbers x and y\n")
#        Scanner s = new Scanner(System.in);
#        System.out.print("Enter number x: ");
#        int x = scanner.nextInt();
#        System.out.print("Enter number y: ");
#        int y = scanner.nextInt();
#        System.out.println("Result: " + exponential(x, y));
#    }
#    public static int exponential(int base, int exponent){
#        if (exponent == 0){
#            return 1;
#        }else{
#            int result = base;
#            for(int i = 0; i < exponent - 1; i++){
#               result = multiply(result, base);
#            }
#            return result;
#       }
#     }
#     public static int multiply(int x, int y){
#        int result = 0;
#        for(int i = 0; i < y; i++){
#            result += x;
#        }
#       return result;
#     }
#
#}


#MIPS Assembly

# declare globals so we can see addresses
.globl welcome

# data area
.data

welcome:
	.asciiz "This program does the exponenetation of two numbers x and y\n\n"
xprompt:
	.asciiz "Enter number x: "
yprompt:
	.asciiz "Enter number y: "
resultprompt:
	.asciiz "\nResult: "
newLine:
	.asciiz "\n"

# text area
.text

main:
	# print welcome message
	addi	$v0, $0, 4
	lui	$a0, 0x1001
	syscall

	# prompt user for x
	addi	$v0, $0, 4
	lui	$a0, 0x1001
	addi	$a0, $a0, 0x3e
	syscall

	# get x from user
	addi	$v0, $0, 5
	syscall

	# store x in $s0
	add	$s0, $0, $v0

	# prompt user for y
	addi	$v0, $0, 4
	lui	$a0, 0x1001
	addi	$a0, $a0, 0x4f
	syscall

	# get y from user
	addi	$v0, $0, 5
	syscall

	# store y in $s1
	add	$s1, $0, $v0

	# print result prompt
	addi	$v0, $0, 4
	lui	$a0, 0x1001
	addi	$a0, $a0, 0x60
	syscall

	# call exponential function (base: $a0, exponent: $a1)
	add	$a0, $0, $s0
	add	$a1, $0, $s1
	jal	exponential

	# save function result
	add	$s2, $0, $v0

	# print result from function
	addi	$v0, $0, 1
	add	$a0, $0, $s2
	syscall

	# print newline
	addi	$v0, $0, 4
	lui	$a0, 0x1001
	addi	$a0, $a0, 0x6a
	syscall

	# exit
	addi	$v0, $0, 10
	syscall

exponential: # (base: $a0, exponent: $a1)
	# push return addr and save reg to stack
	addi	$sp, $sp, -12
	sw	$ra, 0($sp)
	sw	$s0, 4($sp)
	sw	$s1, 8($sp)

	# save arguments
	add	$s0, $0, $a0
	add	$s1, $0, $a1

	# if for exp > 0
	bgt	$a1, $0, expGreater0

	# if exp = 0 return 1 (save result in $s2)
		addi	$s2, $0, 1
		b	after

	# if exp > 0 multiply exp times
	expGreater0:
		# temp for iterator i
		addi	$s3, $0, 0

		# temp for iterator conditional
		addi	$t0, $0, 1
		sub	$s4, $a1, $t0

		# initialize result
		add	$s2, $0, $a0

		expLoopStart:
			# conditional
			bge	$s3, $s4, expLoopEnd

			# call multiply
			# base = $s0; exponent = $s1; result = $s2
			add	$a0, $0, $s2
			add	$a1, $0, $s0
			jal	multiply
			add	$s2, $0, $v0

			# increment i
			addi	$s3, $s3, 1

			# restart loop
			b 	expLoopStart
		expLoopEnd:

	# leave if statement
	after:

	# store result in return register
	add	$v0, $0, $s2

	# pop return addr and save reg to stack
	lw	$ra, 0($sp)
	lw	$s0, 4($sp)
	lw	$s1, 8($sp)
	addi	$sp, $sp, 12

	# return
	jr	$ra

multiply: # (x: $a0, y: $a1)
	# push save reg to stack
	addi	$sp, $sp, -20
	sw	$s0, 0($sp)
	sw	$s1, 4($sp)
	sw	$s2, 8($sp)
	sw	$s3, 12($sp)
	sw	$s4, 16($sp)

	# temp for iterator i
	addi	$t0, $0, 0
	# initialize result
	addi	$v0, $0, 0

	# for loop
	multLoopStart:
		# conditional
		bge	$t0, $a1, multLoopEnd

		# add x to result
		add	$v0, $v0, $a0

		# increment i
		addi	$t0, $t0, 1
		
		# restart loop
		b	multLoopStart
	multLoopEnd:

	# pop save reg from stack
	lw	$s0, 0($sp)
	lw	$s1, 4($sp)
	lw	$s2, 8($sp)
	lw	$s3, 12($sp)
	lw	$s4, 16($sp)
	addi	$sp, $sp, 20

	# return
	jr	$ra
