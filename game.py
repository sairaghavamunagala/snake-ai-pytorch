import pygame
from enum import Enum
from collections import namedtuple
import random
import numpy as np
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


class SnakeGameAI:
    def __init__(self, width=640, height=480):

        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.reset()
        

    def reset(self):
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
        self.frame_iteration=0

    def _place_food(self):
        """
        This method is useful for putting the food in the game.
        """
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def playstep(self,action):
        """
        This method handles update_ui,gameover.
        """
        self.frame_iteration+=1
        self._move(action)
        self.snake.insert(0,self.head)

        reward=0
        gameover=False
        if self.is_collision() or self.frame_iteration>100*len(self.snake):
            reward=-10
            gameover=True
            return gameover,self.score
        
        if self.head==self.food:
            self.score+=1
            self._place_food()
        else:
            self.snake.pop()
       
        self._update_ui()
        self.clock.tick(SPEED)
        
        return reward,gameover, self.score
    
    def is_collision(self,pt=None):
        """
        This method checks for boundary conditions 
        and also snake is eating itself.
        """
        if pt is None:
            pt=self.head
        if pt.x < 0 or pt.x > self.width -BLOCK_SIZE or pt.y < 0 or pt.y > self.height-BLOCK_SIZE:
            return True
        if pt in self.snake[1:]:
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

    def _move(self,action):
         # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction=new_dir
        
        x=self.head.x
        y=self.head.y
        if self.direction==Direction.RIGHT:
            x+=BLOCK_SIZE
        if self.direction==Direction.LEFT:
            x-=BLOCK_SIZE
        if self.direction==Direction.UP:
            y-=BLOCK_SIZE
        if self.direction==Direction.DOWN:
            y+=BLOCK_SIZE

        self.head=Point(x,y)


