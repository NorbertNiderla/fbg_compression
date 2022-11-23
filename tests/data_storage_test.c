#include "data_storage.h"
#include <assert.h>
#include <stdio.h>
#include <math.h>

int main(void){
    // uint32_t samples[10];
    // uint32_t real_samples[10] = {100,110,120,130,139,148,156,164,172,178};

    // size_t len = 10;
    // int ret = data_storage_get_data32_batch(samples, &len);

    // assert(data_storage_get_data32_batch(NULL, NULL) == 1);

    // assert(len == 10);
    // assert(ret == 0);
    // for(int i = 0; i<10; i++){
    //     assert(samples[i] == real_samples[i]);
    // }

    uint16_t* data;
    size_t data_mem_size;
    int ret = data_storage_get_data16_batch(&data, &data_mem_size);
    assert(ret == 0);
    int data_len = data_mem_size /2;

    for(int i = 1; i < data_len; i++){
        int abs_diff = abs((int)data[i] - (int)data[i-1]);
        if(abs_diff > 200){
            printf("%d: ", i);
            for(int x = abs_diff; x > 0; x -= 10){
                printf("*");
            }
            printf("\n");
        }
        
    }

    return 0;
}