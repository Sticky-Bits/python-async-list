import random
import asyncio
import curses


def init_curses(num_tasks):
    stdscr = curses.initscr()
    height, width = stdscr.getmaxyx()
    win = curses.newpad(num_tasks, 300)
    curses.start_color()
    curses.use_default_colors()
    # -1 is default terminal background color
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.noecho()
    curses.cbreak()
    # Turn off cursor
    curses.curs_set(0)
    return (win, height, width)

def addstr(win_info, x, y, text, color=0):
    win, height, width = win_info
    win.addstr(x, y, text, color)
    win.clrtoeol()
    win.clearok(1)
    win.refresh(0, 0, 0, 0, height-1, width-1)

async def run_tasks_async_with_progress(tasks):
    sem = asyncio.Semaphore(2)
    win_info = init_curses(len(tasks) + 1)
    addstr(win_info, 0, 0, f'Your command is now running on the following {len(tasks)} servers (may extend off bottom of terminal):')
    # Ugly.
    just = len(max(tasks, key=lambda x: len(x[1]))[1]) + 1
    tasks = [print_async_complete(task, num + 1, just, win_info, sem) for num, task in enumerate(tasks)]
    outputs = await asyncio.gather(*tasks[::-1])
    addstr(win_info, 0, 0, 'Done. Press enter to print the outputs of the commands.')
    curses.echo()
    curses.nocbreak()
    input()
    curses.endwin()
    print("\n\n".join(outputs))


async def print_async_complete(task, position, just, win_info, sem):
    cor, name = task
    addstr(win_info, position, 0, name)
    output = f'{"-"*20}\n{name}\n{"-"*20}\n'
    try:
        await sem.acquire()
        output += await cor
    except Exception as e:
        addstr(win_info, position, just, '✗', curses.color_pair(1))
        output += f'Exception: {str(e)}'
    else:
        addstr(win_info, position, just, '✔', curses.color_pair(2))
    sem.release()
    return output

# Above is library
# Below is example


async def migrate():
    await asyncio.sleep(random.uniform(0, 1))
    if random.random() < 0.3:
        raise Exception("OOPS")
    return "I ran!"


def main():
    servers = [f'server {x+1}' for x in range(20)]
    example_jobs = [(migrate(), server_name) for server_name in servers]
    asyncio.run(run_tasks_async_with_progress(example_jobs))


if __name__ == "__main__":
    main()
