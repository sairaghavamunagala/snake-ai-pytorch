import pygame
from enum import Enum
from collections import namedtuple
import random

pygame.init()
font = pygame.font.Font("arial.ttf", 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x, y")

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 10


class SnakeGame:
    def __init__(self, width=640, height=480):

        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y),
        ]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        """
        This method is useful for putting the food in the game.
        """
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def playstep(self):
        """
        This method handles update_ui,gameover.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type ==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    self.direction=Direction.LEFT
                if event.key==pygame.K_RIGHT:
                    self.direction=Direction.RIGHT
                if event.key==pygame.K_UP:
                    self.direction=Direction.UP
                if event.key==pygame.K_DOWN:
                    self.direction=Direction.DOWN
        self._move(self.direction)
        self.snake.insert(0,self.head)
        gameover=False
        if self.is_collision():
            gameover=True
            return gameover,self.score
        
        if self.head==self.food:
            self.score+=1
            self._place_food()
        else:
            self.snake.pop()
       
        self._update_ui()
        self.clock.tick(SPEED)
        
        return gameover, self.score
    
    def is_collision(self):
        """
        This method checks for boundary conditions 
        and also snake is eating itself.
        """
        if self.head.x < 0 or self.head.x > self.width -BLOCK_SIZE or self.head.y < 0 or self.head.y > self.height-BLOCK_SIZE:
            return True
        if self.head in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        """
        This method is responsible for updating UI,
        it fills the screen with black color,
        it draw the snake with two blue colors,
        and also food item as well as score it will
        display.
        """
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(
                self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
            )
            pygame.draw.rect(
                self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12)
            )
        pygame.draw.rect(
            self.display,
            RED,
            pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),
        )

        text = font.render("Score:" + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self,direction):
        x=self.head.x
        y=self.head.y
        if direction==Direction.RIGHT:
            x+=BLOCK_SIZE
        if direction==Direction.LEFT:
            x-=BLOCK_SIZE
        if direction==Direction.UP:
            y-=BLOCK_SIZE
        if direction==Direction.DOWN:
            y+=BLOCK_SIZE

        self.head=Point(x,y)

if __name__ == "__main__":
    game = SnakeGame()

    while True:
        gameover, score = game.playstep()
        if gameover is True:
            print("Final Score:", score)
            break
        
    pygame.quit()
