#include <stdio.h>
#include <unistd.h>
#include <stdint.h>
#include <errno.h>
#include <string.h>

//so i dont get warnings because I am compiling with c and these
//arent C
void* sbrk();
void *getenv();
void *pp();

//globals
#define CHUNK 64000
#define ALIGNMENT 16
static int initialized = 0;

//linked-list(ish) structure
typedef struct Header {
    size_t size;
    int is_free;
    struct Header *next;
    //this pointer is to the "data" section after the header
    void* data;
} Header;

static Header *memory_head = NULL;
static Header *memory_tail = NULL;

//aligns the headers to be divisible by ALIGNMENT
static void *pointer_aligner(uintptr_t ptr){
    while(ptr % ALIGNMENT != 0){
        ptr++;
    }
    return (void*)ptr;
}

//only initiates sbrk once for malloc
static void initiate_sbrk(void){
    if(initialized){
        return;
    }
    initialized = 1;
    //first sbrk
    void *current_break = pointer_aligner((uintptr_t)sbrk(CHUNK));
    if(current_break == (void*)-1){
        errno = ENOMEM;
        perror("sbrk failed before any initalization");
        initialized = 0;
        return;
    }
    
    //sets memory pointers on head and tail
    memory_head = (Header*)current_break;
    memory_head->size = CHUNK - sizeof(Header);
    memory_head->is_free = 1;
    memory_head->next = NULL;
    memory_head->data = pointer_aligner(((uintptr_t)memory_head + 
    sizeof(Header)));
    memory_tail = memory_head;
}

//if needed, extends heap for more memory
static Header* extend_heap(size_t needed){
    size_t required_mem;
    size_t total_needed = sizeof(Header) + needed;

    //checking if user needs more than just another CHUNK
    if (total_needed > CHUNK){
        required_mem = total_needed;
    }else{
        required_mem = CHUNK;
    }

    void *extended_break = pointer_aligner((uintptr_t)sbrk(required_mem));
    if(extended_break == (void*)-1){
        errno = ENOMEM;
        perror("sbrk failed before extending heap");
        return NULL;
    }

    //add a node onto the start of the new breakpoint
    Header *h = (Header*)extended_break;
    h->size = required_mem - sizeof(Header);
    h->is_free = 1;
    h->next = NULL;
    h->data = pointer_aligner(((uintptr_t)h + sizeof(Header)));
    //make it the memeory tail
    memory_tail->next = h;
    memory_tail = h;
    return h;

}

//aligns the size to be divisible by ALIGNMENT
static size_t aligner(size_t size){
    while(size % ALIGNMENT != 0){
        size++;
    }
    return size;
}

//this gets the new next pointer for the current 
//and sets all the definitions
static void new_next_pointer(Header *current, size_t size){
    current->data = pointer_aligner(((uintptr_t)current + sizeof(Header)));
    Header *next = (void*)(current->data + size);
    next->size = current->size - size- sizeof(Header);
    next->is_free = 1;
    next->next = current->next;
    next->data = pointer_aligner(((uintptr_t)next + sizeof(Header)));

    current->size = size;
    current->next = next;
    

    if(memory_tail == current){
        memory_tail = next;
    }
}


void *malloc(size_t size){
    if (size == 0){
        return NULL;
    }
    initiate_sbrk();

    //does the alignment
    size = aligner(size);

    //searches linked list
    for (Header *current = memory_head; current; current = current->next){
        //checks to make sure block is free and big enough
        if(current->is_free && current->size >= size){
            if((current->size - size) >= sizeof(Header) + ALIGNMENT){
                new_next_pointer(current, size);
            }
            current->is_free = 0;
            if(getenv("DEBUG_MALLOC")){
                pp(stderr, "MALLOC: malloc(%d) => (ptr=%p, size= %d)\n", 
                size, current->data, current->size);
            }
            return current->data; 
        }
    }
    //no free blocks so need more memory from sbrk
    Header *newmemory = extend_heap(size);
    if(!newmemory){
        return NULL;        
    }
    if((newmemory->size - size) >= sizeof(Header) + ALIGNMENT){
        new_next_pointer(newmemory, size);
    }
    newmemory->is_free = 0;
    
    if(getenv("DEBUG_MALLOC")){
        pp(stderr, "MALLOC: malloc(%d) => (ptr=%p, size= %d)\n", 
        size, newmemory->data, newmemory->size);
    }
    return newmemory->data; 

}

void *calloc(size_t nmemb, size_t size){
    //returns NULL
    if(nmemb == 0 || size == 0){
        return malloc(0);
    }
    size_t total = nmemb * size;
    if (nmemb != 0 && total / nmemb != size){
        perror("Integer Overflow error");
        return NULL;
    }
    void *p = malloc(total);
    if (!p){
        return NULL;
    }
    //set everything to 0
    memset(p, 0, total);

    if(getenv("DEBUG_MALLOC")){
        pp(stderr, "MALLOC: calloc(%d,%d) => (ptr=%p, size= %d)\n", 
        size, nmemb, p, size);
    }

    return p;
}

static Header *find_ptr(void *ptr){
    if(!ptr){
        return NULL;
    }
    char *p = (char*)ptr;
    //goes through the linked list until it finds the address
    //of the start of the header to return to free or realloc
    for (Header *current = memory_head; current; current = current->next){
        char *mem_start = (char*)current->data;
        char *mem_end = mem_start + current->size;

        if(p >= mem_start && p < mem_end){
            if(current->is_free){
                return NULL;
            }
                return current;
        
        }
    }
    return NULL;
}

static void merge_all(void){
    //goes through the whole linked list and finds if there are adjacent 
    //free memory blocks
    Header *current = memory_head;
    while(current && current->next){
        Header *next = current->next;
        if(current->is_free && next->is_free && 
        (char*)current->data + current->size == (char*)next){
            current->size += sizeof(Header) + next->size;
            current->next = next->next;
            if(memory_tail == next){
                memory_tail = current;
            }
        }else{
            current = current->next;
        }
    }
}


void free(void *ptr){
    if (!ptr){
        return;
    }
    //if pointer is not at the header
    Header *h = find_ptr(ptr);
    
    if (!h){
        return;
    }
    //frees the space
    h->is_free = 1;
    if(getenv("DEBUG_MALLOC")){
        pp(stderr, "MALLOC: free(%p)\n", h);
    }
    //merges the free spaces together
    merge_all();
    
}
void *realloc(void *ptr, size_t size){
    if(ptr == NULL){
        return malloc(size);
    }
    if (size == 0){
        free(ptr);
        return NULL;
    }
    Header *start_ptr = find_ptr(ptr);
    if(!start_ptr){
        return NULL;
    }
    size_t old_size = start_ptr->size;
    
    size = aligner(size);
    //shrinking
    //if the new size is smaller than old size
    //shrink the memory block to the new size
    
    if (size <= old_size){
        size_t leftover = old_size - size;
       //split off and free unused memory 
       if(leftover >= sizeof(Header) + ALIGNMENT){
            new_next_pointer(start_ptr, size);
       }
       //merge all free spaces again
        merge_all();    
        return start_ptr->data;  

    }
    //expansion
    Header *n = start_ptr->next;
    //checks if neighbor is free
    if(n && n->is_free){
        //merges the blocks together
        if((n->size + old_size + sizeof(Header)) >= size){
            start_ptr->size = old_size + n->size + sizeof(Header);
            start_ptr->next = n->next;
            if(memory_tail == n){
                memory_tail = start_ptr;
            }
        }
        //if there's enough room to split it into another block of memory
        //this will spilt it
        size_t leftover = start_ptr->size - size;
        if(leftover >= sizeof(Header) + ALIGNMENT){
            new_next_pointer(start_ptr, size);
       }
        
        if(getenv("DEBUG_MALLOC")){
        pp(stderr, "MALLOC: realloc(%p, %d) => (ptr=%p, size= %d)\n", 
            start_ptr, size, start_ptr, start_ptr->size);
        }

        return start_ptr->data; 
        }   
    //if the realloc needs to copy, because it can't expand in place
    void *newmem = malloc(size);
    if(!newmem){
        return NULL;
    }
    //copies the memory over
    memcpy(newmem, start_ptr->data, start_ptr->size);
    free(start_ptr);
    return (void*)newmem;

}
