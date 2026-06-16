#include <stdio.h>
#include "checkit.h"
#include "array_list.h"

void test_resize(){
    array_list *list = array_list_new();
    array_list_add_to_end(list, "Hello");
    array_list_add_to_end(list, "My");
    array_list_add_to_end(list, "Name");
    array_list_add_to_end(list, "will");
    array_list_add_to_end(list, "be");
    array_list_add_to_end(list, "Kaitlyn");
    array_list_add_to_end(list, "Namvar");

    checkit_string(list->items[0], "Hello");
    checkit_string(list->items[1], "My");
    checkit_string(list->items[2], "Name");
    checkit_string(list->items[3], "will");
    checkit_string(list->items[4], "be");
    checkit_string(list->items[5], "Kaitlyn");
    checkit_string(list->items[6], "Namvar");

    checkit_int(list->length, 7);

    for (int i =0; i < list -> length; i++){
        printf("Item %d: %s\n", i, list->items[i]);
    }
    array_list_free(list);

}
int main(void){
    test_resize();
    return 0;
}


