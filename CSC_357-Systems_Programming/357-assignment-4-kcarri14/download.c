#include <stdio.h>  
#include <sys/wait.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

#define max_line_length 1024

//structure to hold the line and corresponding pid for the line
typedef struct {
    pid_t pid;
    int line_number;
} ProcInfo;

int main(int argc, char *argv[]){
    // check if stdin has 3 arguments
    if (argc < 3){
        perror("Error: not enough arguments\n");
        return -1;
    }
    //put the filename address into a pointer
    char *filename = argv[1];
    // change the string number into an integer
    int number_processes = atoi(argv[2]);

    //check if number is positive int
    if(number_processes < 0){
        perror("Error: must be a postive integer\n");
        return -1;
    }

    //open file to be read
    FILE *file = fopen(filename, "r");
    if(file == NULL){
        perror("Error opening file\n");
        return 1;
    }
    //open an array to get the lines from the files
    char line_array[max_line_length];

    //initialize variables for the line number and process numbers
    int line_number = 0;
    int process_counter = 0;
    ProcInfo processes[number_processes];

    //get the line from the file
    while(fgets(line_array, sizeof(line_array), file)){
        //add 1 to line number
        line_number++;

        //tokenize the line from the file
        char *output_filename = strtok(line_array, " ");
        char *url = strtok(NULL, " \n");
        char *time = strtok(NULL, " \n");
        
        //returns if download was sucessful and the status number
        while(process_counter >= number_processes){
            int status;
            //wait for child process to finish
            pid_t finished_pid = wait(&status);
            //decrease the process counter
            process_counter--;
            //get the line associated with the process
            for(int i = 0; i < number_processes; i++){
                if(processes[i].pid == finished_pid){
                    if(WIFEXITED(status)){ //if sucessfully print complete
                        printf("Process %d processing line #%d: download complete\n", finished_pid, processes[i].line_number);
                        if(status == 0){
                            printf("Process %d complete with status %d\n", finished_pid, WEXITSTATUS(status));
                        }
                    }else{// if not successful say abornomally terminated
                        printf("Process %d abnormally terminated\n", finished_pid);
                    }
                    break;
                }
            }
        }    
        
        //fork to create processes
        pid_t pid = fork();
        if(pid < 0){
            perror("Error: Fork failed\n");
            fclose(file);
            return 1;
        }else if(pid == 0){
            // child process
            printf("Process: %d Processing line #%d: starting download\n", getpid(), line_number);
            if(time){//execute the curl function for lines with time
                execlp("curl", "curl","-m", time,"-o", output_filename,"-s", url,(char *) NULL);  
            }else{// execute the curl function for the lines without time
               execlp("curl", "curl", "-o", output_filename, "-s", url, (char *)NULL);
            }
            perror("curl");
            exit(1);
        }else{
            //parent process
            processes[process_counter++] =(ProcInfo){pid, line_number};
        }

    }
    fclose(file);

        //returns if download was sucessful and the status number
        while(process_counter > 0){
            int status;
            //wait for child process to finish
            pid_t finished_pid = wait(&status);
            //decrease the process counter
            process_counter--;
            //get the line associated with the process
            for(int i = 0; i < number_processes; i++){
                if(processes[i].pid == finished_pid || processes[i].pid == number_processes){
                    if(WIFEXITED(status)){ //if sucessfully print complete
                        printf("Process %d processing line #%d: download complete\n", finished_pid, processes[i].line_number);
                        if(status == 0){
                            printf("Process %d complete with status %d\n", finished_pid, WEXITSTATUS(status));
                        }
                    }else{// if not successful say abornomally terminated
                        printf("Process %d abnormally terminated\n", finished_pid);
                    }
                    break;
                }
            }
        }    
    return 0;
}