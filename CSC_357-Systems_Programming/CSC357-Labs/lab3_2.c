#include <stdio.h>
#include <stdlib.h>

#define BUFFER_SIZE 1

int main(int argc, char *argv[]){
    FILE *fp;
    ssize_t bytes_read;
    char buffer[BUFFER_SIZE];
    
    fp = fopen("/usr/lib/locale/locale-archive","r");

    while ((bytes_read = fread(buffer,1, BUFFER_SIZE, fp) > 0)){

    }
    fclose(fp);

    return 0;

}