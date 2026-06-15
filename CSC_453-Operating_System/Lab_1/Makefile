#Makefile
CC = gcc
CFLAGS = -Wall -std=c99 -pedantic -g
MAIN = pipeit
SRCS = pipeit.c
OBJS = $(SRCS: .c=.o)

all : $(MAIN)

$(MAIN) : $(OBJS) 
	$(CC) $(OBJS) -o $(MAIN)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@


clean :
	rm -f $(OBJS) $(MAIN) 

run: $(MAIN)
	./$(MAIN)