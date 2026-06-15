CC = gcc
CFLAGS = -Wall -g -fpic 
MINLS = minls
MINGET = minget
MINLS_SRC = minls.c
MINGET_SRC = minget.c
MINLS_OBJS = minls.o shared.o
MINGET_OBJS = minget.o shared.o

all : $(MINLS) $(MINGET) 

$(MINLS): $(MINLS_OBJS) 
	$(CC) $(CFLAGS) -o $@ $^

$(MINGET) : $(MINGET_OBJS)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

minls.o: shared.h
minget.o: shared.h
shared.o: shared.h

clean :
	rm -f *.o $(MINLS) $(MINGET)

run-minls: $(MINLS)
	./$(MINLS)

run-minget: $(MINGET)
	./$(MINGET)

