import random
import math
from copy import deepcopy
from operator import itemgetter, attrgetter

import numpy as np

from snake import *

# Classes for BFS and DFS searches


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

# A class for AI


class PlayerAI():

    def __init__(self):
        self.up = 'up'
        self.down = 'down'
        self.left = 'left'
        self.right = 'right'

    def isValid(self, row, col, height, width):
        return (row >= 0) and (row < height) and (col >= 0) and (col < width)

    def isUnBlocked(self, copied_board, row, col, steps):
        if copied_board[row][col][0] == 0 or (copied_board[row][col][6] <= steps and copied_board[row][col][6] >= 0):
            return True
        else:
            return False

    def isDestination(self, src, dest):
        if src == dest:
            return True
        else:
            return False

    def calculateHvalue(self, row, col, dest):
        # abs(row-dest[0]) + abs(col-dest[1])
        return math.sqrt((row-dest[0])*(row-dest[0]) + (col-dest[1])*(col-dest[1]))

    def update_ai_board(self, row, col, blocked, copied_board, f, g, h, pi, pj):
        if blocked == True:
            copied_board[row][col][0] = 1
        else:
            copied_board[row][col][0] = 0

        copied_board[row][col][1] = f
        copied_board[row][col][2] = g
        copied_board[row][col][3] = h
        copied_board[row][col][4] = pi
        copied_board[row][col][5] = pj
        return copied_board

    def update_snake(self, ai_board, height, width, path, length, tail, steps):
        for i in range(height):
            for j in range(width):
                if ai_board[i][j][6] > 0 and ai_board[i][j][6] <= length:
                    ai_board[i][j][6] -= 1
                    if ai_board[i][j][6] == 0:
                        ai_board[i][j][0] = 0
                        ai_board[i][j][6] = 0

        for p in path:
            if length > 0:
                ai_board[p[0]][p[1]][6] = length
                ai_board[p[0]][p[1]][0] = 1
                length -= 1
                print(length)
            else:
                ai_board[p[0]][p[1]][6] = 0
                ai_board[p[0]][p[1]][0] = 0

    def print_path(self, ai_board, height, width, length):
        for i in range(height):
            for j in range(width):
                print(ai_board[i][j][6], end="")
            print("")

    def trace_path(self, copied_board, dest):
        row = dest[0]
        col = dest[1]

        path = []
        while (copied_board[row][col][4] != row or copied_board[row][col][5] != col):
            path.append((row, col))
            temp_row = copied_board[row][col][4]
            temp_col = copied_board[row][col][5]
            row = temp_row
            col = temp_col

        path.append((row, col))
        return path

    def get_neighbors(self, cell):
        neighbors = [
            (cell[0] - 1, cell[1]),
            (cell[0] + 1, cell[1]),
            (cell[0], cell[1] + 1),
            (cell[0], cell[1] - 1)
        ]

        return neighbors

    def breadthFirstSearch(self, start, height, width):
        frontier = QueueFrontier()
        cost_so_far = {}

        for s in start:
            frontier.add(s)
            cost_so_far[s] = 0

        while (not frontier.empty()):
            current = frontier.remove()
            neighbors = self.get_neighbors(current)
            for n in neighbors:
                if self.isValid(n[0], n[1], height, width):
                    if n not in cost_so_far:
                        cost_so_far[n] = cost_so_far[current] + 1
                        frontier.add(n)
        return cost_so_far

    def aStarSearch(self, src, dest, board, height, width, length, tail):
        ai_board = deepcopy(board)
        steps = 0
        if self.isValid(src[0], src[1], height, width) == False:
            print("Snake starting cell is NOT valid")
            return

        if self.isValid(dest[0], dest[1], height, width) == False:
            print("Destintion is NOT valid")
            return

        if self.isUnBlocked(ai_board, src[0], src[1], steps) == False or self.isUnBlocked(ai_board, dest[0], dest[1], steps) == False:
            print("Either source or destination is blocked")
            return

        if self.isDestination(src, dest) == True:
            print("We are already at the destination")
            return

        self.update_ai_board(src[0], src[1], False,
                             ai_board, 0.0, 0.0, 0.0, src[0], src[1])

        closedList = []
        openList = [{"pair": src, "f": 0}]

        foundDest = False
        depth = 0
        steps = 0

        while (len(openList) > 0):
            p = openList.pop(0)

            closedList.append((p["pair"]))

            i = p["pair"][0]
            j = p["pair"][1]

            d = abs(src[0] - i) + abs(src[1] - j)
            if d > depth:
                depth = d
                steps += 1

            # Cell-->Popped Cell (i, j)
            # N -->  North       (i-1, j)
            # S -->  South       (i+1, j)
            # E -->  East        (i, j+1)
            # W -->  West        (i, j-1)

            gNew, hNew, fNew = 0, 0, 0

            # North
            if self.isValid(i-1, j, height, width) == True:
                if self.isDestination((i-1, j), dest) == True:
                    ai_board[i-1][j][4] = i
                    ai_board[i-1][j][5] = j
                    path = self.trace_path(ai_board, dest)
                    # path.append(ai_board)
                    foundDest = True
                    return path

                elif (i-1, j) not in closedList and self.isUnBlocked(ai_board, i-1, j, steps) == True:
                    gNew = ai_board[i][j][2] + 1.0
                    hNew = self.calculateHvalue(i-1, j, dest)
                    fNew = gNew + hNew
                    if ai_board[i-1][j][1] == float('inf') or ai_board[i-1][j][1] < fNew:
                        openList.append({"pair": (i-1, j), "f": fNew})
                        ai_board = self.update_ai_board(
                            i-1, j, False, ai_board, fNew, gNew, hNew, i, j)

            # South
            if self.isValid(i+1, j, height, width) == True:
                if self.isDestination((i+1, j), dest) == True:
                    ai_board[i+1][j][4] = i
                    ai_board[i+1][j][5] = j
                    path = self.trace_path(ai_board, dest)
                    # path.append(ai_board)
                    foundDest = True
                    return path

                elif (i+1, j) not in closedList and self.isUnBlocked(ai_board, i+1, j, steps) == True:
                    gNew = ai_board[i][j][2] + 1.0
                    hNew = self.calculateHvalue(i+1, j, dest)
                    fNew = gNew + hNew
                    if ai_board[i+1][j][1] == float('inf') or ai_board[i+1][j][1] < fNew:
                        openList.append({"pair": (i+1, j), "f": fNew})
                        ai_board = self.update_ai_board(
                            i+1, j, False, ai_board, fNew, gNew, hNew, i, j)

            # East
            if self.isValid(i, j+1, height, width) == True:
                if self.isDestination((i, j+1), dest) == True:
                    ai_board[i][j+1][4] = i
                    ai_board[i][j+1][5] = j
                    path = self.trace_path(ai_board, dest)
                    # path.append(ai_board)
                    foundDest = True
                    return path

                elif (i, j+1) not in closedList and self.isUnBlocked(ai_board, i, j+1, steps) == True:
                    gNew = ai_board[i][j][2] + 1.0
                    hNew = self.calculateHvalue(i, j+1, dest)
                    fNew = gNew + hNew
                    if ai_board[i][j+1][1] == float('inf') or ai_board[i][j+1][1] < fNew:
                        openList.append({"pair": (i, j+1), "f": fNew})
                        ai_board = self.update_ai_board(
                            i, j+1, False, ai_board, fNew, gNew, hNew, i, j)

            # West
            if self.isValid(i, j-1, height, width) == True:
                if self.isDestination((i, j-1), dest) == True:
                    ai_board[i][j-1][4] = i
                    ai_board[i][j-1][5] = j
                    path = self.trace_path(ai_board, dest)
                    # path.append(ai_board)
                    foundDest = True
                    return path

                elif (i, j-1) not in closedList and self.isUnBlocked(ai_board, i, j-1, steps) == True:
                    gNew = ai_board[i][j][2] + 1.0
                    hNew = self.calculateHvalue(i, j-1, dest)
                    fNew = gNew + hNew
                    if ai_board[i][j-1][1] == float('inf') or ai_board[i][j-1][1] < fNew:
                        openList.append({"pair": (i, j-1), "f": fNew})
                        ai_board = self.update_ai_board(
                            i, j-1, False, ai_board, fNew, gNew, hNew, i, j)

        if foundDest == False:
            print("No path to food found")

        return None

    def get_action(self, next_cell, current_cell):
        if next_cell == (current_cell[0] - 1, current_cell[1]):
            return self.up
        elif next_cell == (current_cell[0] + 1, current_cell[1]):
            return self.down
        elif next_cell == (current_cell[0], current_cell[1] + 1):
            return self.right
        else:
            return self.left

        print("error: no action")
        return None


"""
Set up for board and snake class
self.ai_board = []
        
        inf = float('inf')
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append([0, inf, inf, inf, -1, -1, 0])
            self.ai_board.append(row)
Update walls
self.ai_board[index[0]][index[1]][0] = 1
self.ai_board[index[0]][index[1]][6] = -1

Update snake
def update_with_snake(self, snake):
    for index in np.ndindex(self.height, self.width):
        if self.structure[index[0]][index[1]] == self.snake:
            self.structure[index[0]][index[1]] = None
            self.ai_board[index[0]][index[1]][0] = 0
            self.ai_board[index[0]][index[1]][6] = 0
    self.structure[snake.head_location[0]][snake.head_location[1]] = self.snake
    self.ai_board[snake.head_location[0]][snake.head_location[1]][6] = snake.length
    if snake.length > 1:
        self.structure[snake.tail_location[0]][snake.tail_location[1]] = self.snake
        self.ai_board[snake.tail_location[0]][snake.tail_location[1]][0] = 1
        self.ai_board[snake.tail_location[0]][snake.tail_location[1]][6] = 1
        time = snake.length - 1
        for cell in snake.middle_cells:
            self.structure[cell[0]][cell[1]] = self.snake
            self.ai_board[cell[0]][cell[1]][0] = 1
            self.ai_board[cell[0]][cell[1]][6] = time
            time -= 1
    return True

# Find path in runner
if reachedFood:
    print("food: ", new_board.food_cell)
    path = player.aStarSearch(snake.head_location, new_board.food_cell, new_board.ai_board, new_board.height, new_board.width, snake.length, snake.tail_location)
    if path != None:
        start = path.pop()
    elif new_board.width * recalculating_factor == len(path):
        path = player.aStarSearch(snake.head_location, new_board.food_cell, new_board.ai_board, new_board.height, new_board.width, snake.length, snake.tail_location)
    if path != None:
        start = path.pop()

if path == None or len(path) == 0:
    print("no path found to food waaaah!")
    if len(sorted_dict) == 0:
        start = []
        for i in range(new_board.height):
            for j in range(new_board.width):
                if new_board.ai_board[i][j][0] == 1:
                    start.append((i, j))
        costs_to_obstacles = player.breadthFirstSearch(start, new_board.height, new_board.width)
        sorted_dict = sorted(costs_to_obstacles.items(), key=lambda x: x[1])
    for i in sorted_dict:
        if i[1] != 0:    
            path = player.aStarSearch(snake.head_location, i[0], new_board.ai_board, new_board.height, new_board.width, snake.length, snake.tail_location)
            if path != None:
                sorted_dict.remove(i)
                start = path.pop()
                break

# ai variables
food = 'food'
tail = 'tail'
player = PlayerAI()
recalculating_factor = 0.7
total = new_board.width
if total % 2 != 0:
    total += 0.5
sorted_dict = {}
"""
