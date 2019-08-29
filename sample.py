import random
import asyncio
import curses


def init_curses():
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    # -1 is default terminal background color
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.noecho()
    curses.cbreak()
    # Turn off cursor
    curses.curs_set(0)
    return stdscr


async def run_tasks_async_with_progress(tasks):
    stdscr = init_curses()
    # Ugly.
    just = len(max(tasks, key=lambda x: len(x[1]))[1]) + 1
    tasks = [print_async_complete(task, num, len(tasks), just, stdscr) for num, task in enumerate(tasks)]
    outputs = await asyncio.gather(*tasks)
    stdscr.addstr(len(tasks), 0, 'Done. Would you like to print the outputs of the commands? [Y/n]')
    stdscr.refresh()
    curses.echo()
    curses.nocbreak()
    print_logs = input().lower() != 'n'
    curses.endwin()
    if print_logs:
        print("\n\n".join(outputs))


async def print_async_complete(task, position, length, just, stdscr):
    """
    Move cursor to `position`, print task name, run  task coroutine, then move
    back to `pos` print message and a justified completion mark (red cross or
    green check) depending on if the coroutine raises an exception or not.
    """
    cor, name = task
    # TODO: Log output of `cor` to a file named f'{name}.log'
    stdscr.addstr(position, 0, name)
    stdscr.refresh()
    output = f'{"-"*20}\n{name}\n{"-"*20}\n'
    try:
        output += await cor
    except Exception as e:
        stdscr.addstr(position, just, '✗', curses.color_pair(1))
        output += f'Exception: {str(e)}'
    else:
        stdscr.addstr(position, just, '✔', curses.color_pair(2))
    stdscr.refresh()
    output += f'\n{"-"*20}'
    return output


# Above is library
# Below is example


async def migrate():
    await asyncio.sleep(random.uniform(1, 5))
    if random.random() < 0.3:
        raise Exception("OOPS")
    return "I ran!"


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
