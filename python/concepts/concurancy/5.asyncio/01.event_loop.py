import asyncio

# def square(number:int)->int:
#     return number * number

# result = square(10)
# print(result)


# async def square(number:int)->int:
#     return number * number

# result = asyncio.run(square(10))
# print(result)

async def square(number:int)->int:
    return number*number

async def main():
    x = await square(10)
    print(f'x = {x}')

    y = await square(20)
    print(f'y = {y}')

    print(f'total = {x + y}')

asyncio.run(main())