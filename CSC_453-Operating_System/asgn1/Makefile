#Makefile
CC = gcc
CFLAGS = -Wall -g -fpic -std=c99

.PHONY : malloc

all : malloc

intel-all : lib/libmalloc.so lib64/libmalloc.so

lib/libmalloc.so : lib malloc32.o
	$(CC) $(CFLAGS) -m32 -shared -o $@ malloc32.o

lib64/libmalloc.so: lib64 malloc64.o
	$(CC) $(CFLAGS) -shared -o $@ malloc64.o

lib: 
	mkdir lib

lib64: 
	mkdir lib64

malloc32.o: malloc_lib.c
	$(CC) $(CFLAGS) -m32 -c -o  malloc32.o malloc_lib.c

malloc64.o: malloc_lib.c
	$(CC) $(CFLAGS) -m64 -c -o  malloc64.o malloc_lib.c



malloc : libmalloc.a libmalloc.so

libmalloc.a : malloc.o
	ar r libmalloc.a malloc.o
	ranlib libmalloc.a

libmalloc.so : malloc.o
	$(CC) $(CFLAGS)  -shared -o $@ malloc.o

malloc.o : malloc_lib.c
	$(CC) $(CFLAGS) -c -o malloc.o malloc_lib.c
	

clean :
	rm -f malloc64.o malloc32.o malloc.o
