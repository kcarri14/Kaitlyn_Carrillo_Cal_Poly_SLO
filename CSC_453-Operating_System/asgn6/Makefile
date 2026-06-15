CC = gcc
CFLAGS = -Wall -ansi -pedantic -g

all : hello

hello : hello.o
	$(CC) -g -o hello hello.c

hello.o: hello.c
	$(CC) $(CFLAGS) -c -o hello.o hello.c

clean :
	rm -f hello.o

test: hello
	@echo "Testing Hello..."
	@echo $$(./hello)
	@echo "done."
