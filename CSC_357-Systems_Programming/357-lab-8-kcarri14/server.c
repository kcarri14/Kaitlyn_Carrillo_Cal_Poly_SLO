#define _GNU_SOURCE
#include "net.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define PORT 2828

void handle_request(int nfd)
{
   FILE *network = fdopen(nfd, "r");
   char *line = NULL;
   size_t size;
   ssize_t num;

   if (network == NULL)
   {
      perror("fdopen");
      close(nfd);
      return;
   }

   while ((num = getline(&line, &size, network)) >= 0)
   {
      printf("Message: %s", line);
      write(nfd, line, num);
   }

   free(line);
   fclose(network);
}

void run_service(int fd)
{
   while (1)
   {
      int nfd = accept_connection(fd);
      if (nfd != -1)
      {
        pid_t pid = fork();
        if(pid < 0){
            perror("Error: fork failed");
        }else if(pid == 0){
            close(fd);
            printf("Connection established\n");
            handle_request(nfd);
            printf("Connection closed\n");
            close(nfd);
        }else{
            close(nfd);
        }
         
      }
   }


}

void sigchild_handler(int signal){
    (void)signal;
    while(waitpid(-1, NULL, WNOHANG) > 0){

    }
}

int main(void){
    
    struct sigaction signal_alarm;
    signal_alarm.sa_handler = sigchild_handler;
    signal_alarm.sa_flags = 0;
    sigemptyset(&signal_alarm.sa_mask);
    if(sigaction(SIGALRM, &signal_alarm, NULL)== -1){
        perror("Error: sigaction no working");
        return 1;
    }

   int fd = create_service(PORT);

   if (fd == -1)
   {
      perror(0);
      exit(1);
   }

   printf("listening on port: %d\n", PORT);
   run_service(fd);
   
   close(fd);

   return 0;

}
