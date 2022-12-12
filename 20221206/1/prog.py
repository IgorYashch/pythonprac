import asyncio

evnt = asyncio.Event()

async def writer(queue, time_delay):
    i = 0
    while not evnt.is_set():
        await asyncio.sleep(time_delay)
        await queue.put(f"{i}_задержка")
        i += 1


async def stacker(queue, stack):
    while not evnt.is_set():
        elem = async queue.get()
        stack.append(elem)


async def reader(stack, num, time_delay):
    for i in range(num):
        await asyncio.sleep(time_delay)
        elem = stack.pop()
        print(elem)
    evnt.set()
