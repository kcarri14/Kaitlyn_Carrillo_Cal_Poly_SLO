#include "lwp.h"
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



typedef struct {
    thread head;
    thread tail;
    int length;
} AZQueue;

static AZQueue q = {NULL, NULL, 0 };

static void az_admit(thread t) {
    if (!t) return;

    /* scheduler owns sched_one/sched_two */
    t->sched_one = NULL;
    t->sched_two = NULL;

    if (!q.head) {
        q.head = q.tail = t;
    } else {
        q.tail->sched_one = t;
        t->sched_two = q.tail;
        q.tail = t;
    }
    q.length++;
}

static void az_remove(thread t) {
    if (!t || !q.head) return;

    /* detach t if it is in the queue */
    if (t->sched_two) t->sched_two->sched_one = t->sched_one;
    else             q.head = t->sched_one;

    if (t->sched_one) t->sched_one->sched_two = t->sched_two;
    else              q.tail = t->sched_two;

    if (q.length > 0) q.length--;

    t->sched_one = NULL;
    t->sched_two = NULL;
}

static thread az_next(void) {
    /* Always run the head; DO NOT rotate */
    return q.head;
}

static int az_qlen(void) {
    return q.length;
}

/* Exported symbol that matches: extern scheduler AlwaysZero; */
static struct scheduler az_sched = {
    .init = NULL,
    .shutdown = NULL,
    .admit = az_admit,
    .remove = az_remove,
    .next = az_next,
    .qlen = az_qlen
};

scheduler AlwaysZero = &az_sched;
