#Name: Kaitlyn Carrillo and Kenton Rhoden
# Section:  01
# Description: This program takes in 2 32-bit numbers to represent a 64-bit unsigned number,
# then divides that with a 31 bit unsigned number that must be a power of 2.
# The answer should be printed out as 2 32-bit numbers.

#Java
# import java.util.Scanner;
# 
# 
# public class divide {
# 	public static void main(String[] args){
# 		Scanner s = new Scanner(System.in);
# 		System.out.print("Enter a number for the UPPER 32-bits of a dividend: ");
# 		int dividendHi = s.nextInt();
# 		System.out.print("Enter a number for the LOWER 32-bits of a dividend: ");
# 		int dividendLo = s.nextInt();
# 		System.out.print("Enter a divisor: ");
# 		int divisor = s.nextInt();
# 
# 		int shift = 0;
# 		int temp = divisor;
# 		while(temp > 1) {
# 			temp = temp >> 1;
# 			shift ++;
# 		}
# 
# 		int loBits = dividendLo >> shift;
# 		int hiUnderflow = dividendHi << (32 - shift);
# 		int newLo = loBits | hiUnderflow;
# 
# 		int newHi = dividendHi >> shift;
# 
# 		System.out.println("Result: " + newHi + ", " + newLo);
# 	}
# }


#MIPS Assembly

# declare globals so we can see addresses
.globl welcome

# data area
.data

welcome:
	.asciiz "This program takes in 2 32-bit numbers to represent a 64-bit unsigned number, then divides that with a 31 bit unsigned number that must be a power of 2. The answer should be printed out as 2 32-bit numbers\n\n" # 208 chars (0x10010000)
upperprompt:
	.asciiz "Enter a number for the UPPER 32-bits of the dividend: " # 55 chars (0x100100d0)
lowerprompt:
	.asciiz "Enter a number for the LOWER 32-bits of the dividend: " # 55 chars (0x10010107)
divisorprompt:
	.asciiz "Enter a divisor: " # 18 chars (0x1001013e)
resultprompt:
	.asciiz "\nResult: " # 10 chars (0x10010150)
comma:
	.asciiz ", " # 3 chars (0x1001015a)
newline:
	.asciiz "\n" # 2 chars (0x1001015d)

# text area
.text

main:
	# print welcome message
	addi	$v0, $0, 4
	lui	$a0, 0x1001
	syscall

	# prompt user for dividendHi
	addi	$v0, $0, 4
	lui	$a0, 0x1001
	addi	$a0, $a0, 0xd0
	syscall

	# get and store dividendHi
	addi	$v0, $0, 5
	syscall
	add	$s0, $0, $v0

	# prompt user for dividendLo
	addi	$v0, $0, 4
	lui	$a0, 0x1001
	addi	$a0, $a0, 0x107
	syscall

	# get and store dividendLo
	addi	$v0, $0, 5
	syscall
	add	$s1, $0, $v0

	# prompt user for divisor
	addi	$v0, $0, 4
	lui	$a0, 0x1001
	addi	$a0, $a0, 0x13e
	syscall

	# get and store divisor
	addi	$v0, $0, 5
	syscall
	add	$s2, $0, $v0

	# print result prompt
	addi	$v0, $0, 4
	lui	$a0, 0x1001
	addi	$a0, $a0, 0x150
	syscall

	# zero var for shift amount
	addi	$s3, $0, 0
	# temp var for finding shift amount
	add	$t0, $0, $s2
	# temp for value 1
	addi	$t1, $0, 1

	# calculate shift amount
	startWhile:
		ble	$t0, $t1, afterWhile

		# shift temp by 1 right and increment shift var
		srl	$t0, $t0, $t1
		addi	$s3, $s3, 1

		b	startWhile
	afterWhile:

	# hiBits $s0; loBits $s1; divisor $s2

	# calculate lo bits
	srl	$s1, $s1, $s3

	# calculate underflow from hi bits
	addi	$t0, $0, 32
	sub	$t0, $t0, $s3
	sll	$t1, $s0, $t0

	# merge underflow and lo bits
	or	$s1, $s1, $t1

	# calculate final hi bits
	srl	$s0, $s0, $s3

	# print hiBits
	addi $v0, $0, 1
	add $a0, $0, $s0
	syscall

	# print ", "
	addi	$v0, $0, 4
	lui	$a0, 0x1001
	addi	$a0, $a0, 0x15a
	syscall

	# print loBits
	addi	$v0, $0, 1
	add	$a0, $0, $s1
	syscall

	# print newline
	addi	$v0, $0, 4
	lui	$a0, 0x1001
	addi	$a0, $a0, 0x15d
	syscall

	# exit
	addi	$v0, $0, 10
	syscall
