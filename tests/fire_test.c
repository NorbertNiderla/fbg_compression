#include "./../fire.h"
#include <stdio.h>
#include <string.h>

#define NUMBER_OF_SAMPLES   (20)

int main(void){

    Fire_t tx_predictor, rx_predictor;
    fire_init(&tx_predictor, -1, 8, 0);
    fire_init(&rx_predictor, -1, 8, 0);

    uint32_t data[NUMBER_OF_SAMPLES];
    uint32_t predicted_data[NUMBER_OF_SAMPLES];
    for(int i = 0; i < NUMBER_OF_SAMPLES; i++){
        data[i] = i;
        predicted_data[i] = i;
    }

    for(int i = 0; i < NUMBER_OF_SAMPLES; i++){
        fire_predict(&tx_predictor, &predicted_data[i]);
    }

    for(int i = 0; i < NUMBER_OF_SAMPLES; i++){
        printf("%d ", data[i]);
    }
    printf("\n");

    for(int i = 0; i < NUMBER_OF_SAMPLES; i++){
        printf("%d ", predicted_data[i]);
    }
    printf("\n");

    return 0;
}