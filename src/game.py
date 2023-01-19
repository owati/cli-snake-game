import threading
import time
import curses
from random import randint

from state import State, SnakeDirection
from cursehandler import CurseHandler
from snake import Snake



def main() -> None:
    keypressed = None 
    state = State.BEGIN  
    snake = Snake()
    handler = CurseHandler()

    food = [None]

    wall = []
    handler.setup()

    dead = False 

    def handle_key_pressing():
        nonlocal keypressed
        while state != State.END:
            keypressed = handler.stdscr.getch()

    def generate_food(snake_cord : list):
        nonlocal food
        food_x = randint(0, 58)
        food_y = randint(0, 13)

        while (food_x, food_y) in snake_cord or (food_x, food_y) in wall:
            food_x = randint(0, 58)
            food_y = randint(0, 13)
        food = [(food_x, food_y)]

    def generate_map() -> None:
        for i in range(-10, 11):
            wall.extend([(-40, i), (40, i)])

        for j in range(20, 40):
            wall.extend([(j, -10), (-j, -10), (j, 10), (-j, 10)])

        for k in range(0, 30):
            wall.extend([(k, -5), (k, 5), (-k, 5), (-k, -5)])


    key_pressing_thread = threading.Thread(target=handle_key_pressing)
    key_pressing_thread.start()

    generate_map()

    try:
        
        while state != State.END:
            if keypressed == ord('q'):
                state = State.END
                break

            if state in [State.BEGIN, State.GAME_OVER]:
                if keypressed:
                    state = State.PLAYING
            
            if state == State.PLAYING:
                dead = snake.move(food, wall)

                if dead:
                    state = State.GAME_OVER
                    keypressed = None
                    food = [None]
                    snake.change_direction(SnakeDirection.UP)

                if not food[0]:
                    generate_food(snake.get_body())

                if keypressed == curses.KEY_UP and snake.direction != SnakeDirection.DOWN:
                    snake.change_direction(SnakeDirection.UP)
                elif keypressed == curses.KEY_DOWN and snake.direction != SnakeDirection.UP:
                    snake.change_direction(SnakeDirection.DOWN)
                elif keypressed == curses.KEY_LEFT and snake.direction != SnakeDirection.RIGHT:
                    snake.change_direction(SnakeDirection.LEFT)
                elif keypressed == curses.KEY_RIGHT and snake.direction != SnakeDirection.LEFT:
                    snake.change_direction(SnakeDirection.RIGHT)


            handler.run(state=state, snake=snake.get_body() , food=food, wall=wall)
            # text=f'{chr(keypressed if keypressed else 12)} {food[0]} {wall}'

            time.sleep(0.08)
        


        key_pressing_thread.join()
        handler.terminate()
    except Exception as e:
        key_pressing_thread.join()
        handler.terminate()
        print(e)
    return

if __name__ == "__main__":
    main()