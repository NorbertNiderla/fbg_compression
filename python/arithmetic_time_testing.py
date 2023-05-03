from random import randint
from time import time
from Common.algorithms import algorithm_arithmetic

data = [randint(0, 16000) for _ in range(20000)]

counts = [0] * (max(data) + 1)
for x in data:
    counts[x] += 1

start_time = time()
algorithm_arithmetic(data)
end_time = time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time}")
