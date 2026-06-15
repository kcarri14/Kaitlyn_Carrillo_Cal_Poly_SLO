#include <stdio.h>
#include <string.h>
#include <stdlib.h>


int main(int argc, char *argv[]){
    char line[1024];
    char *token;
    char *delim = " \t\n";

    while (fgets(line, sizeof(line), stdin) != NULL){
        char *ptr = line;
        while((token = strsep(&ptr, delim)) != NULL){
            if(*token != '\0'){
                printf("%s\n", token);
            }
        }
    }
    return 0;

}