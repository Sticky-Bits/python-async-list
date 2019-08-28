import random
import asyncio


RED_CROSS = "\033[31m✗\033[0m"
GREEN_CHECK = "\033[32m✔\033[0m"


def move_cursor(x, y):
    print(f'\x1b[{y+1};{x+1}H')


def clear():
    print('\x1b[2J')


async def run_tasks_async_with_progress(tasks):
    just = len(max(tasks, key=lambda x: len(x[1]))[1])
    tasks = [print_async_complete(task, num, len(tasks), just) for num, task in enumerate(tasks)]
    clear()
    await asyncio.gather(*tasks)


async def print_async_complete(task, position, length, just):
    """
    Move cursor to `position`, print task name, run  task coroutine, then move
    back to `pos` print message and a justified completion mark (red cross or
    green check) depending on if the coroutine raises an exception or not.
    """
    cor, name = task
    # TODO: Log output of `cor` to a file named f'{name}.log'
    move_cursor(0, position)
    print(name)
    try:
        await cor
    except Exception:
        completed_icon = RED_CROSS
    else:
        completed_icon = GREEN_CHECK
    move_cursor(0, position)
    print(name.ljust(just) + f" {completed_icon}")
    move_cursor(0, length)


async def migrate():
    await asyncio.sleep(random.uniform(1, 5))
    if random.random() < 0.3:
        raise Exception("OOPS")


# Above is library
# Below is example


def main():
    servers = [
        'myserver',
        'otherserver',
        'blahserver',
        'bigcompany',
        'blah',
        'some',
        'other',
        'server',
        'names',
        'here',
    ]
    example_jobs = [(migrate(), server_name) for server_name in servers]
    asyncio.run(run_tasks_async_with_progress(example_jobs))


if __name__ == "__main__":
    main()
