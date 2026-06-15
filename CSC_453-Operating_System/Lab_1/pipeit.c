#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>
int main (){
    //create file descriptors for pipe and outfile
    int fd[2];
    int outfile_fd;
    int status_pid1;
    int status_pid2;
    // create a pip for interprocess communication
    if(pipe(fd) == -1){
        perror("Error: pipe failed");
    }

    // fork 2 children one for ls and the other for sort -r
    pid_t pid1 = fork(); 
    if(pid1 < 0){
        perror("Error: fork failed");
    }else if(pid1 == 0){
        //redirecting the stdout to the pipes write end 
        //so ls can write its output to the pipe
        dup2(fd[1], STDOUT_FILENO);
        close(fd[0]);
        close(fd[1]);

        //exec ls in this fork
        char *ls_arg[] = {"ls", NULL};
        execvp("ls", ls_arg);
        
        perror("error in execvp");
    }
    pid_t pid2 = fork();
    if(pid2 < 0){
        perror("Error: fork failed");
    }else if(pid2 == 0){
        //read in what the pipe has which is the files
        dup2(fd[0], STDIN_FILENO);
        outfile_fd = open("outfile", O_WRONLY | O_CREAT | O_TRUNC, 
        S_IRUSR |S_IWUSR |S_IRGRP| S_IROTH );
        if (outfile_fd == -1){
            perror("error opening outfile");
        }
        //change the stdout to the outfile so that the file 
        //names are placed into the outfile
        dup2(outfile_fd, STDOUT_FILENO);
        close(outfile_fd);
        close(fd[0]);
        close(fd[1]);
    
        //executes the sort and reverse
        char *sort_args[] = {"sort", "-r", NULL};
        execvp("sort", sort_args);

        perror("error in execvp");
    }
    close(fd[0]);
    close(fd[1]);

    //waits for the proccess to terminate with correct pid
    wait(&status_pid1);
    wait(&status_pid2);

    if(WIFEXITED(status_pid1) && WIFEXITED(status_pid2)){
        int exit1 = WEXITSTATUS(status_pid1);
        int exit2 = WEXITSTATUS(status_pid2);
        if ((exit1 == 0) && (exit2 == 0)){
            printf("ls | sort -r > outfile complete!\n");
            return EXIT_SUCCESS;
        }
        else{
            if(exit1 != 0){
        printf("the ls fork exited unsuccessfully on status %d\n", exit1);
            }else if (exit2 != 0) {
        printf("the sort fork unsuccessfully on exited on status %d\n", exit2);
            }else if ((exit1 != 0) && (exit2 != 0)){
        printf("the ls fork exited unsuccessfully on status %d\n", exit1);
        printf("the sort fork exited unsuccessfully on status %d\n", exit2);
            }
            return EXIT_FAILURE;
        }

    }
   //hi
}