from enum import Enum
import random
import curses
import _thread
import time


class dir(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


FRUIT = 987654321


def main():
    random.seed()
    stdscr = init_curses()

    field_width = 20
    field_height = 10

    field = []
    for i in range(field_width*field_height):
        field.append(0)

    for y in range(field_height):
        for x in range(field_width):
            if y == 0 or y == field_height-1 or x == 0 or x == field_width-1:
                field[y*field_width+x] = -1

    snake_dir = dir.N
    snake_head = [field_width//2, field_height//2]
    snake_length = 3

    max_fruits = 3
    field[random.randrange(1, field_width-2) +
          random.randrange(1, field_height-2) * field_width] = FRUIT
    current_fruits = 1

    ramaramadingdong = [True]
    _thread.start_new_thread(ticker, (ramaramadingdong, ))
    print_field(stdscr, field, field_width, field_height)

    while True:

        input_dir = stdscr.getch()

        while ramaramadingdong[0]:
            pass
        ramaramadingdong[0] = True
        
        if not input_dir:
            pass
        elif input_dir == curses.KEY_UP:
            snake_dir = dir.N
        elif input_dir == curses.KEY_RIGHT:
            snake_dir = dir.E
        elif input_dir == curses.KEY_DOWN:
            snake_dir = dir.S
        elif input_dir == curses.KEY_LEFT:
            snake_dir = dir.W

        if snake_dir == dir.N:
            snake_head[1] -= 1
        elif snake_dir == dir.E:
            snake_head[0] += 1
        elif snake_dir == dir.S:
            snake_head[1] += 1
        elif snake_dir == dir.W:
            snake_head[0] -= 1

        head_string = "Head:(" + str(snake_head[0]) + "," + str(snake_head[1]) + ")"
        length_string = "length: " + str(snake_length)
        stdscr.addstr(field_height, 0, head_string)
        stdscr.addstr(field_height + 1, 0, length_string)

        landing_coord = snake_head[0]+field_width*snake_head[1]

        if field[landing_coord] != FRUIT:  # If snake does not eat fruit, decr tails
            for y in range(field_height):
                for x in range(field_width):
                    if field[y*field_width+x] > 0 and field[y*field_width+x] != FRUIT:
                        field[y*field_width+x] -= 1

        if field[landing_coord] == 0:
            field[landing_coord] = snake_length
        elif field[landing_coord] == FRUIT:
            current_fruits -= 1
            snake_length += 1
            field[landing_coord] = snake_length
        else:
            pass
            # print("death")

        if current_fruits < max_fruits and random.randrange(1, 100) < 10:
            xc = random.randrange(1, field_width-2)
            yc = random.randrange(1, field_height-2)*field_width
            if field[xc+yc] == 0:
                field[xc+yc] = FRUIT
                current_fruits += 1

        print_field(stdscr, field, field_width, field_height)

    curses.nocbreak()
    curses.echo()
    stdscr.keypad(False)
    curses.endwin()

    
def val_to_char(val):
    if val < 0:
        return '#'
    elif val == 0:
        return '.'
    elif val == FRUIT:
        return '&'
    elif val > 0:
        return 'o'


def print_field(stdscr, field, field_width, field_height):
    for y in range(field_height):
        for x in range(field_width):
            stdscr.addch(y, x, val_to_char(field[y*field_width+x]))
    stdscr.refresh()


def ticker(lock):
    while True:
        time.sleep(0.5)
        lock[0] = False



def init_curses():
    stdscr = curses.initscr()
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    stdscr.timeout(500)
    return stdscr


if __name__ == "__main__":
    main()
