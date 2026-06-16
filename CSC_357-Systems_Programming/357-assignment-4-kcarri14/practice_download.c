#include <stdio.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

#define max_line_length 1024
int main(int argc, char *argv[]){
    if (argc < 3){
        perror("Error: not enough arguments");
        return -1;
    }
    char *filename = argv[1];
    int number = atoi(argv[2]);
    printf("Number of arguments: %d\n", number);
    if(number < 0){
        perror("Error: must be a postive integer");
        return -1;
    }

    FILE *file = fopen(filename, "r");
    if(file == NULL){
        perror("Error opening file");
        return 1;
    }
    char line_array[max_line_length];
    int line_number = 0;
    int process_counter = 0;

    while(fgets(line_array, sizeof(line_array), file)){
        line_number++;
        char *output_filename = strtok(line_array, " ");
        char *url = strtok(NULL, " ");
        char *time = strtok(NULL, " \n");

        if(!output_filename || !url){
            perror("Error: invalid format\n");
        }

            pid_t pid = fork();
            if(pid < 0){
                perror("Error: Fork failed");
                fclose(file);
                return 1;
            }else if(pid == 0){
                printf("Process: %d Processing line #%d: starting download\n", getpid(), line_number);
                if (time){
                    execlp("curl", "curl","-m", time,"-o", output_filename,"-s", url,(char *) NULL);
                }else{
                    execlp("curl", "curl","-o", output_filename,"-s", url, (char *) NULL);
                }
                    perror("curl");
            }else{
                process_counter++;
            }

            if(process_counter >= number){
            int status;
            pid_t finished_pid = wait(&status);
            process_counter--;
            if(WIFEXITED(status)){
                printf("Process %d processing line #%d: download complete\n", finished_pid, line_number);
                printf("Process %d complete\n", finished_pid);
            }else{
                printf("Process %d abnormally terminated", finished_pid);
            }
            
        }  

    }

        fclose(file);

        while(process_counter > 0){
            int status;
            pid_t pid_finished = wait(&status);
            process_counter--;
            if(WIFEXITED(status)){
                printf("Process %d processing line #%d: download complete\n", pid_finished, line_number);
                printf("Process %d complete with status %d\n", pid_finished, WEXITSTATUS(status));
            }else{
                printf("Process %d abnormally terminated\n", pid_finished);
            }
        }
    
    return 0;
}