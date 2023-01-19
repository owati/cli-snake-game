from state import SnakeDirection
from copy import deepcopy

class Snake:
    def __init__(self) -> None:
        self.direction = SnakeDirection.LEFT
        self.body = [
            (0,0),
            (1,0),
            (2,0),
            (3,0)
        ]

    def change_direction(self, direction : SnakeDirection) -> None:
        self.direction = direction

    def move(self, food : list, wall : list) -> bool:
        last_coord = self.body[-1]
        head_cord = self.body[0]
        self.body = self.body[:-1]

        self.body.insert(0, (head_cord[0] + self.direction.value[0], head_cord[1] + self.direction.value[1]))
        if food and self.body[0] == food[0]:
            self.body.append(last_coord)
            food[0] = None 
        if abs(self.body[0][0]) >= 59 or abs(self.body[0][1]) >= 14 or self.body[0] in wall:
            self.reset()
            return True
        return False

    def get_body(self) -> list:
        return self.body

    def reset(self) -> None:
        self.body = [
            (0,0),
            (1,0),
            (2,0),
            (3,0)
        ]


if __name__ == "__main__":
    snake = Snake()
    snake.move()
    print(snake.get_body())
