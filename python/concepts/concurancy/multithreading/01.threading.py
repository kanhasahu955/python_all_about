# SINGLE THREAD 

# from time import sleep, perf_counter

# def task():
#     print('task started')
#     sleep(1)
#     print('task finished')

# start_time = perf_counter()
# task()
# task()
# end_time = perf_counter()
# print(f'Time taken: {end_time - start_time} seconds')


# ------------------------------------------------------------
# MULTI THREAD
# To create a multi-threaded program, you need to use the Python threading module.

# from threading import Thread
# from time import sleep, perf_counter

# def task():
#     print('task started')
#     sleep(1)
#     print('task finished')

# start_time = perf_counter()

# # create two new threads
# thread1 = Thread(target=task)
# thread2 = Thread(target=task)

# # start the threads
# thread1.start()
# thread2.start()

# # wait for the threads to finish
# thread1.join()
# thread2.join()  

# # print the time taken
# end_time = perf_counter()
# print(f'Time taken: {end_time - start_time} seconds')

# ------------------------------------------------------------
# Passing arguments to threads
# from threading import Thread
# from time import sleep, perf_counter

# def task(name):
#     print(f'task {name} started')
#     sleep(1)
#     print(f'task {name} finished')

# start_time = perf_counter()

# threads = []
# for n in range(1,11):
#     thread = Thread(target=task, args=(n,))
#     threads.append(thread)
#     thread.start()

# for thread in threads:
#     thread.join()

# end_time = perf_counter()
# print(f'Time taken: {end_time - start_time} seconds')


# ------------------------------------------------------------
# from time import perf_counter


# def replace(filename, substr, new_substr):
#     print(f'Processing the file {filename}')
#     # get the contents of the file
#     with open(filename, 'r') as f:
#         content = f.read()

#     # replace the substr by new_substr
#     content = content.replace(substr, new_substr)

#     # write data into the file
#     with open(filename, 'w') as f:
#         f.write(content)


# def main():
#     filenames = [
#         'c:/temp/test1.txt',
#         'c:/temp/test2.txt',
#         'c:/temp/test3.txt',
#         'c:/temp/test4.txt',
#         'c:/temp/test5.txt',
#         'c:/temp/test6.txt',
#         'c:/temp/test7.txt',
#         'c:/temp/test8.txt',
#         'c:/temp/test9.txt',
#         'c:/temp/test10.txt',
#     ]

#     for filename in filenames:
#         replace(filename, 'ids', 'id')


# if __name__ == "__main__":
#     start_time = perf_counter()

#     main()

#     end_time = perf_counter()
#     print(f'It took {end_time- start_time :0.2f} second(s) to complete.')








from threading import Thread
from time import perf_counter


def replace(filename, substr, new_substr):
    print(f'Processing the file {filename}')
    # get the contents of the file
    with open(filename, 'r') as f:
        content = f.read()

    # replace the substr by new_substr
    content = content.replace(substr, new_substr)

    # write data into the file
    with open(filename, 'w') as f:
        f.write(content)


def main():
    filenames = [
        'c:/temp/test1.txt',
        'c:/temp/test2.txt',
        'c:/temp/test3.txt',
        'c:/temp/test4.txt',
        'c:/temp/test5.txt',
        'c:/temp/test6.txt',
        'c:/temp/test7.txt',
        'c:/temp/test8.txt',
        'c:/temp/test9.txt',
        'c:/temp/test10.txt',
    ]

    # create threads
    threads = [Thread(target=replace, args=(filename, 'id', 'ids'))
            for filename in filenames]

    # start the threads
    for thread in threads:
        thread.start()

    # wait for the threads to complete
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    start_time = perf_counter()

    main()

    end_time = perf_counter()
    print(f'It took {end_time- start_time :0.2f} second(s) to complete.')
