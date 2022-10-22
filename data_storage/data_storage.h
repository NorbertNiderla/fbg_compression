#ifndef DATA_STORAGE_H
#define DATA_STORAGE_H

#include <stdlib.h>
#include <stdint.h>

/**
 * @brief Writes data from data storage into mem buffer.
 * 
 * @param mem 
 * @param len Indicates max length of mem buffer, final data length will be written into len.
 * @retval 0 on success
 * @retval 1 on error
 */
int data_storage_get_data32_batch(uint32_t* mem, size_t* len);
int data_storage_get_data16_batch(uint16_t* mem, size_t* len);
int data_storage_get_data8_batch(uint8_t* mem, size_t* len);



#endif //DATA_STORAGE_H