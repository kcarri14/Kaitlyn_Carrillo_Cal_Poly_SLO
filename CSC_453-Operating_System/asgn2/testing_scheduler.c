#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "lwp.h"
#include <sys/mman.h>
#include <fcntl.h>

#define next sched_one
#define prev sched_two

typedef struct Queue{
    thread head;
    thread tail;
    int length;
} Queue;

static Queue rr_queue_inital = {NULL, NULL, 0};
static Queue *rr_queue = &rr_queue_inital;

void rr_admit(thread new_t){
    new_t->sched_two = NULL;
    new_t->sched_one = NULL;
    if (rr_queue->head == NULL){
        rr_queue->head = new_t;
        rr_queue->tail = new_t;
        rr_queue->length++;
    }else{
        rr_queue->tail->sched_one = new_t;
        new_t->sched_two = rr_queue->tail;
        rr_queue->tail = new_t;
        rr_queue->length++;
    }
}

void rr_remove(thread new_t){
    new_t->sched_two = NULL;
    new_t->sched_one = NULL;
    if (rr_queue->head == new_t && rr_queue->tail == new_t){
        rr_queue->head = NULL;
        rr_queue->tail = NULL;
        rr_queue->length--;
    }else if (rr_queue->tail == new_t){
        new_t->sched_two->sched_one = NULL;
        rr_queue->tail = new_t->sched_two;
        rr_queue->length--;
    }  
    else{
        new_t->sched_two->sched_one = new_t->sched_one;
        new_t->sched_one->sched_two = new_t->sched_two;
        rr_queue->length--;
    }
}

static thread rr_next(void){
    thread next_t = rr_queue->head;
    if (next_t == NULL){
        return NULL;
    }
    rr_queue->head = next_t->sched_one;
    if(rr_queue->head){
        rr_queue->head->sched_two = NULL;
    }else{
        rr_queue->tail = NULL;
    }
    next_t->sched_one = NULL;
    next_t->sched_two = NULL;
    rr_queue->length--;

    return next_t;
}

static int rr_qlen(void){
    return rr_queue->length;
}


struct scheduler rr_publish = {NULL, NULL, rr_admit, rr_remove, rr_next, rr_qlen};
scheduler RoundRobin = &rr_publish;

int main(void){
    thread A = malloc(sizeof *A);
    thread B = malloc(sizeof *B);
    thread C = malloc(sizeof *C);
    if (!A || !B || !C) { perror("malloc"); exit(1); }
    memset(A, 0, sizeof *A);
    memset(B, 0, sizeof *B);
    memset(C, 0, sizeof *C);
    A->tid = 1;
    B->tid = 2;
    C->tid = 3;


    rr_admit(A);
    rr_admit(B);
    rr_admit(C);

    printf("qlen = %d\n", rr_qlen());
    thread t1;
    t1 = rr_next();
    printf("%d", t1->tid);
    rr_admit(t1);
    thread t;
    while ((t = rr_next()) != NULL) {
        printf("popped node %d\n", t->tid);
        free(t); 
    }
    printf("qlen after pops = %d\n", rr_qlen());
    return 0;
}