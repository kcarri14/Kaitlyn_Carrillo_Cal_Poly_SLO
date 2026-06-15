// #include "lwp.h"
// #include "schedulers.h"
// #include <stdlib.h>
// #include <stdio.h>
// #include <string.h>
// #include <unistd.h>
// #include <stdio.h>
// #include <stdint.h>
// #include <sys/mman.h>
// #include <fcntl.h>
// #include <unistd.h>
// #include <sys/time.h>
// #include <sys/resource.h>


// #define INITIALSTACK 4096
// #define NUMTHREADS 5
// #define ITERS 1

// #define tnext sched_one
// #define tprev sched_two

// static void indentnum(void *num);


// int main(int argc, char *argv[]){
//   long i;


//   printf("Launching LWPS\n");

//   /* spawn a number of individual LWPs */
//   for(i=1;i<=NUMTHREADS;i++) {
//     lwp_create((lwpfun)indentnum,(void*)i);
//   }

//   lwp_start();                     /* returns when the last lwp exits */

//   for(i=1;i<=NUMTHREADS;i++) {
//     lwp_wait(NULL);
//   }

//   printf("Back from LWPS.\n");
//   return 0;
// }

// static void indentnum(void *num) {
//   /* print the number num num times, indented by 5*num spaces
//    * Not terribly interesting, but it is instructive.
//    */
//   long i;
//   int howfar;
//   char *name = (char *)num;

//   howfar=(long)num;              /* interpret num as an integer */
//   for(i=0;i<howfar;i++){
//     printf("%*d\n",howfar*5,howfar);
//     lwp_yield();                /* let another have a turn */
//   }
//   printf("Task finishing\n");
//   lwp_exit(i);                  /* bail when done.  This should
//                                  * be unnecessary if the stack has
//                                  * been properly prepared
//                                  */
// }

#include <stdio.h>
#include <stdlib.h>
#include "lwp.h" // Example LWP library header

// Function to be executed by the LWP
static void thread_task(void *arg) {
    char *name = (char *)arg;
    int i;
    for (i = 0; i < 3; i++) {
        printf("Task %s running, iteration %d\n", name, i);
        lwp_yield(); // Voluntarily yield control to another LWP
    }
    printf("Task %s finishing\n", name);
    lwp_exit(i); // Exit the process
}

int main() {
    long i;
    // 1. Create multiple lightweight processes
    lwp_create((lwpfun)thread_task, "A");
    lwp_create((lwpfun)thread_task, "B");
    lwp_create((lwpfun)thread_task, "C");

    printf("Starting scheduler...\n");
    // 2. Start the scheduler (runs until all threads finish)
    lwp_start(); 

    for(i=1;i<=3;i++) {
        lwp_wait(NULL);
    }

    printf("All tasks finished.\n");
    return 0;
}



