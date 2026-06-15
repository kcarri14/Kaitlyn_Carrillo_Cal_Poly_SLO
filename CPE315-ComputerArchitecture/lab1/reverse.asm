#Name: Kaitlyn Carrillo and Kenton Rhoden
# Section:  01
# Description: This program print the number that represents the 
# reverse-ordered binary of the given 32-bit number.


#Java
#import java.util.Scanner;
#public class Main {
#    public static void main(String[] args){
#        Scanner s = new Scanner(System.in);
#        System.out.print("Enter a Number: ");
#        int number = s.nextInt();
#        int result = 0;
#        for (int i = 0; i < 32; i++){
#            result = result << 1;
#            int rmb = number & 1;
#            result |= rmb;
#            number = number >> 1;
#        }
#        System.out.println("Result: " + result);
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
        .asciiz " This program print the number that represents the reverse-ordered binary of the given 32-bit number \n\n"

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
    addi $a0, $a0, 0x68
    syscall

    #read int
    addi $v0, $0, 5
    syscall
    
    #t0 is for result
    addi $t0, $0, 0

    #t1 is for number
    add $t1, $v0, $0

    #s0 is i in for loop
    addi $s0, $0, 0

    j loop


loop:
    #check for loop
    slti $t2, $s0, 32
    beq $t2, $0, end

    #computations
    sll $t0, $t0, 1     #result = result << 1
    andi $t3, $t1, 1    #int rmb = number & 1
    or $t0, $t0, $t3    #result |= rmb
    srl $t1, $t1, 1     #number = number >> 1

    #add 1 to loop
    addi $s0, $s0, 1
    j loop
    

end:
    
    #display prompt
    addi $v0, $0, 4
    lui $a0, 0x1001
    addi $a0, $a0, 0x7C
    syscall

    #display result
    addi $v0, $0, 1
    add $a0, $t0, $0
    syscall

    #display newline
    addi $v0, $0, 4
    lui $a0, 0x1001
    addi $a0, $a0, 0x87
    syscall

    #exit
    addi $v0, $0, 10
    syscall
