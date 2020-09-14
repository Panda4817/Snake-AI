import random
import math
from copy import deepcopy
from operator import itemgetter, attrgetter

import numpy as np

from snake import *

class PlayerAI():

    def __init__(self):
        self.up = 'up'
        self.down = 'down'
        self.left = 'left'
        self.right = 'right'
    
    def isValid(self, row, col, height, width):
        return (row >= 0) and (row < height) and (col >= 0) and (col < width)

    def isUnBlocked(self, copied_board, row, col):
        if copied_board[row][col][0] == 0:
            return True
        else:
            return False
    
    def isDestination(self, src, dest):
        if src == dest:
            return True
        else:
            return False
    
    def calculateHvalue(self, row, col, dest):
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

    
    def aStarSearch(self, src, dest, board, height, width):
        ai_board = deepcopy(board)
        if self.isValid(src[0], src[1], height, width) == False:
            print("Snake starting cell is NOT valid")
            return
        
        if self.isValid(dest[0], dest[1], height, width) == False:
            print("Destintion is NOT valid")
            return
        
        if self.isUnBlocked(ai_board, src[0], src[1]) == False or self.isUnBlocked(ai_board, dest[0], dest[1]) == False:
            print("Either source or destination is blocked")
            return

        if self.isDestination(src, dest) == True:
            print("We are already at the destination")
            return
        
        self.update_ai_board(src[0], src[1], False, ai_board, 0.0, 0.0, 0.0, src[0], src[1])

        closedList = []
        openList = [{"pair": src, "f": 0}]

        foundDest = False

        while (len(openList) > 0):
            p = openList.pop(0)
            
            closedList.append((p["pair"]))

            i = p["pair"][0]
            j = p["pair"][1]

            # Cell-->Popped Cell (i, j) 
            # N -->  North       (i-1, j) 
            # S -->  South       (i+1, j) 
            # E -->  East        (i, j+1) 
            # W -->  West           (i, j-1) 

            gNew, hNew, fNew = 0, 0, 0
            
            # North
            if self.isValid(i-1, j, height, width) == True:
                if self.isDestination((i-1, j), dest) == True:
                    ai_board[i-1][j][4] = i
                    ai_board[i-1][j][5] = j
                    path = self.trace_path(ai_board, dest)
                    path.append(ai_board)
                    foundDest = True
                    return path
                
                elif (i-1, j) not in closedList and self.isUnBlocked(ai_board, i-1, j) == True:
                    gNew = ai_board[i][j][2] + 1.0
                    hNew = self.calculateHvalue(i-1, j, dest)
                    fNew = gNew + hNew
                    
                    if ai_board[i-1][j][1] == float('inf') or ai_board[i-1][j][1] > fNew:
                        openList.append({"pair": (i-1, j), "f": fNew})
                        ai_board = self.update_ai_board(i-1, j, False, ai_board, fNew, gNew, hNew, i, j)

            # South
            if self.isValid(i+1, j, height, width) == True:
                if self.isDestination((i+1, j), dest) == True:
                    ai_board[i+1][j][4] = i
                    ai_board[i+1][j][5] = j
                    path = self.trace_path(ai_board, dest)
                    path.append(ai_board)
                    foundDest = True
                    return path
                
                elif (i+1, j) not in closedList and self.isUnBlocked(ai_board, i+1, j) == True:
                    gNew = ai_board[i][j][2] + 1.0
                    hNew = self.calculateHvalue(i+1, j, dest)
                    fNew = gNew + hNew
                    
                    if ai_board[i+1][j][1] == float('inf') or ai_board[i+1][j][1] > fNew:
                        openList.append({"pair": (i+1, j), "f": fNew})
                        ai_board = self.update_ai_board(i+1, j, False, ai_board, fNew, gNew, hNew, i, j)
            # East
            if self.isValid(i, j+1, height, width) == True:
                if self.isDestination((i, j+1), dest) == True:
                    ai_board[i][j+1][4] = i
                    ai_board[i][j+1][5] = j
                    path = self.trace_path(ai_board, dest)
                    path.append(ai_board)
                    foundDest = True
                    return path
                
                elif (i, j+1) not in closedList and self.isUnBlocked(ai_board, i, j+1) == True:
                    gNew = ai_board[i][j][2] + 1.0
                    hNew = self.calculateHvalue(i, j+1, dest)
                    fNew = gNew + hNew
                    
                    if ai_board[i][j+1][1] == float('inf') or ai_board[i][j+1][1] > fNew:
                        openList.append({"pair": (i, j+1), "f": fNew})
                        ai_board = self.update_ai_board(i, j+1, False, ai_board, fNew, gNew, hNew, i, j)
            # West
            if self.isValid(i, j-1, height, width) == True:
                if self.isDestination((i, j-1), dest) == True:
                    ai_board[i][j-1][4] = i
                    ai_board[i][j-1][5] = j
                    path = self.trace_path(ai_board, dest)
                    path.append(ai_board)
                    foundDest = True
                    return path
                
                elif (i, j-1) not in closedList and self.isUnBlocked(ai_board, i, j-1) == True:
                    gNew = ai_board[i][j][2] + 1.0
                    hNew = self.calculateHvalue(i, j-1, dest)
                    fNew = gNew + hNew
                    
                    if ai_board[i][j-1][1] == float('inf') or ai_board[i][j-1][1] > fNew:
                        openList.append({"pair": (i, j-1), "f": fNew})
                        ai_board = self.update_ai_board(i, j-1, False, ai_board, fNew, gNew, hNew, i, j)
        
        if foundDest == False:
            print("No path found")
        
        return

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





