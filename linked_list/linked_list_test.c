#include <assert.h>
#include <stdlib.h>
#include <stdint.h>
#include "linked_list.h"


int main(void){

    LinkedList_t* list = linked_list_create();
    
    assert(linked_list_pop(list) == NULL);

    uint32_t val = 1;
    uint16_t another_val = 2;
    uint8_t yet_another_val = 3;
    linked_list_append(list, (void*)&val);
    linked_list_append(list, (void*)&another_val);
    linked_list_append(list, (void*)&yet_another_val);
    
    assert(*((uint32_t*)linked_list_pop(list)) == 1);
    assert(*((uint16_t*)linked_list_pop(list)) == 2);
    assert(*((uint8_t*)linked_list_pop(list)) == 3);
    assert(linked_list_pop(list) == NULL);

    linked_list_append(list, (void*)&val);
    linked_list_append(list, (void*)&another_val);
    linked_list_append(list, (void*)&yet_another_val);
    
    linked_list_destroy(list);

    return 0;
}