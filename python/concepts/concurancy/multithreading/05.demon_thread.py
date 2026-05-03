from threading import Thread
from time import sleep

def show_timer():
    count = 0
    while True:
        print(f'Timer: {count}')
        count += 1
        sleep(1)
        print(f'Has been waiting for {count} second(s)...')

# thread = Thread(target=show_timer)
thread = Thread(target=show_timer, daemon=True)
thread.start()

answer = input('Do you want to finish the timer? (y/n): ')

    

