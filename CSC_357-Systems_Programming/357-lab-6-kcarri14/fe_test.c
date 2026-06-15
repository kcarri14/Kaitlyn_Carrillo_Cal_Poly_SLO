#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>

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

    pid_t pid1, pid2;
    
    pid1 =fork();

    if(pid1 < 0){
        printf("Error");
        return 1;
    }else if(pid1 == 0){
        execl("./odds", "odds", argv[1], (char *) NULL);
        perror("Error: failed to execute");
    }
    pid2 =fork();

    if(pid2 < 0){
        printf("Error");
        return 1;
    }else if(pid2 == 0){
        execl("./evens", "evens", argv[1], (char *) NULL);
        perror("Error: failed to execute");
    }
    waitpid(pid1, NULL, 0 );
    waitpid(pid2, NULL, 0);
    
    return 0;
}