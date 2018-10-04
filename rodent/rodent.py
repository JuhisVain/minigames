import _thread
import time
import curses
import random

EMPTY = 0
WALL = 1
BLOCK = 2
CAT = 3
MOUSE = 4
CHEESE = 5

score = 0


def main():
    # init
    random.seed()
    
    field_width = 23
    field_height = 23
    border_zone = 3

    mouse = [(field_width//2), (field_height//2)]
    
    cat_list = []
    cat_list.append( [2,2] )

    stdscr = init_curses()

    # make field
    field = [[EMPTY for x in range(field_width)] for y in range(field_height)]

    #make border walls
    for i in range(field_width):
        field[i][0] = WALL
        field[i][field_height-1] = WALL

    for i in range(field_height):
        field[0][i] = WALL
        field[field_width-1][i] = WALL
        
    # make pushable blocks
    for y in range(field_height - border_zone*2):
        for x in range(field_width - border_zone*2):
            field[border_zone+x][border_zone+y] = BLOCK

    # test:
    # field[8][8] = WALL  # OK, can't be moved

    # place mouse at center
    field[mouse[0]][mouse[1]] = MOUSE

    _thread.start_new_thread(tick, (field, cat_list, mouse, stdscr, ))

    while True:
        input_key = stdscr.getch()
        move(mouse, input_key, field)
        print_field(stdscr, field)


def move(coord, direction, field):
    x_mod = 0
    y_mod = 0
    if direction == curses.KEY_UP:
        y_mod -= 1
    elif direction == curses.KEY_RIGHT:
        x_mod += 1
    elif direction == curses.KEY_DOWN:
        y_mod += 1
    elif direction == curses.KEY_LEFT:
        x_mod -= 1

    target = field[coord[0]+x_mod][coord[1]+y_mod]

    if target == BLOCK:
        move([coord[0]+x_mod, coord[1]+y_mod], direction, field)

    target = field[coord[0]+x_mod][coord[1]+y_mod]
    # target can't be used, need reference
    if target == EMPTY or target == CHEESE:
        memory = field[coord[0]][coord[1]]
        field[coord[0]][coord[1]] = EMPTY
        coord[0] += x_mod
        coord[1] += y_mod
        field[coord[0]][coord[1]] = memory
        if memory == MOUSE and target == CHEESE:
            eat_cheese()


def eat_cheese():
    global score
    score += 100


def tick(field, cat_list, mouse, stdscr):
    while True:
        time.sleep(0.75)
        feline_strategy(field, cat_list, mouse)
        print_field(stdscr, field)


def feline_strategy(field, cat_list, mouse):
    for cat in cat_list:
        mod_x = 0
        mod_y = 0
        if mouse[0] < cat[0]:
            mod_x = -1
        elif mouse[0] > cat[0]:
            mod_x = 1
        else:
            pass

        if mouse[1] < cat[1]:
            mod_y = -1
        elif mouse[1] > cat[1]:
            mod_y = 1
        else:
            pass

        if field[cat[0]+mod_x][cat[1]+mod_y] == EMPTY:
            pass
        elif field[cat[0]][cat[1]+mod_y] == EMPTY:
            mod_x = 0
        elif field[cat[0]+mod_x][cat[1]] == EMPTY:
            mod_y = 0
        else:
            mod_x = 0
            mod_y = 0
            if cheese_magic(cat, field, cat_list):
                continue

        field[cat[0]][cat[1]] = EMPTY
        cat[0] += mod_x
        cat[1] += mod_y
        field[cat[0]][cat[1]] = CAT


def cheese_magic(cat, field, cat_list):
    for x in range(-1,2):
        for y in range(-1,2):
            tile = field[cat[0]+x][cat[1]+y]
            if x == 0 and y == 0:
                continue
            elif tile == BLOCK or tile == WALL:
                continue
            else:
                return False

    # if we got here the cat is trapped
    global score
    score += 50
    field[cat[0]][cat[1]] = CHEESE
    cat_list.remove(cat)
    spawn_cats(cat_list, field)
    return True


def spawn_cats(cat_list, field):
    if len(cat_list) != 0:
        return
    for n in range(random.randrange(1, 3)):
        while True:
            tent_x = random.randrange(1, len(field)-2)
            tent_y = random.randrange(1, len(field[0])-2)
            if field[tent_x][tent_y] == EMPTY:
                field[tent_x][tent_y] = CAT
                cat_list.append( [tent_x, tent_y] )
                break

def print_field(stdscr, field):
    for y in range(len(field[0])):
        for x in range(len(field)):
            stdscr.addch(y, x, val_to_char(field[x][y]))

    global score
    stdscr.addstr(len(field[0]), 0, "SCORE : " + str(score))
    stdscr.refresh()

def val_to_char(value):
    if value == EMPTY:
        return '-'
    elif value == WALL:
        return '='
    elif value == BLOCK:
        return '#'
    elif value == CAT:
        return 'C'
    elif value == MOUSE:
        return '@'
    elif value == CHEESE:
        return 'b'

def init_curses():
    stdscr = curses.initscr()
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    return stdscr

if __name__ == "__main__":
    main()
