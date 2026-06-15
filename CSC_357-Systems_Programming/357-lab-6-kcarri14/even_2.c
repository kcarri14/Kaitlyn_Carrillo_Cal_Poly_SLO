#include <stdio.h>
#include <stdlib.h>

void even(int input){
    for(int i = 2; i <= input; i+=2){
        printf("\t%d\n", i);
    }
}

int main(int argc, char *argv[]){
    even(30);
}
