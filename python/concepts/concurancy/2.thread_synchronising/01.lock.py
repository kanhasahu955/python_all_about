# # This is a simple example of how to use a lock to synchronize access to a shared resource.
# from threading import Thread
# from time import sleep

# counter = 0 

# def increase_counter(by:int):
#     global counter
#     local_counter = counter
#     local_counter += by

#     sleep(0.01)
#     counter = local_counter
#     print(f'Counter: {counter}')

# thread_1 = Thread(target=increase_counter, args=(100,))
# thread_2 = Thread(target=increase_counter, args=(200,))

# thread_1.start()
# thread_2.start()

# thread_1.join()
# thread_2.join()

# print(f'Counter: {counter}')


# ------------------------------------------------------------
# from threading import Thread, Lock
# from time import sleep

# counter = 0

# def increase_counter(by:int,lock:Lock):
#     global counter

#     lock.acquire()
#     local_counter = counter

#     local_counter += by
#     sleep(0.01)
#     counter = local_counter
#     print(f'Counter: {counter}')
#     lock.release()
#     print(f'Counter: {counter}')

# lock = Lock()
# thread_1 = Thread(target=increase_counter, args=(100,lock))
# thread_2 = Thread(target=increase_counter, args=(200,lock))

# thread_1.start()
# thread_2.start()

# thread_1.join()
# thread_2.join()

# print(f'The final counter is {counter}')


# ------------------------------------------------------------
# from threading import Thread, Lock
# from time import sleep

# counter = 0

# def increase_counter(by:int, lock:Lock):
#     global counter
    
#     with lock:
#         local_counter = counter
#         local_counter += by

#         sleep(0.01)
#         counter = local_counter
#         print(f'Counter: {counter}')

# lock = Lock()
# thread_1 = Thread(target=increase_counter, args=(100,lock))
# thread_2 = Thread(target=increase_counter, args=(200,lock))

# thread_1.start()
# thread_2.start()

# thread_1.join()
# thread_2.join()

# print(f'final counter: {counter}')



# ------------------------------------------------------------
from threading import Thread, Lock
from time import sleep,perf_counter

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = Lock()

    def increase(self, by:int):
        with self.lock:
            current_value = self.value
            current_value += by
            sleep(0.01)
            self.value = current_value
            print(f'Counter: {self.value}')

def main():
    counter = Counter()

    thread_1 = Thread(target=counter.increase, args=(100,))
    thread_2 = Thread(target=counter.increase, args=(200,))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    print(f'Counter: {counter.value}')

if __name__ == "__main__":
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    print(f'Time taken: {end_time - start_time} seconds')
