import asyncio

async def merge(A, B, start, middle, finish, event_in1, event_in2, event_out):
    await event_in1.wait()
    await event_in2.wait()

    # чтобы можно было вызывать B = A
    A = A.copy()

    k = start
    pos1 = start
    pos2 = middle

    while not (pos1 == middle and pos2 == finish):
        if pos1 == middle:
            B[k] = A[pos2]
            pos2 += 1
        elif pos2 == finish:
            B[k] = A[pos1]
            pos1 += 1
        elif A[pos1] < A[pos2]:
            B[k] = A[pos1]
            pos1 += 1
        else:
            B[k] = A[pos2]
            pos2 += 1
        k += 1

    event_out.set()


async def mtasks(A):
    tasks = []
    B = A.copy()
    n = 1
    
    # рекурсивное создание тасков
    def create_tasks(start, finish, event_out):
        if abs(finish - start) <= 1:
            event_out.set()
            return None

        event1 = asyncio.Event()
        event2 = asyncio.Event()

        task = asyncio.create_task(
            merge(
                B, B, start, (start + finish) // 2, finish,
                event1, event2, event_out
            )
        )

        tasks.append(task)

        create_tasks(start, (start + finish) // 2, event1)
        create_tasks((start + finish) // 2, finish, event2)
        
        return None

    create_tasks(0, len(A), asyncio.Event())

    return tasks, B


import sys
exec(sys.stdin.read())