from asyncio import sleep,run,create_task,CancelledError

async def api_call(message:str,result=1000,delay=3):
    print(message)
    await sleep(delay)
    return result

async def main():
    task = create_task(api_call('Get stock price of MSFT.. ',300))
    time_elapsed = 0
    while not task.done():
        time_elapsed += 1
        await sleep(1)
        print('task is not done yet, time elapsed: ',time_elapsed)

        if time_elapsed == 3:
            print('cancelling the task...')
            task.cancel()
            break
    try:
        await task
    except CancelledError:
        print('the task was cancelled')
    else:
        print('the task was completed')
        print(f'result: {task.result()}')

run(main())