#Makefile
CC = gcc
CFLAGS = -Wall -g -fpic 
LIB = -I ~pn-cs453/Given/Asgn2/include
MAGIC = ~pn-cs453/Given/Asgn2/src/magic64.S
.PHONY : lwp
all : lwp

lwp : liblwp.so

liblwp.so : lwp.o magic64.o
	$(CC) $(CFLAGS) $(LIB) -shared -o $@ lwp.o magic64.o

lwp.o : lwp.c
	$(CC) $(CFLAGS) $(LIB) -c -o lwp.o lwp.c

magic64.o : $(MAGIC)
	$(CC) $(CFLAGS) -c -o $@ $(MAGIC)


clean :
	rm -f lwp.o magic64.o liblwp.so

