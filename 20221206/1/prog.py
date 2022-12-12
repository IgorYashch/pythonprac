import asyncio

evnt = asyncio.Event()

async def writer(queue, time_delay):
    i = 0
    while not evnt.is_set():
        await asyncio.sleep(time_delay)
        await queue.put(f"{i}_{time_delay}")
        i += 1


async def stacker(queue, stack):
    while not evnt.is_set():
        elem = await queue.get()
        await stack.put(elem)


async def reader(stack, num, time_delay):
    k = 0

    while not evnt.is_set():
        await asyncio.sleep(time_delay)
        print(await stack.get())
        k += 1
        if k == num: evnt.set()


async def main():
    delay1, delay2, delay3, num = eval(input())
    queue = asyncio.Queue()
    stack = asyncio.LifoQueue()

    await asyncio.gather(
        writer(queue, delay1),
        writer(queue, delay2),
        reader(stack, num, delay3),
        stacker(queue, stack)
    )


asyncio.run(main())