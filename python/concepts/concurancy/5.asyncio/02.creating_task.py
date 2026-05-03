# from asyncio import sleep,run
# from time import perf_counter

# async def api_call(message:str,result=1000,delay=3):
#     print(message)
#     await sleep(delay)
#     return result

# async def main():
#     start_time = perf_counter()

#     price = await api_call('Get stock price of MSFT.. ',300)
#     print(f'price = {price}')

#     price = await api_call('Get stock price of GOOGL.. ',200)
#     print(f'price = {price}')

#     end_time = perf_counter()
#     print(f'Time taken: {end_time - start_time} seconds')

# run(main())



# from asyncio import sleep,run, create_task
# from time import perf_counter

# async def api_call(message:str,result=1000,delay=3):
#     print(message)
#     await sleep(delay)
#     return result

# async def main():
#     start_time = perf_counter()

#     task1 = create_task(api_call('Get stock price of MSFT.. ',300))
#     task2 = create_task(api_call('Get stock price of GOOGL.. ',200))

#     price1 = await task1
#     price2 = await task2

#     print(f'price1 = {price1}')
#     print(f'price2 = {price2}')

#     end_time = perf_counter()
#     print(f'Time taken: {end_time - start_time} seconds')

# run(main())




from asyncio import sleep,run,create_task
from time import perf_counter

async def call_api(message:str,result=1000,delay=3):
    print(message)
    await sleep(delay)
    return result

async def show_message():
    for _ in range(3):
        await sleep(1)
        print('api call is in progress...')

async def main():
    start_time = perf_counter()

    message_task = create_task(show_message())

    task1 = create_task(call_api('Get stock price of MSFT.. ',300))
    task2 = create_task(call_api('Get stock price of GOOGL.. ',200))

    price = await task1
    print(f'price1 = {price}')
    price = await task2
    print(f'price2 = {price}')

    await message_task


    end_time = perf_counter()
    print(f'Time taken: {end_time - start_time} seconds')

if __name__ == '__main__':
    run(main()) 