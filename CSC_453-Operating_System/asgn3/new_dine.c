#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <semaphore.h>

//globals
#ifndef NUM_PHILOSOPHERS
#define NUM_PHILOSOPHERS 5
#endif

#ifndef DAWDLEFACTOR
#define DAWDLEFACTOR 1000
#endif

#define CHANGING 2
#define EATING 0 
#define THINKING 1

//struct for philosopher
typedef struct Philosopher{
    int id;
    char label;
    int state;
    int left_fork;
    int right_fork;
    bool has_left;
    bool has_right;
    
} Philosopher;

//semaphores and threads
sem_t forks[NUM_PHILOSOPHERS];
sem_t print_lock;
pthread_t tids[NUM_PHILOSOPHERS];
int cycles;
Philosopher *global_phils = NULL;

//function given to us
void dawdle() {
    struct timespec tv;
    int msec = (int) ((((double)random()) /RAND_MAX) * DAWDLEFACTOR);

    tv.tv_sec = 0;
    tv.tv_nsec = 1000000 * msec;
    if(-1 == nanosleep(&tv, NULL)){
        perror("nanosleep");
    }
}


void print_status(void){
    int i;
    int j;

    //for printing prettiness
    printf("| ");
    //array for the forks
    char display[NUM_PHILOSOPHERS+1];

    //cycle through philosophers to print the status
    for(j = 0; j <NUM_PHILOSOPHERS; j++){
        Philosopher *p = &global_phils[j];
            for(i = 0; i< NUM_PHILOSOPHERS; i++){
                display[i] = '-';
            }
            display[NUM_PHILOSOPHERS] = '\0';
            if(p->has_left){
                display[p->left_fork] = '0' + p->left_fork;
            }
            if(p->has_right){
                display[p->right_fork] = '0' + p->right_fork;
            }

            printf("%s ", display);

            if(p->state == EATING){
                printf("Eat   | ") ;
            }else if (p->state == THINKING){
                printf("Think | ");
            }else{
                printf("      | ");
            }
        
    }
    printf("\n");
}
void take_forks(Philosopher *p, int fork){
    //lock the fork
    sem_wait(&forks[fork]);
    //lock the print status
    sem_wait(&print_lock);
    //change the state for the forks
    if(fork == p->left_fork){
        p->has_left = true;
    }else{
        p->has_right = true;
    }
    //print the new line
    print_status();
    //unlock the print semaphore
    sem_post(&print_lock);
}

void put_forks(Philosopher *p, int fork){
    //lock the print semaphore
    sem_wait(&print_lock);
    // change the state for the forks
    if(fork == p->left_fork){
        p->has_left = false;
    }else{
        p->has_right = false;
    }
    //print the new line
    print_status();
    //unlock the print semaphore
    sem_post(&print_lock);
    //unlock the fork
    sem_post(&forks[fork]);
}

void set_state(Philosopher *p, int new_state){
    //lock the print semaphore
    sem_wait(&print_lock);
    //check if the state is the same to avoid duplicate lines
    if(p->state == new_state){
        sem_post(&print_lock);
        return;
    }
    //change the state
    p->state = new_state;
    //print the new line
    print_status();
    //unlock the print semaphore
    sem_post(&print_lock);
}


void *thread_processing(void *arg){
    int i;
    Philosopher *p = (Philosopher*)arg;
    for(i=0; i<cycles; i++){
        
        set_state(p, CHANGING);

        int first  = (p->id % 2 == 0) ? p->right_fork : p->left_fork;
        int second = (p->id % 2 == 0) ? p->left_fork  : p->right_fork;

        //take first fork
        
        take_forks(p, first);

        //take second fork
        take_forks(p, second);

        //Eating
        set_state(p, EATING);
        dawdle();

        //changing
        set_state(p, CHANGING);

        //put down first fork
        put_forks(p, first);

        //put down second fork
        put_forks(p,second);

        set_state(p, THINKING);
        dawdle();
    }
    return NULL;
}

int main(int argc, char *argv[]){
    //checks for too many or too few philosophers
    if (NUM_PHILOSOPHERS <= 2 || NUM_PHILOSOPHERS >= 62){
        printf("Cannot have this many(or few) philsophers: %d\n",
        NUM_PHILOSOPHERS);
        return 0;
    }
    int i;
    int bar_length = 11 + (NUM_PHILOSOPHERS - 2);
    char display[bar_length];
    //prints the top line
    printf("|");
    for (i=0; i<NUM_PHILOSOPHERS; i++){
        if(i == NUM_PHILOSOPHERS - 1){
            for(i = 0; i< bar_length; i++){
                display[i] = '=';
            }
            display[bar_length -1] = '|';
            display[bar_length] = '\0';  
            for(i= 0; i< NUM_PHILOSOPHERS- 1; i++){
                printf(display);
                
            }
            
            
        }else{
            for(i = 0; i< bar_length; i++){
                display[i] = '=';
            }
            display[bar_length -1] = '|';
            display[bar_length] = '\0';  
            for(i= 0; i< NUM_PHILOSOPHERS- 1; i++){
                printf(display);
            }
            printf(display);
        }
    }
    printf("\n");
    printf("|");
    Philosopher phils[NUM_PHILOSOPHERS];
    global_phils = phils;
    if (argc == 1){
        cycles = 1;
    }else{
        cycles = (int) strtol(argv[1], NULL,10);
    }
    for(i=0; i< NUM_PHILOSOPHERS; i++){
       if((sem_init(&forks[i],0, 1)) != 0){
            int fork_id = i;
            printf("Could not initialize fork %d\n", fork_id);
       }
    }
    if((sem_init(&print_lock,0, 1)) != 0){
        perror("Could not initialize print fork\n");
    }
    int buffer;
    if (NUM_PHILOSOPHERS > 13){
        buffer = 0;
    }else{
        buffer = 6 - ((NUM_PHILOSOPHERS - 1) / 2);
    }
    int space_length = buffer + (NUM_PHILOSOPHERS - 3);
    char space[space_length + 1];
    char space_even[space_length]; 
    for(i = 0; i< space_length; i++){
                space[i] = ' ';
    }
    space[space_length] = '\0';
    for(i = 0; i< space_length -1; i++){
        space_even[i] = ' ';
    }  
    space_even[space_length-1] = '\0'; 
    for (i = 0; i < NUM_PHILOSOPHERS; i++){
        Philosopher *new = &phils[i]; 
        new->id = i;
        new->label = 'A' + i;
        new->state = CHANGING;
        new->left_fork = i;
        new->right_fork = (i + 1) % NUM_PHILOSOPHERS;
        new->has_left = false;
        new->has_right = false;

        if(i == NUM_PHILOSOPHERS - 1){
            printf("%s",space);
            printf("%c", new->label);
            if(NUM_PHILOSOPHERS % 2 == 0){
                printf("%s",space_even);
            }else{
                printf("%s",space);
            }
            
            printf("|\n");
        }else{
            printf("%s",space);
            printf("%c", new->label);
            if(NUM_PHILOSOPHERS % 2 == 0){
                printf("%s",space_even);
            }else{
                printf("%s",space);
            }
            printf("|");
        }

    }
    printf("|");
    for (i=0; i<NUM_PHILOSOPHERS; i++){
        printf(display);
    }
    printf("\n");
    for (i = 0; i< NUM_PHILOSOPHERS; i++){
        int pt = pthread_create(&tids[i], NULL, thread_processing, &phils[i]);
        if(pt != 0){
            printf("thread unsuccessful");
        }
    }
    for(i=0; i<NUM_PHILOSOPHERS;i++){
        int pj = pthread_join(tids[i], NULL);
        if(pj != 0){
            printf("thread unsuccessful");
        }
    }

    for(i=0; i<NUM_PHILOSOPHERS;i++){
        sem_destroy(&forks[i]);
        
    }
    printf("\n");
    sem_destroy(&print_lock);

}

