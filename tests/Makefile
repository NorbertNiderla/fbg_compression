FLAGS = -Wall -Wextra -g
LIB_DIR = ./..

BITSTREAM_DIR = $(LIB_DIR)/bitstream
BITSTREAM_TEST_SRC = $(LINKED_LIST_DIR)/*.c $(BITSTREAM_DIR)/*.c bitstream_test.c
BITSTREAM_TEST_INC = -I$(LINKED_LIST_DIR) -I$(BITSTREAM_DIR)

LINKED_LIST_DIR = $(LIB_DIR)/linked_list
LINKED_LIST_TEST_SRC = $(LINKED_LIST_DIR)/*.c linked_list_test.c
LINKED_LIST_TEST_INC = -I$(LINKED_LIST_DIR)

DATA_STORAGE_DIR = $(LIB_DIR)/data_storage
DATA_STORAGE_TEST_SRC = $(DATA_STORAGE_DIR)/*.c data_storage_test.c
DATA_STORAGE_TEST_INC = -I$(DATA_STORAGE_DIR)

all: test_bitstream test_linked_list test_data_storage

test_data_storage:
	$(CC) $(DATA_STORAGE_TEST_SRC) -o test $(DATA_STORAGE_TEST_INC) $(FLAGS)
	./test

test_bitstream:
	$(CC) $(BITSTREAM_TEST_SRC) -o test $(BITSTREAM_TEST_INC) $(FLAGS)
	./test

test_linked_list:
	$(CC) $(LINKED_LIST_TEST_SRC) -o test $(LINKED_LIST_TEST_INC) $(FLAGS)
	./test

clean:
	rm ./test