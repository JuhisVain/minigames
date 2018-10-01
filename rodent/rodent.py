import _thread
import time
import curses

EMPTY = 0
BLOCK = 1
CAT = 2
MOUSE = 3
CHEESE = 4


def main():
    # init
    field_width = 21
    field_height = 21
    border_zone = 3

    mouse = [(field_width//2 + 1), (field_height//2 + 1)]
    cat_list = []
    cat_list.append( [1,1] )

    stdscr = init_curses()

    # make field
    field = [[EMPTY for x in range(field_width)] for y in range(field_height)]

    # make pushable blocks
    for y in range(field_height - border_zone*2):
        for x in range(field_width - border_zone*2):
            field[border_zone+x][border_zone+y] = BLOCK

    # place mouse at center
    field[mouse[0]][mouse[1]] = MOUSE

    _thread.start_new_thread(tick, (field, cat_list, mouse, stdscr, ))
    
    stdscr.getch()

    

def tick(field, cat_list, mouse, stdscr):
    while True:
        time.sleep(0.75)
        feline_strategy(field, cat_list, mouse)
        print_field(stdscr, field)


def feline_strategy(field, cat_list, mouse):
    for cat in cat_list:
        wanna_go = cat[:]
        if mouse[0] < cat[0]:
            wanna_go[0] -= 1
        elif mouse[0] > cat[0]:
            wanna_go[0] += 1

        if mouse[1] < cat[1]:
            wanna_go[1] -= 1
        elif mouse[1] > cat[1]:
            wanna_go[1] += 1

            if field[wanna_go[0]][wanna_go[1]] == EMPTY:
                field[cat[0]][cat[1]] = EMPTY
                cat[0] = wanna_go[0]
                cat[1] = wanna_go[1]
                field[cat[0]][cat[1]] = CAT

        
def print_field(stdscr, field):
    for y in range(len(field[0])):
        for x in range(len(field)):
            stdscr.addch(y, x, val_to_char(field[x][y]))
    stdscr.refresh()

def val_to_char(value):
    if value == EMPTY:
        return '-'
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