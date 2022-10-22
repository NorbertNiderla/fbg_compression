#include "bitstream.h"
#include <assert.h>
#include <stdio.h>

int main(void){
    Bitstream_t* bitstream = bitstream_create();

    for(int i = 10; i < 20; i++){
        bitstream_write(bitstream, i << 5, i);
    }

    bitstream_end_write(bitstream);

    for(int i = 10; i < 20; i++){
        uint32_t val = bitstream_read(bitstream, i);
        // assert((int)val == ((i * 3) & ((1-i)-1)));
        assert((int)val == (i << 5));
    }

    assert(bitstream_read(bitstream, 10) == 0);
    
    bitstream_destroy(bitstream);
    return 0;
}