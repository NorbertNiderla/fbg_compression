#include "bitstream.h"
#include "linked_list.h"
#include <stdlib.h>

Bitstream_t* bitstream_create(void){
    Bitstream_t* stream = (Bitstream_t*)malloc(sizeof(Bitstream_t));
    stream->list = linked_list_create();
    stream->write_buffer = 0;
    stream->bits_in_write_buffer = 0;
    stream->read_buffer = 0;
    stream->bits_in_read_buffer = 0;
    return stream;
}

void bitstream_destroy(Bitstream_t* const stream){
    if(stream == NULL){
        return;
    }

    linked_list_destroy(stream->list);
    free(stream);
}

void bitstream_write(Bitstream_t* const stream, uint32_t value, uint32_t bits){
    if(stream == NULL || bits == 0 || bits > 32){
        return;
    }

    value &= ((1 << bits) - 1);
    unsigned free_bits = 64 - stream->bits_in_write_buffer;
    uint64_t value64 = value;

    if(free_bits >= bits){
        stream->write_buffer |= (value64 << (free_bits - bits));
        stream->bits_in_write_buffer += bits;
        bits -= bits;
    } else {
        stream->write_buffer |= (value64 >> (bits - free_bits));
        stream->bits_in_write_buffer += free_bits;
        bits -= free_bits; 
    }

    if(stream->bits_in_write_buffer == 64){
        uint64_t* new_value = malloc(sizeof(uint64_t));
        *new_value = stream->write_buffer;
        linked_list_append(stream->list, (void*)new_value);
        stream->write_buffer = 0;
        stream->bits_in_write_buffer = 0;
    }

    if(bits != 0){
        bitstream_write(stream, value64, bits);
    }
}

void bitstream_end_write(Bitstream_t* const stream){
    if(stream == NULL){
        return;
    }

    uint64_t* new_value = (uint64_t*)malloc(sizeof(uint64_t));
    *new_value = stream->write_buffer;
    linked_list_append(stream->list, (void*)new_value);
    stream->write_buffer = 0;
    stream->bits_in_write_buffer = 0;
}

uint32_t bitstream_read(Bitstream_t* const stream, unsigned bits){
    if(stream == NULL || bits == 0 || bits > 32){
        return 0;
    }
    uint64_t value64 = 0;

    if(stream->bits_in_read_buffer == 0){
        void* val_ptr = linked_list_pop(stream->list);
        stream->read_buffer = val_ptr != NULL ? *((uint64_t*)val_ptr) : 0;
        free(val_ptr);
        stream->bits_in_read_buffer = 64;
    }

    if(stream->bits_in_read_buffer >= bits){
        value64 = (stream->read_buffer >> (stream->bits_in_read_buffer - bits));
        value64 &= ((1 << bits) - 1);
        stream->bits_in_read_buffer -= bits;
    } else {
        value64 = stream->read_buffer & ((1 << stream->bits_in_read_buffer) - 1);
        bits -= stream->bits_in_read_buffer;
        stream->bits_in_read_buffer = 0;
        uint32_t value32 = bitstream_read(stream, bits);
        value64 <<= bits;
        value64 |= value32;
    }

    return (uint32_t)value64;
}