#Name: Kaitlyn Carrillo and Kenton Rhoden
# Section:  01
# Description: This takes in a number and a divisor where the divisor
# is a guaranteed power of 2 and does the modulus operation. 

#Java
#import java.util.Scanner;
#public class Main {
#    public static void main(String[] args){
#        Scanner s = new Scanner(System.in);
#        System.out.print("Enter a Number: ");
#        int number = scanner.nextInt();
#        System.out.print("Enter a Divisor: ");
#        int divisor = scanner.nextInt();
#
#        int remainder = number & (divisor - 1);
#
#        System.out.println("Remainder: " + remainder);
#    }
#
#}

#MIPS Assembly

#declare globals
.globl welcome
.globl prompt
.globl result

.data

welcome: 
        .asciiz " This program does modulus operation\n"

prompt:
        .asciiz " Enter an integer: "

result: 
        .asciiz " Result = "

newline:
        .asciiz "\n"

.text

main:
    #display the welcome message
    addi $v0, $0, 4
    lui $a0, 0x1001
    syscall

    #display prompt
    addi $v0, $0, 4
    lui $a0, 0x1001
    addi $a0, $a0, 0x26
    syscall

    #read int
    addi $v0, $0, 5
    syscall

    #put number in $t0
    addi $t0, $v0, 0

    #display prompt
    addi $v0, $0, 4
    lui $a0, 0x1001
    addi $a0, $a0, 0x26
    syscall

    #read int
    addi $v0, $0, 5
    syscall

    #t1 is for divsor
    add $t1, $v0, $0

    #computation
    addi $t3, $0, 1
    sub $t1, $t1, $t3
    and $t2, $t0, $t1

    #display prompt
    addi $v0, $0, 4
    lui $a0, 0x1001
    addi $a0, $a0, 0x3A
    syscall

    #display result
    addi $v0, $0, 1
    add $a0, $t2, $0
    syscall

    #display newline
    addi $v0, $0, 4
    lui $a0, 0x1001
    addi $a0, $a0, 0x45
    syscall

    #exit
    addi $v0, $0, 10
    syscall