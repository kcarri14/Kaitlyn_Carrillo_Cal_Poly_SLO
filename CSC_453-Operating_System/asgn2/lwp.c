#include <stdio.h>
#include <stdint.h>
#include "lwp.h"
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <stdlib.h>
#include <string.h>


#define bytes 8000000
#define ALIGNMENT 16
#define HALF_ALIGNMENT 8
#define MAX_HASH 4096
#define START 1

//my queue list 
typedef struct Queue{
    thread head;
    thread tail;
    int length;
    
} Queue;

//queue for scheduler
static Queue rr_queue_inital = {NULL, NULL, NO_THREAD};
static Queue *rr_queue = &rr_queue_inital;

//queue for the terminated nodes
static Queue terminated_inital = {NULL, NULL, NO_THREAD};
static Queue *terminated = &terminated_inital;

//queue for the waiting node
static Queue wait_inital = {NULL, NULL, NO_THREAD};
static Queue *wait = &wait_inital;

//nodes for the all thread list
typedef struct Node{
    tid_t tid;
    thread t;
    struct Node* next;
}Node;

//creates hash table
static Node *all_thread_list[MAX_HASH] = {NO_THREAD};

//maps a thread id to an index in hash table
static size_t hashtable(tid_t tid){
    return ((size_t) tid) % MAX_HASH;
}

//round robin scheudler
void rr_admit(thread new_t){
    if(!new_t){
        return;
    }
    if (rr_queue->head == NULL){
        rr_queue->head = new_t;
        rr_queue->tail = new_t;
        //make the node loop on itself so its round robin
        new_t->sched_one = new_t;
        new_t->sched_two = new_t;
        rr_queue->length = START;
        return;
    }
    //pre-define because they change when working on them
    //if I don't it doesnt work
    thread head = rr_queue->head;
    thread tail = rr_queue->tail;

    new_t->sched_one = head;
    new_t->sched_two = tail;
    
    //this make sure its round robin and it keeps the queue
    //circular
    tail->sched_one = new_t;
    head->sched_two = new_t;

    rr_queue->tail = new_t;
    rr_queue->length++;
    
}
//removes a thread from scheduler
void rr_remove(thread new_t){
    if (!new_t || rr_queue->length == NO_THREAD){
         return;
    }
    if(rr_queue->length == START){
        //basically resets the queue
        rr_queue->head = NULL;
        rr_queue->tail = NULL;
        rr_queue->length = NO_THREAD;
    }else{
        //pre-define because they change when working on them
        //if I don't it doesnt work
        thread next = new_t->sched_one;
        thread prev = new_t->sched_two;

        if(new_t == rr_queue->head){
            rr_queue->head = next;
        }
        if(new_t == rr_queue->tail){
            rr_queue->tail = prev;
            
        }

        prev->sched_one = new_t->sched_one;
        next->sched_two = new_t->sched_two;
        rr_queue->length--;
    }
    new_t->sched_two = NULL;
    new_t->sched_one = NULL;
}
//gives the next thread in scheduler
static thread rr_next(void){
    thread next_t = rr_queue->head;
    //return NULL if no next
    if (next_t == NULL){
        return NULL;
    }
    //gets the next node
    rr_queue->head = next_t->sched_one;
    rr_queue->tail = rr_queue->head->sched_two;

    return next_t;
}

//this is simple, just return the length
static int rr_qlen(void){
    return rr_queue->length;
}

//wrapper function
void wrap(lwpfun f, void *arg){
    int val;
    val = f(arg);
    lwp_exit(val);
}

//takes out a thread from the big list of nodes
void remove_hash(tid_t tid){
    size_t index = hashtable(tid);
    Node *prev = NULL;
    Node *current = all_thread_list[index];

    while(current){
        if(current->tid == tid){
            if(prev){
                prev->next = current->next;
            }else{
                all_thread_list[index] = current->next;
            }
            free(current);
            return;
        }
        prev = current;
        current = current->next;
    }
}

//establishes the round robin scheduler
struct scheduler rr_publish = {NULL, NULL, rr_admit, 
rr_remove, rr_next, rr_qlen};
scheduler CurrentScheduler = &rr_publish;

//more global variables
static thread current = NULL;
int count = 0;


tid_t lwp_create(lwpfun function, void* argument){
    //figure out how much to space for stack
    size_t howbig = 0;
    size_t page_size = sysconf(_SC_PAGESIZE);
    struct rlimit rlim;
    int limit = getrlimit(RLIMIT_STACK, &rlim);
    if(limit == 0 && rlim.rlim_cur != RLIM_INFINITY){
        howbig = rlim.rlim_cur;
    }else{
        //aligns to the pages
        howbig = ((bytes + page_size - 1) / page_size) * page_size;
        while(howbig % ALIGNMENT != 0){
            howbig++;
        }
    }
    //allocate a stack 
    void *s = mmap(NULL,howbig,PROT_READ|PROT_WRITE,
    MAP_PRIVATE|MAP_ANONYMOUS|MAP_STACK,-1,0);
    if(s == MAP_FAILED){
        return NO_THREAD;
    }

    //context for new LWP
    thread new = malloc(sizeof *new);
    if(new == NULL){
        munmap(s, howbig);
        return NO_THREAD;
    }
    new->tid = ++count;
    new->stack = s;
    new->stacksize = howbig;
    new->status = LWP_LIVE;
    new->lib_one = NULL;
    new->lib_two = NULL;
    new ->exited = NULL;

    //initialze the stack for the swap_files
    void *tos = (char*)s + howbig;

    uintptr_t *fake_rbp = (uintptr_t*)((char*)tos - ALIGNMENT);
    if((uintptr_t)fake_rbp % ALIGNMENT == 0){
         fake_rbp = (uintptr_t *)((char *)fake_rbp - HALF_ALIGNMENT);
    }
    fake_rbp[0] = 0;
    fake_rbp[1] = (uintptr_t)wrap;

    new->state.rbp = (uintptr_t)fake_rbp;
    new->state.rsp = (uintptr_t)fake_rbp;
    //initalize rfiles
    new->state.rdi= (uintptr_t)function;
    new->state.rsi= (uintptr_t)argument;

    new->state.fxsave=FPU_INIT;

    //adds thread into the hash table so we can look it up later
    size_t index = hashtable(new->tid);
    Node *n = (Node*)malloc(sizeof(*n));
    if(!n){
        free(new);
        current = NULL;
        return NO_THREAD;
    }
    n->tid = new->tid;
    n->t = new;
    n->next = all_thread_list[index];
    all_thread_list[index] = n;

    //admits to the current scheduler
    scheduler sched = lwp_get_scheduler();
    sched->admit(new);
    return new->tid;
}

void lwp_start(void){
    //checks if current already exists so it doesn't make another one
    if (current != NULL){
        return;
    }
    //allocates a context for LWP 
    thread new_thread = malloc(sizeof *new_thread);
    if(!new_thread){
        return;
    }

    new_thread->tid = ++count;
    new_thread->stack = NULL;
    new_thread->stacksize = 0;
    new_thread->status = LWP_LIVE;
    new_thread->lib_one = NULL;
    new_thread->lib_two = NULL;
    new_thread ->exited = NULL;
    
    current = new_thread;

    size_t index = hashtable(new_thread->tid);
    Node *n = (Node*)malloc(sizeof *n);
    if (!n) {
        free(new_thread);
        current = NULL;
        return;
    }
    n->tid = new_thread->tid;
    n->t   = new_thread;
    n->next = all_thread_list[index];
    all_thread_list[index] = n;

    //admits it to the scheduler
    scheduler s = lwp_get_scheduler();
    s->admit(new_thread); 

    //yields control 
    lwp_yield();
  
}

void lwp_yield(void){
    //gets next thread and yields control to it
    scheduler s = lwp_get_scheduler();
    thread old = current;
    thread next_t = s->next();
    //if no next thread, call exit
    if(next_t == NULL){
        exit(LWPTERMSTAT(old->status));
    }
    current = next_t;
    
    swap_rfiles(&old->state, &next_t->state);
    
}

void lwp_exit(int status){
    //terminates the calling thread
    //termination status becomes the low 8 bits of a passed int
    int exit_status = MKTERMSTAT(LWP_TERM, status & 0xFF);
    current->status = exit_status;
    scheduler s = lwp_get_scheduler();
    if(s && s->remove){
        s->remove(current);
    }
    current->lib_one = NULL;
    current->lib_two = NULL;
    //if theres something waiting to be terminated
    //take it out of termianted queue and admit it to the scheduler
    thread waiter = wait->head;
    if(waiter != NULL){
        wait->head = wait->head->lib_one;
        if(wait->head){
            wait->head->lib_two = NULL;
        }else{
            wait->tail = NULL;
        }
        waiter->lib_one = NULL;
        waiter->lib_two = NULL;
        wait->length--;
        waiter->exited = current;
        s->admit(waiter);   
    }else{
        //if no one waiting, just add current to the terminated list
        if(terminated->head == NULL){
            terminated->head = current;
            terminated->tail = current;
        }else{
            terminated->tail->lib_one = current;
            current->lib_two = terminated->tail;
            terminated->tail = current;
            current->lib_one = NULL;
        }
        terminated->length++;

    }
    lwp_yield();
}

tid_t lwp_wait(int* status){
    tid_t oldest_tid;
    if(terminated->head != NULL){
        //if thread in terminated, deallocate its resources 
        //and give termination status
        thread oldest_term = terminated->head;
        terminated->head = oldest_term->lib_one;
        if(terminated->head != NULL){
            terminated->head->lib_two = NULL;
        }else{
            terminated->tail = NULL;   
        }
        terminated->length--;
        oldest_term->lib_one = NULL;
        oldest_term->lib_two = NULL;
        if(status != NULL){
            *status = oldest_term->status;
        }
        oldest_tid = oldest_term->tid;
        if(oldest_term->stack != NULL){
            munmap(oldest_term->stack, oldest_term->stacksize);
        }

        remove_hash(oldest_tid);
        free(oldest_term);
        return oldest_tid;
    }else{
        //if not add current thread to waiting queue
        //it will wait until there is a terminated thread
        scheduler s = lwp_get_scheduler();
        int length = s->qlen();
        if(length == 0){
            return NO_THREAD;
        }else{
            if (s && s->remove) {
                s->remove(current);
            }
            current->lib_one = NULL;
            current->lib_two = NULL;
            if(wait->head == NULL){
                wait->head = current;
                wait->tail = current;
            }else{
                wait->tail->lib_one = current;
                current->lib_two = wait->tail;
                wait->tail = current;
            }
            wait->length++;
            
            lwp_yield();
            thread exit_t = current->exited;
            if(exit_t == NULL){
                return NO_THREAD;
            }else{
                current->exited = NULL;
                if(status != NULL){
                    *status = exit_t->status;
                } 
                oldest_tid = exit_t->tid;
                
                if(exit_t->stack != NULL){
                    munmap(exit_t->stack, exit_t->stacksize);
                }
                remove_hash(oldest_tid);
                free(exit_t);
            }
            return oldest_tid;
        }
    }

}

//gives the tid of current thread
tid_t lwp_gettid(void){
    if(current != NULL){
        return current->tid;
    }else{
        return NO_THREAD;
    } 
}
//looks through hash table to find the thread that goes with the tid
thread tid2thread(tid_t needed_tid){
    if(needed_tid == NO_THREAD){
        return NULL;
    }
    if(needed_tid <= 0){
        return NULL;
    }
   size_t index = hashtable(needed_tid);
   if(index >= MAX_HASH){
    return NULL;
   }
   Node *n = all_thread_list[index];
   while(n){
    if(n && n->tid == needed_tid){
        return n->t;
    }else{
        n = n->next;
    }
   }
   return NULL;
}
//makes a smooth transition between schedulers
void lwp_set_scheduler(scheduler sched){
    if(sched == NULL){
        sched = &rr_publish;
    }
    if(sched == CurrentScheduler){
        return;
    }
    scheduler old_sched = CurrentScheduler;
    if(sched->init){
        sched->init();
    }
    if(old_sched){
        thread t;
        while((t = old_sched->next()) != NULL){
            old_sched->remove(t);
            sched->admit(t);
            
        }

        if(old_sched && old_sched->shutdown){
            old_sched->shutdown();
        }
    }

    
    
    CurrentScheduler = sched;
}
//gets the scheduler
scheduler lwp_get_scheduler(void){
    if(CurrentScheduler == NULL){
        return &rr_publish;
    }else{
        return CurrentScheduler;
    }
}


