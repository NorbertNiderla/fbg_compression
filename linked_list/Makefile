.DEFAULT_GOAL := all

test: all
	./test

test_w_valgrind: all
	valgrind --leak-check=full ./test 

all:
	gcc linked_list_test.c linked_list.c -o test -Wall -Wextra -g

clean:
	rm ./test