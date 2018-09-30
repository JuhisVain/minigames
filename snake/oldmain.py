import os
import _thread
import time

clear_term = 'clear'  # unix terminal clearing


def main():

    field_width = 20
    field_height = 10

    field = []

    for i in range(field_width*field_height):
        field.append('.')

    snake = [(field_width//2, field_height//2),     # head
             (field_width//2, field_height//2 + 1),  # body
             (field_width//2, field_height//2 + 2)]  # tail

    snake_dir = 'n'

    _thread.start_new_thread(field_timer, (1, snake, field, field_width,
                                           field_height, ))
    
    while True:
        
        user_input = input()
        #user_input = sys.stdin.read(1)
        if user_input == 'n' or user_input == 'e' or user_input == 's' or user_input == 'w':
            snake_dir = user_input
        
        if snake_dir == 'n':
            snake.insert(0, (snake[0][0], snake[0][1]-1))
        elif snake_dir == 'e':
            snake.insert(0, (snake[0][0]+1, snake[0][1]))
        elif snake_dir == 's':
            snake.insert(0, (snake[0][0], snake[0][1]+1))
        elif snake_dir == 'w':
            snake.insert(0, (snake[0][0]-1, snake[0][1]))

        field[snake[0][0] + snake[0][1]*field_width] = '#'
        snake_pop = snake.pop()
        field[snake_pop[0] + snake_pop[1]*field_width] = '.'


def field_timer(interval, snake, field, field_width, field_height):
    while True:
        # termios.tcsendbreak(sys.stdin.fileno(),1)
        os.system("\n")
        time.sleep(interval)

        os.system(clear_term)

        for y in range(field_height):
            for x in range(field_width):
                print(field[x+y*field_width], end='')
            print()

if __name__ == "__main__":
    main()
