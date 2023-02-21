#ifndef BITSTREAM_H
#define BITSTREAM_H

#include <stdint.h>
#include "linked_list.h"

typedef struct Bitstream {
    LinkedList_t* list;
    uint64_t write_buffer;
    unsigned bits_in_write_buffer;
    uint64_t read_buffer;
    unsigned bits_in_read_buffer;
} Bitstream_t;

Bitstream_t* bitstream_create(void);
void bitstream_destroy(Bitstream_t* const stream);
void bitstream_write(Bitstream_t* const stream, uint32_t value, uint32_t bits);
void bitstream_end_write(Bitstream_t* const stream);
uint32_t bitstream_read(Bitstream_t* const stream, unsigned bits);

#endif //BITSTREAM_H