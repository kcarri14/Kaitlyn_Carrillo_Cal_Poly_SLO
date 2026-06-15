#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>

#define BUFFER_SIZE 1

int main(int argc, char *argv[]){
    int fd;
    ssize_t bytes_read;
    char buffer[BUFFER_SIZE];
    
    fd = open("/usr/lib/locale/locale-archive",O_RDONLY);

    while ((bytes_read = read(fd, buffer, BUFFER_SIZE ) > 0)){

    }
    close(fd);

    return 0;

}