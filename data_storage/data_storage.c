#include "data_storage.h"
#include <stdlib.h>
#include <stdio.h>

#define SHORT_SINUS_DATA_FILE_DIR "/home/norbert/fbg_compression/data_storage/data/short_sinus_data.txt"
#define BM_DATA_FILE_DIR    "/home/norbert/fbg_compression/data_storage/data/bm_data_bin/0"
#define CREATE_BM_DATA_FILE_DIR "/home/norbert/fbg_compression/data_storage/data/bm_data_bin/%d"

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

int data_storage_get_data16_batch(uint16_t** mem, size_t* len, unsigned file_number){ 
    if(mem == NULL || len == NULL){
        return 1;
    }

    char filedir[128];
    sprintf(filedir, CREATE_BM_DATA_FILE_DIR, file_number);
    FILE* fp = fopen(BM_DATA_FILE_DIR, "r");

    if(fp == NULL){
        return 1;
    }

    fseek(fp, 0, SEEK_END); // seek to end of file
    size_t size = ftell(fp); // get current file pointer
    fseek(fp, 0, SEEK_SET); // seek back to beginning of file

    uint16_t* data = (uint16_t*)malloc(size);
    fread(data, 1, size, fp);
    fclose(fp);

    *mem = data;
    *len = size;
    return 0;
}

// int data_storage_get_data8_batch(uint8_t* mem, size_t* len){
//     return 1;
// }