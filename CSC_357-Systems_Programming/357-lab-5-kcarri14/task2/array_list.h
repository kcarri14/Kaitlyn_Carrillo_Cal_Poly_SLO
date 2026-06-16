#ifndef ARRAY_LIST_H
#define ARRAY_LIST_H

typedef struct{
    char **items;
    int capacity;
    int length; 
}array_list;

array_list *array_list_new();
void array_list_add_to_end(array_list *list, char *str);
void array_list_free(array_list *list);

#endif