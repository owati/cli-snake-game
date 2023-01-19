import curses
import time
from state import State

FRAME_WIDTH = 120
FRAME_HEIGHT = 30

class CurseHandler:
    def __init__(self) -> None:
        '''
        Initializes the curse enviroment
        '''
        self.stdscr = curses.initscr()
        if curses.LINES < FRAME_HEIGHT or curses.COLS < FRAME_WIDTH:
            self.terminate()
            raise Exception("The terminal window is too small")

    def setup(self) -> None:
        '''
        Setup teh curses enviroment
        '''
        self.stdscr.keypad(True)
        curses.cbreak()
        curses.noecho()
        curses.curs_set(False)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
        self.frame_coord_x, self.frame_coord_y = int((curses.LINES - FRAME_HEIGHT)/ 2), int((curses.COLS - FRAME_WIDTH) / 2)

    def terminate(self) -> None:
        '''
        Terminate the Curses environment
        '''
        curses.nocbreak()
        curses.echo()
        self.stdscr.keypad(False)
        curses.curs_set(True)
        curses.endwin()
        print(curses.LINES, curses.COLS, int((curses.LINES - FRAME_HEIGHT)/ 2), int((curses.COLS - FRAME_WIDTH) / 2))

    def draw_frame(self) -> None:
        '''
        Draws the frame of the game area
        '''
        self.stdscr.addstr(self.frame_coord_x, self.frame_coord_y, '-'*FRAME_WIDTH, curses.color_pair(1))
        self.stdscr.addstr(self.frame_coord_x + FRAME_HEIGHT - 1, self.frame_coord_y, '-'*FRAME_WIDTH, curses.color_pair(1))
        for i in range(FRAME_HEIGHT - 2):
            self.stdscr.addstr(self.frame_coord_x + 1 + i, self.frame_coord_y , '|', curses.color_pair(1))
            self.stdscr.addstr(self.frame_coord_x + 1 + i, self.frame_coord_y + FRAME_WIDTH , '|', curses.color_pair(1))

    def addstrcoord(self, x :  int, y : int, _str : str, color=None ) -> None:
        '''
        Abstracts the frame positoning to normal cartesian plane
        '''
        self.stdscr.addstr(
            self.frame_coord_x + int((FRAME_HEIGHT - 2) / 2) - y,
            self.frame_coord_y + int((FRAME_WIDTH - 2) / 2) + x,
            _str,
            curses.color_pair(1) if not color else color
        )

    def display_welcome_text(self) -> None:
        self.addstrcoord(-5, 0, "SNAKE GAME", curses.color_pair(1))
        self.addstrcoord(-16, -2, "Press any key to play, q to quit", curses.color_pair(1))

    def display_gameover_text(self) -> None:
        self.addstrcoord(-5, 0, "GAME OVER", curses.color_pair(1))
        self.addstrcoord(-16, -2, "Press any key to play, q to quit", curses.color_pair(1))

    def draw_snake(self, snake_cords : list) -> None:
        for x, y in snake_cords:
            self.addstrcoord(x, y, '█', curses.color_pair(2))

    def draw_food(self, food_coord : tuple) -> None:
        self.addstrcoord(food_coord[0], food_coord[1], '█', curses.color_pair(3))

    def write_score(self, snake_length: int) -> None:
        self.addstrcoord(50, 15, f'Score: {snake_length - 4}', curses.color_pair(2))
    
    def draw_wall(self, wall : list) -> None:
        for x, y in wall:
            self.addstrcoord(x, y, '█', curses.color_pair(1))
            
    def run(self, state=State.BEGIN, snake=[], food=None, wall=[], text="None",) -> None:
        try:
            self.stdscr.clear()
            self.draw_frame()
            # self.stdscr.addstr(0,0,text + f'{state}') 
            if state == State.BEGIN:
                self.display_welcome_text()
            
            elif state == State.PLAYING:
                self.draw_snake(snake)
                self.draw_wall(wall)
                self.write_score(len(snake))
                if food[0]:
                    self.draw_food(food[0])
            
            elif state == State.GAME_OVER:
                self.display_gameover_text()
    
            self.stdscr.refresh()
        except Exception as e:
            self.terminate()
            print(e)

