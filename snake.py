import random

import numpy as np
import tensorflow as tf

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts

tf.compat.v1.enable_v2_behavior()

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

        for index in np.ndindex(self.height, self.width):
            if index[0] == 0 or index[0] == (self.height - 1) or index[1] == 0 or index[1] == (self.width - 1):
                self.structure[index[0]][index[1]] = self.wall
                self.wall_cells.append((index[0], index[1]))
        
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
    
    def reset(self, board):
        board.place_food()
        head = board.food_cell
        while (head == board.food_cell):
            random_i = random.randint(1, board.height - 2)
            random_j = random.randint(1, board.width - 3)
            head = (random_i, random_j)
        self.head_location = head
        self.middle_cells = []
        self.tail_location = None
        self.length = 1
        self.direction = self.right
        self.food_count = 0
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
        elif self.length <= 2:
            self.tail_location = self.head_location
            self.move_head(board)
            return True
        elif self.length > 2:
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
    
    def check_distances(self, env, distances, direction):
        current = 0
        new = 0
        tp = list(self.head_location)
        if direction == self.up:
            tp[0] -= 1
        elif direction == self.down:
            tp[0] += 1
        elif direction == self.right:
            tp[1] += 1
        elif direction == self.left:
            tp[1] -= 1
        for index, d in zip(np.ndindex(env._board.height, env._board.width), distances):
            if self.head_location == index:
                current = d
            if index == tuple(tp):
                new = d
        if new <= current and new >= 0:
            return True

        return False
    
    def is_action_valid(self, env, action, distances):
        valid_move = True

        if action == 0:
            if (self.length > 1 and self.direction != self.down) or (self.length == 1):
                if self.check_distances(env, distances, self.up):
                    self.direction = self.up
                else:
                    valid_move = False
            elif self.length > 1 and self.direction == self.down:
                valid_move = False
        elif action == 1:
            if (self.length > 1 and self.direction != self.up) or (self.length == 1):
                if self.check_distances(env, distances, self.down):
                    self.direction = self.down
                else:
                    valid_move = False
            elif self.length > 1 and self.direction == self.up:
                valid_move = False
        elif action == 2:
            if (self.length > 1 and self.direction != self.left) or (self.length == 1):
                if self.check_distances(env, distances, self.right):
                    self.direction = self.right
                else:
                    valid_move = False
            elif self.length > 1 and self.direction == self.left:
                valid_move = False
        elif action == 3:
            if (self.length > 1 and self.direction != self.right) or (self.length == 1):
                if self.check_distances(env, distances, self.down):
                    self.direction = self.left
                else:
                    valid_move = False
            elif self.length > 1 and self.direction == self.right:
                valid_move = False

        return valid_move





class SnakeAiEnvironment(py_environment.PyEnvironment):

    def __init__(self, snake, board):
        self._snake = snake
        self._board = board
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(),
            dtype=np.dtype('int32'),
            minimum=0,
            maximum=3,
            name='action'
        )
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(1, self._board.width * self._board.height),
            dtype=np.dtype('int32'),
            minimum=-11250,
            maximum=11251,
            name='observation'
        )
        
    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec
    
    def _reset(self):
        self._snake.reset(self._board)
        return ts.restart(np.array(self.__state_to_observation(), dtype=np.dtype('int32')))

    def __state_to_observation(self):
        ls = []
        for index in np.ndindex(self._board.height, self._board.width):
            if self._board.structure[index[0]][index[1]] == self._board.wall:
                ls.append(11251)
            elif self._board.structure[index[0]][index[1]] == self._board.snake:
                ls.append(11251)
            elif self._board.structure[index[0]][index[1]] == self._board.food:
                ls.append(0)
            else:
                ls.append(abs(index[0]-self._board.food_cell[0]) + abs(index[1]-self._board.food_cell[1]))
        return [ls]
    
    def _step(self, action):
        if self._snake.check_game_status(self._board):
            return self._reset()
        
        distances = self.__state_to_observation()
        result = self._snake.is_action_valid(self, action, distances[0])

        if result == True:
            self._snake.move_snake(self._board)
            if self._snake.check_game_status(self._board):
                return ts.termination(np.array(
                    self.__state_to_observation(), 
                    dtype=np.dtype('int32')), 
                    reward=-1.0
                )
            elif self._snake.check_food_status(self._board):
                return ts.transition(np.array(
                    self.__state_to_observation(), 
                    dtype=np.dtype('int32')), 
                    reward=1.0,
                )
            else:
                return ts.transition(np.array(
                    self.__state_to_observation(), 
                    dtype=np.dtype('int32')), 
                    reward=0,
                )
        else:
            return ts.termination(np.array(
                self.__state_to_observation(), 
                dtype=np.dtype('int32')), 
                reward=-1.0
            )



        


    



            

                    

            
            
            






