import random
import math

import numpy as np


class Board():
    """A class to define the board structure and cells"""
    wall = "wall"
    food = "food"
    snake = 'snake'

    def __init__(self, h, w):
        self.width = w
        self.height = h
        self.structure = np.full((self.height, self.width), None)
        self.wall_cells = []
        self.food_cell = None

        # Define the outer cells of the board to be walls
        for index in np.ndindex(self.height, self.width):
            if index[0] == 0 or index[0] == (self.height - 1) or index[1] == 0 or index[1] == (self.width - 1):
                self.structure[index[0]][index[1]] = self.wall
                self.wall_cells.append((index[0], index[1]))

    def place_food(self, other_player_board=None):
        """Assign a new cell in the board as food"""
        if self.food_cell != None:
            self.structure[self.food_cell[0]][self.food_cell[1]] = None
        found_new_food = False
        tried = []
        while (found_new_food == False):
            random_i = random.randint(1, self.height - 2)
            random_j = random.randint(1, self.width - 2)
            if (random_i, random_j) in tried:
                continue
            for index in np.ndindex(self.height, self.width):
                if other_player_board == None:
                    if index == (random_i, random_j) and self.structure[index[0]][index[1]] != self.snake and index != self.food_cell:
                        found_new_food = True
                else:
                    if index == (random_i, random_j) and self.structure[index[0]][index[1]] != self.snake and index != self.food_cell and other_player_board.structure[index[0]][index[1]] != other_player_board.snake:
                        found_new_food = True
            tried.append((random_i, random_j))
            if len(tried) == (self.width - 2) * (self.height - 2):
                self.food_cell = None
                return False
        self.structure[random_i][random_j] = self.food
        self.food_cell = (random_i, random_j)
        return True

    def update_with_snake(self, snake):
        """Update the cells on the board to snake when snake moves"""
        for index in np.ndindex(self.height, self.width):
            if self.structure[index[0]][index[1]] == self.snake:
                self.structure[index[0]][index[1]] = None
        self.structure[snake.head_location[0]
                       ][snake.head_location[1]] = self.snake
        if snake.length > 1:
            self.structure[snake.tail_location[0]
                           ][snake.tail_location[1]] = self.snake
            for cell in snake.middle_cells:
                self.structure[cell[0]][cell[1]] = self.snake
        return True


class Snake():
    """A class to define how the snake moves and interacts with the board"""
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

    def reset(self, board, food_cell=None):
        """A function to reset board with snake starting position and new food cell."""
        if food_cell == None:
            board.place_food()
        else:
            board.food_cell = food_cell
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
        """Moves the head of the snake so a new cell is assigned to head location"""
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

    def move_snake(self, board, eaten):
        """Works with move_head to move the whole snake"""
        if self.length == 1:
            self.move_head(board)
            return True
        elif self.length == 2:
            self.tail_location = self.head_location
            self.move_head(board)
            return True
        elif self.length > 2:
            if eaten == False:
                self.tail_location = self.middle_cells.pop()
            if self.length == 3:
                self.middle_cells.append(self.head_location)
            else:
                self.middle_cells.insert(0, self.head_location)
            self.move_head(board)
        return True

    def check_food_status(self, board, other_player_board=None):
        """Checks if head of the snake is in the same cell as the food"""
        if board.food_cell == self.head_location:
            self.food_count += 1
            self.length += 1
            if self.tail_location == None:
                self.tail_location = self.head_location
            board.place_food(other_player_board)
            return True
        return False

    def check_game_status(self, board, computer=None):
        """Checks for various conditions to see if the game is over.
        Returns true if game is over else false."""
        if computer == None:
            for cell in board.wall_cells:
                if cell == self.head_location:
                    return True
            for cell in self.middle_cells:
                if cell == self.head_location:
                    return True
        else:
            for cell in board.wall_cells:
                if cell == self.head_location or cell == computer.head_location:
                    return True
            for cell in self.middle_cells:
                if cell == self.head_location or cell == computer.head_location:
                    return True
            for cell in computer.middle_cells:
                if cell == computer.head_location or cell == self.head_location:
                    return True
            if computer.head_location == self.head_location:
                return True
            if computer.head_location == self.tail_location or self.head_location == computer.tail_location:
                return True
        return False
