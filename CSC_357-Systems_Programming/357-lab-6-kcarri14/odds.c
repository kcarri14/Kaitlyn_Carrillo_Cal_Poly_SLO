#include <stdio.h>
#include <stdlib.h>

void odd(int input){
    for(int i = 1; i <= input; i+=2){
        printf("%d\n", i);
    }
}

int main(int argc, char *argv[]){
    int N = atoi(argv[1]);
    odd(N);
}