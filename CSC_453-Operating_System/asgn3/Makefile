CC = gcc
CFLAGS = -Wall -g -fpic 
LIB = -lpthread -lrt
MAIN = dine
SRCS = dine.c
OBJS = $(SRCS: .c=.o)

all : $(MAIN)

$(MAIN) : $(OBJS) 
	$(CC) $(OBJS) -o $(MAIN) $(LIB)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@


clean :
	rm -f $(OBJS) $(MAIN) 

run: $(MAIN)
	./$(MAIN)
