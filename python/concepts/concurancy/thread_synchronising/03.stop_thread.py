# from threading import Thread, Event
# from time import sleep, perf_counter

# def task(event:Event)->None:
#     for i in range(10):
#         print(f'running task {i+1}')
#         sleep(1)
#         if event.is_set():
#             print('the thread was stopped prematurely')
#             break
#         else:
#             print('the thread is stopped maturely')


# def main()->None:
#     event = Event()
#     thread = Thread(target=task, args=(event,))

#     thread.start()
#     sleep(3)
#     event.set()

# if __name__ == "__main__":
#     start_time = perf_counter()
#     main()
#     end_time = perf_counter()
#     print(f'Time taken: {end_time - start_time} seconds')



# ------------------------------------------------------------
from threading import Thread, Event
from time import sleep,perf_counter

class Worker(Thread):
    def __init__(self, event:Event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event

    def run(self)->None:
        for i in range(10):
            print(f'running task {i+1}')
            sleep(1)
            if self.event.is_set():
                print('the thread was stopped prematurely')
                break
            else:
                print('the thread is stopped maturely')

def main()->None:
    event = Event()
    thread = Worker(event)
    thread.start()
    sleep(3)
    event.set()

if __name__ == "__main__":
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    print(f'Time taken: {end_time - start_time} seconds')