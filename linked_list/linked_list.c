#include "linked_list.h"
#include <stdlib.h>

LinkedList_t* linked_list_create(void){
    LinkedList_t* this = (LinkedList_t*)malloc(sizeof(LinkedList_t));
    this->start = NULL;
    this->end = NULL;
    this->size = 0;
    return this;
}

void linked_list_destroy(LinkedList_t* const list){
    if(list == NULL){
        return;
    }

    if(list->size != 0){
        Node_t* next = list->start;
        do{
            Node_t* temp = next->next;
            free(next);
            next = temp;
        }while(next != NULL);
    }

    free(list);
}

void linked_list_append(LinkedList_t* const list, void* ptr){
    if(list == NULL){
        return;
    } else if(ptr == NULL){
        return;
    }

    Node_t* new_node = (Node_t*)malloc(sizeof(Node_t));
    new_node->next = NULL;
    new_node->ptr = ptr;
    if(list->size == 0){
        list->start = new_node;
        list->end = new_node;
    } else {
        list->end->next = new_node;
        list->end = new_node;
    }   
    list->size++;
}

void* linked_list_pop(LinkedList_t* const list){
    if(list == NULL){
        return NULL;
    }

    if(list->size == 0){
        return NULL;
    }

    Node_t* node_to_pop = list->start;
    list->start = node_to_pop->next;
    list->size--;
    if(list->size == 0){
        list->end = NULL;
    }
    void* val = node_to_pop->ptr;
    free(node_to_pop);
    return val;
}