#ifndef LINKED_LIST_H
#define LINKED_LIST_H

typedef struct Node {
    struct Node* next;
    void* ptr;
}Node_t;

typedef struct LinkedList{
    Node_t* start;
    Node_t* end;
    unsigned size;
}LinkedList_t;

LinkedList_t* linked_list_create(void);
void linked_list_destroy(LinkedList_t* const list);
void linked_list_append(LinkedList_t* const list, void* ptr);
void* linked_list_pop(LinkedList_t* const list);

#endif //LINKED_LIST_H