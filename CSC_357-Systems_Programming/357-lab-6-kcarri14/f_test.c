#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

void odd(int input){
    for(int i = 1; i <= input; i+=2){
        printf("%d\n", i);
    }
    exit(0);
}

void even(int input){
    for(int i = 2; i <= input; i+=2){
        printf("\t%d\n", i);
    }
}

int main(int argc, char *argv[]){
    int N = atoi(argv[1]);

    pid_t pid = fork();

    if(pid < 0){
        printf("Error");
        return 1;
    }else if(pid == 0){
        odd(N);
    }else{
        even(N);
    }
    return 0;
}