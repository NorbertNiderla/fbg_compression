#include "fire.h"
#include <stdint.h>

static uint32_t predict(Fire_t* state, uint32_t sample){
    uint32_t alpha = state->learn_shift > 0 ? 
        state->accumulator >> state->learn_shift :
        state->accumulator << -state->learn_shift;
    
    if(state->delta >= 0){
        return sample + ((alpha * state->delta) >> state->bitwidth);
    } else {
        return sample - ((-alpha * state->delta) >> state->bitwidth);
    }
}

static void train(Fire_t* state, uint32_t sample, uint32_t next_sample,
    int32_t error){

    state->accumulator += ((error >= 0) ? state->delta : -state->delta);
    if(state->accumulator < 0){
        state->accumulator = 0;
    }

    state->delta = next_sample - sample;
}

int fire_init(Fire_t* state, int learn_shift, unsigned bitwidth, uint32_t init_value){
    if(state == NULL){
        return 1;
    }

    if(bitwidth != 8 && bitwidth != 16 && bitwidth != 32){
        return 1;
    }

    state->accumulator = 0;
    state->bitwidth = bitwidth;
    state->learn_shift = learn_shift;
    state->delta = 0;
    state->last_sample = init_value;
    return 0;
}

int fire_predict(Fire_t* state, uint32_t* sample){
    if(state == NULL || sample == NULL){
        return 1;
    }

    uint32_t new_sample = *sample;
    uint32_t temp = predict(state, state->last_sample);
    train(state, state->last_sample, new_sample, (int32_t)temp - (int32_t)new_sample);
    state->last_sample = new_sample;
    *sample = temp;
    return 0;
}