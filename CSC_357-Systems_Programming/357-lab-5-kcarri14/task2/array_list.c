#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "array_list.h"

#define inital_cap 4

array_list *array_list_new(){
    array_list *list = malloc(sizeof(array_list));
    list -> capacity = inital_cap;
    list -> length = 0;
    list -> items = malloc(list-> capacity * sizeof(char *));
    return list;
}

void array_list_add_to_end(array_list *list, char *str){
    if(list -> length == list -> capacity){
        list-> capacity *= 2;
        list -> items = realloc(list -> items, list -> capacity * sizeof(char *));
    }
    list -> items[list-> length] = strdup(str);
    list -> length++;
}
void array_list_free(array_list *list){
    for(int i = 0; i < list-> length; i++){
        free(list-> items[i]);
    }
    free(list-> items);
    free(list);
}