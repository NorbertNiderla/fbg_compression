#include "data_storage.h"
#include <stdlib.h>
#include <stdio.h>

#define SHORT_SINUS_DATA_FILE_DIR "/home/norbert/fbg_compression/data_storage/data/short_sinus_data.txt"

int data_storage_get_data32_batch(uint32_t* mem, size_t* len){
    if(mem == NULL || len == NULL){
        return 1;
    }

    FILE* fp = fopen(SHORT_SINUS_DATA_FILE_DIR, "r");
    size_t max_n = *len;

    if(fp == NULL){
        *len = 0;
        return 1;
    }

    unsigned i = 0;
    while(fscanf(fp, "%d\n", &mem[i]) == 1 && ++i < max_n);
    *len = i;

    fclose(fp);
    return 0;
}

// int data_storage_get_data16_batch(uint16_t* mem, size_t* len){ 
//     return 1;
// }

// int data_storage_get_data8_batch(uint8_t* mem, size_t* len){
//     return 1;
// }