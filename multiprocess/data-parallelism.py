from multiprocessing import Pool
import time

def square(x): # This is executed in a process
    return x*x

if __name__ == '__main__':
    numbers_to_square = range(10000)
    start_time = time.time()
    with Pool(4) as p: # Number of processes
        results = p.map(square, numbers_to_square)
        print(results)
    print("Time taken = {0:.5f}".format(time.time() - start_time))
