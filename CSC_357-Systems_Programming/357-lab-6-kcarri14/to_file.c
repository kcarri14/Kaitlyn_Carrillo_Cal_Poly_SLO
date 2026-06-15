#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main(int argc, char* argv[]){
    if (argc != 3){
        perror("Error: not enough arguments");
    }
    char *other_program = argv[1];
    char *file_name = argv[2];

    int fd;
    fd = dup(STDOUT_FILENO);

    int file_fd = open(file_name, O_WRONLY |O_CREAT, 0644);

    execl(other_program, other_program, NULL);

    dup2(file_fd, STDOUT_FILENO);

    close(file_fd);

   
}