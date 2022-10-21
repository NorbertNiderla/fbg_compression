INCLUDES = ./../linked_list/
FLAGS = -Wall -Wextra -g
SRC_FILES = ./../linked_list/linked_list.c bitstream.c bitstream_test.c
.DEFAULT_GOAL=all

test: all
	./test

test_w_valgrind: all
	valgrind --leak-check=full ./test

all:
	gcc $(SRC_FILES) -I $(INCLUDES) -o test $(FLAGS)

clean:
	rm ./test