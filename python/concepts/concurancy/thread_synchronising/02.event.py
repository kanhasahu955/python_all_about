from threading import Thread, Event
from time import sleep,perf_counter

def task(event:Event, id:int):
    print(f'Task {id} started')
    event.wait()

    print(f'received signal , the thread {id} is completed')


def main():
    event = Event()
    t1 = Thread(target=task, args=(event, 1))
    t2 = Thread(target=task, args=(event, 2))

    t1.start()
    t2.start()

    print('blocking the main thread for 3 seconds...')
    sleep(3)
    event.set()

if __name__ == "__main__":
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    print(f'Time taken: {end_time - start_time} seconds')