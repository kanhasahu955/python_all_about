# from asyncio import sleep,run,create_task,wait_for
# from asyncio.exceptions import TimeoutError

# async def api_call(message:str,result=1000,delay=3):
#     print(message)
#     await sleep(delay)
#     return result

# async def main():
#     task = create_task(api_call('Get stock price of MSFT..',result=2000,delay=4))
#     MAX_WAIT_TIME = 3

#     try:
#         result =await wait_for(task,MAX_WAIT_TIME)
#     except TimeoutError:
#         print('the task timed out')
#     else:
#         print('the task completed')
#         print(f'result: {result}')

# run(main())



from asyncio import sleep,run,create_task,wait_for,shield
from asyncio.exceptions import TimeoutError

async def api_call(message: str, result=100, delay=3):
    print(message)
    await sleep(delay)
    return result

async def main():
    task = create_task(api_call('Get stock price of MSFT..',result=2000,delay=4))
    MAX_WAIT_TIME = 3

    try:
        await wait_for(shield(task),timeout=MAX_WAIT_TIME)
    except TimeoutError:
        print('The task took more than expected and will complete soon.')
        result = await task
        print(f'result: {result}')
    else:
        print('the task completed')


if __name__ == '__main__':
    run(main())