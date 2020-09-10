import random

import numpy as np
import tensorflow as tf

from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import q_network
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common

class Board():

    wall = "wall"
    food = "food"
    snake = 'snake'

    def __init__(self, h, w):
        self.width = w
        self.height = h
        self.structure = np.full((self.height, self.width), None)
        self.wall_cells = []
        self.food_cell = None
    
    
    def setup(self):
        for index in np.ndindex(self.height, self.width):
            if index[0] == 0 or index[0] == (self.height - 1) or index[1] == 0 or index[1] == (self.width - 1):
                self.structure[index[0]][index[1]] = self.wall
                self.wall_cells.append((index[0], index[1]))
        return True
        
    def place_food(self):
        if self.food_cell != None:
            self.structure[self.food_cell[0]][self.food_cell[1]] = None
        found_new_food = False
        while (found_new_food == False):
            random_i = random.randint(1, self.height - 2)
            random_j = random.randint(1, self.width - 2)
            for index in np.ndindex(self.height, self.width):
                if index == (random_i, random_j) and self.structure[index[0]][index[1]] != self.snake:
                    found_new_food = True    
        self.structure[random_i][random_j] = self.food
        self.food_cell = (random_i, random_j)
        return True
    
    def update_with_snake(self, snake):
        for index in np.ndindex(self.height, self.width):
            if self.structure[index[0]][index[1]] == self.snake:
                self.structure[index[0]][index[1]] = None
        self.structure[snake.head_location[0]][snake.head_location[1]] = self.snake
        if snake.length > 1:
            self.structure[snake.tail_location[0]][snake.tail_location[1]] = self.snake
            for cell in snake.middle_cells:
                self.structure[cell[0]][cell[1]] = self.snake
        return True

class Snake():
    up = "up"
    down = "down"
    left = "left"
    right = "right"

    def __init__(self):
        self.length = 1
        self.direction = self.right
        self.head_location = None
        self.tail_location = None
        self.middle_cells = []
        self.food_count = 0
    
    def setup(self, board):
        head = board.food_cell
        while (head == board.food_cell):
            random_i = random.randint(1, board.height - 2)
            random_j = random.randint(1, board.width - 3)
            head = (random_i, random_j)
        self.head_location = head
        self.tail_location = None
        board.update_with_snake(self)
        return True

    
    def move_head(self, board):
        head_list = list(self.head_location)
        if self.direction == self.up:
            head_list[0] -= 1
        if self.direction == self.down:
            head_list[0] += 1
        if self.direction == self.right:
            head_list[1] += 1
        if self.direction == self.left:
            head_list[1] -= 1
        self.head_location = (head_list[0], head_list[1])
        board.update_with_snake(self)
        return True
    
    def move_snake(self, board):
        if self.tail_location == None:
            self.move_head(board)
            return True
        if self.length <= 2:
            self.tail_location = self.head_location
            self.move_head(board)
            return True
        if self.length > 2:
            self.tail_location = self.middle_cells.pop()
            if self.length == 3:
                self.middle_cells.append(self.head_location)
            else:
                self.middle_cells.insert(0, self.head_location)
            self.move_head(board)
        return True
    
    def check_food_status(self, board):
        if board.food_cell == self.head_location:
            self.food_count += 1
            board.place_food()
            if self.tail_location == None:
                self.tail_location = self.head_location
            elif self.length <= 2:
                self.middle_cells.append(self.head_location)
            else:
                self.middle_cells.insert(0, self.head_location)
            self.length += 1
            return True
        return False

    def check_game_status(self, board):
        for cell in board.wall_cells:
            if cell == self.head_location:
                return True
        for cell in self.middle_cells:
            if cell == self.head_location:
                return True
        return False

    

            

                    

            
            
            






