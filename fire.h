#ifndef FIRE_H
#define FIRE_H

#include <stdint.h>
#include <stdlib.h>

typedef struct Fire{
    int learn_shift;
    unsigned bitwidth;
    int accumulator;
    int delta;
    uint32_t last_sample;
}Fire_t;

/**
 * @brief 
 * 
 * @param state 
 * @param learn_shift 
 * @param bitwidth 
 * @param init_value 
 * @retval 0 on success
 * @retval 1 on error
 */
int fire_init(Fire_t* state, int learn_shift, unsigned bitwidth, uint32_t init_value);

int fire_predict(Fire_t* state, uint32_t* sample);

#endif //FIRE_H