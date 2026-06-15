#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>
#include <stdlib.h>

pid_t pid;

void alarm_handler(int signal){
    if(pid > 0){
        kill(pid, SIGKILL);
    }
}

int main(int argc, char* argv[]){
    if(argc < 3){
        perror("Error: need the number of seconds");
        return -1;
    }
    int timeout = atoi(argv[1]);
    if(timeout <= 0){
        perror("Error: time cannot be negative");
        return -1;
    }

    struct sigaction signal_alarm;
    signal_alarm.sa_handler = alarm_handler;
    signal_alarm.sa_flags = 0;
    sigemptyset(&signal_alarm.sa_mask);
    if(sigaction(SIGALRM, &signal_alarm, NULL)== -1){
        perror("Error: sigaction no working");
        return 1;
    }

    pid = fork();

    if(pid < 0){
        perror("Error: fork failed");

    }else if(pid == 0){
        execvp(argv[2], &argv[2]);
        perror("Error: failed exec");
    }else{
        alarm(timeout);
        int status;
        pid_t result_wait = waitpid(pid, &status, 0);

        if(result_wait == -1){
            perror("Error: abnormal termination");
            return 1;
        }

        alarm(0);

        if(WIFEXITED(status)){
            return WEXITSTATUS(status);
        }else{
            return 1;
        }
    }

}