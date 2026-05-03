from threading import Thread
from queue import Queue, Empty
from time import sleep, perf_counter

def producer(queue:Queue):
    for i in range(1,6):
        print(f'inserting item {i} into the queuq')
        sleep(1)
        queue.put(i)

def consumer(queue:Queue):
    while True:
        try:
            item = queue.get()
        except Empty:
            continue
        else:
            print(f'processing item {item}')
            sleep(2)
            queue.task_done()

def main():
    queqe = Queue()
    producer_thread = Thread(target=producer, args=(queqe,),daemon=True)
    producer_thread.start()
    consumer_thread = Thread(target=consumer, args=(queqe,),daemon=True)
    consumer_thread.start()

    producer_thread.join()
    queqe.join()


if __name__ == "__main__":
    main()

