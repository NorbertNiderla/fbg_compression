#include "data_storage.h"
#include <assert.h>

int main(void){
    uint32_t samples[10];
    uint32_t real_samples[10] = {100,110,120,130,139,148,156,164,172,178};

    size_t len = 10;
    int ret = data_storage_get_data32_batch(samples, &len);

    assert(data_storage_get_data32_batch(NULL, NULL) == 1);

    assert(len == 10);
    assert(ret == 0);
    for(int i = 0; i<10; i++){
        assert(samples[i] == real_samples[i]);
    }

    return 0;
}