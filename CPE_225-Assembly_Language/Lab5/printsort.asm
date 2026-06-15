#PrintSort 
#Kaitlyn Carrillo

.text

main:
la a0, new_line   	#load newline
jal printstring		#jump to printstring in io.asm   

la a0, enter_word	#load enter word
jal printstring		#jump to printstring in io.asm

la a0, input_buffer	#load input buffer
jal clear_buffer	#jump to clear_buffer in io.asm
la a0, input_buffer	#load input buffer
jal readstring		#jump to readstring in io.asm


la a0, input_buffer
lb t0, 0(a0)
beqz t0, exit1

la a0, og_word		#load original work
jal printstring		#jump to printstring in io.asm

la a0, input_buffer	#load input buffer
jal printstring		#jump to printstring in io.asm

la a0, new_line		#load new line
jal printstring		#jump to printstring in io.asm

la a0, a_word		#load alphabetized word
jal printstring		#jump to printstring in io.asm

jal sort_and_print	#jump to print_and_sort in io.asm               

j main		#jump to main in printsort.asm

#exit
exit1:
la a0, exit_word
jal printstring
jal exit		#jump to exit in io.asm

.data 
.global input_buffer
enter_word: .string "Enter word: "
og_word: .string "Original word: "
a_word: .string "Alphabetized word: "
new_line: .string "\n"
input_buffer: .space 20
exit_word: .string "Exiting"
