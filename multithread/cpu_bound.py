# This is a CPU-intensive script, which will perform bad when
# using multithreading.

import threading
from queue import Queue
import time

list_lock = threading.Lock()

def find_rand(num):
    sum_of_primes = 0

    ix = 2

    while ix <= num:
        if is_prime(ix):
            sum_of_primes += ix
        ix += 1

    sum_primes_list.append(sum_of_primes)

def is_prime(num):
    if num <= 1:
        return False
    elif num <= 3:
        return True
    elif num%2 == 0 or num%3 == 0:
        return False
    i = 5
    while i*i <= num:
        if num%i == 0 or num%(i+2) == 0:
            return False
        i += 6
    return True

def process_queue():
    while True:
        rand_num = min_nums.get()
        find_rand(rand_num)
        min_nums.task_done()

min_nums = Queue()

rand_list = [1000000, 2000000, 3000000]
sum_primes_list = list()

for i in range(4):
    t = threading.Thread(target=process_queue)
    t.daemon = True
    t.start()

start = time.time()

for rand_num in rand_list:
    min_nums.put(rand_num)

min_nums.join()

end_time = time.time()

sum_primes_list.sort()
print(sum_primes_list)

print("Execution time = {0:.5f}".format(end_time - start))
