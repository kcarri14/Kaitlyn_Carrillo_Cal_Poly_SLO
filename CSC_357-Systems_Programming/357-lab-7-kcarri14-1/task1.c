#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(int argc, char* argv[]){

    int pipe_parent_to_1[2];
    int pipe_1_to_2[2];
    int pipe_2_to_parent[2];

    if(pipe(pipe_parent_to_1) == -1 || pipe(pipe_1_to_2) == -1 || pipe(pipe_2_to_parent) == -1){
        perror("Error: pipr failed");
    }

    pid_t pid1 = fork();
    pid_t pid2 = fork();

    if(pid1 < 0){
        perror("Error: fork failed");
    }else if(pid1 == 0){
        close(pipe_parent_to_1[1]);
        close(pipe_1_to_2[0]);
        close(pipe_2_to_parent[0]);
        close(pipe_2_to_parent[1]);

        int number;
        while(read(pipe_parent_to_1[0], &number, sizeof(number)) > 0){
            number *= number;
            write(pipe_1_to_2[1], &number, sizeof(number));
        }

        close(pipe_parent_to_1[0]);
        close(pipe_1_to_2[1]);
    }


    if(pid2 < 0){
        perror("Error: fork failed");
    }else if(pid2 == 0){
        close(pipe_parent_to_1[0]);
        close(pipe_parent_to_1[1]);
        close(pipe_1_to_2[1]);
        close(pipe_2_to_parent[0]);
        

        int number;
        while(read(pipe_1_to_2[0], &number, sizeof(number)) > 0){
            number += 1;
            write(pipe_2_to_parent[1], &number, sizeof(number));
        }

        close(pipe_2_to_parent[1]);
        close(pipe_1_to_2[0]);
    }
    close(pipe_parent_to_1[0]);
    close(pipe_1_to_2[0]);
    close(pipe_1_to_2[1]);
    close(pipe_2_to_parent[1]);

    int number;
    while(scanf("%d", &number) == 1){
        write(pipe_parent_to_1[1],&number, sizeof(number));

        if(read(pipe_2_to_parent[0], &number, sizeof(number))> 0){
            printf("%d", number);
        }
    }

    close(pipe_parent_to_1[1]);
    close(pipe_2_to_parent[0]);

    waitpid(pid1, NULL, 0);
    waitpid(pid2, NULL, 0);
   
}