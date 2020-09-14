import random
from operator import itemgetter, attrgetter

import numpy as np

from snake import *

class PlayerAI():

    def __init__(self, alpha=1.0, epsilon=0.1):
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon
        self.directions = ['up', 'down', 'left', 'right']

    def convert_board_tuple(self, d):
        t = tuple(tuple(i) for i in d)
        return t
    
    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        o = old_state #self.convert_board_tuple(old_state)
        n = new_state #self.convert_board_tuple(new_state)
        old = self.get_q_value(o, action)
        best_future = self.best_future_reward(n)
        self.update_q_value(o, action, old, reward, best_future)
    
    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        try:
            return self.q[state, action]
        except KeyError:
            return 0
    
    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estimate of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        # Update q value based on function arguments
        self.q[state, action] = old_q + self.alpha * \
            (reward + future_rewards - old_q)
        return True
    
    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        # Find possible actions
        possible_actions = ['up', 'down', 'left', 'right']
        # Create a list to store future rewards
        future_rewards = []
        # Loop over actions
        for action in possible_actions:
            if (state, action) in self.q:
                future_rewards.append(self.q[state, action])
            else:
                future_rewards.append(0)
        # Return the maximum reward from the list
        return max(future_rewards, default=0)
    

    def choose_action_q(self, state, avoid, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        # Get all possible actions from state
        possible_actions = ['up', 'down', 'left', 'right']
        # Get maximum q value for that state
        highest_q = self.best_future_reward(state)
        # Initialise variables to store best action and all actions
        best = []
        all_actions = []
        # For each action, store the action and q value as key-value pairs
        for action in possible_actions:
            if action not in avoid:
                if (state, action) in self.q:
                    all_actions.append(
                        {"action": action, "q": self.q[state, action]})
                    if self.q[state, action] == highest_q:
                        best.append(
                            {"action": action, "q": self.q[state, action]})
                else:
                    all_actions.append({"action": action, "q": 0})
        if len(all_actions) == 0:
            return None
        # Make sure best is not empty
        if len(best) == 0:
            best.extend(all_actions)
        # Check if epsilon is true
        if epsilon:
            choose = ["random", "best"]
            answer = random.choices(
                choose, [self.epsilon, 1 - self.epsilon], k=1)
            if answer[0] == "random":
                a = random.choice(all_actions)
                return a["action"]
        # Or choose best action
        a = random.choice(best)
        return a["action"]
    
    def get_avoid_cells(self, snake, board):
        avoid = []
        if snake.length > 1:
            if snake.direction == 'up':
                avoid.append('down')
            elif snake.direction == 'down':
                avoid.append('up')
            elif snake.direction == 'left':
                avoid.append('right')
            else:
                avoid.append('left')
        if (snake.head_location[0] - 1, snake.head_location[1]) in board.wall_cells or (snake.head_location[0] - 1, snake.head_location[1]) in snake.middle_cells:
            avoid.append('up')
        if (snake.head_location[0] + 1, snake.head_location[1]) in board.wall_cells or (snake.head_location[0] + 1, snake.head_location[1]) in snake.middle_cells:
            avoid.append('down')
        if (snake.head_location[0], snake.head_location[1] - 1) in board.wall_cells or (snake.head_location[0], snake.head_location[1] - 1) in snake.middle_cells:
            avoid.append('left')
        if (snake.head_location[0], snake.head_location[1] + 1) in board.wall_cells or (snake.head_location[0], snake.head_location[1] + 1) in snake.middle_cells:
            avoid.append('right')
        
        return avoid
    
    def get_available_actions(self, avoid):
        a = []
        for i in self.directions:
            if i not in avoid:
                a.append(i)
        return a

    def get_manhattan_distances(self, actions, current_board, snake):
        a_d = []
        for a in actions:
            if a == 'up':
                man = current_board[snake.head_location[0] - 1][snake.head_location[1]] 
            elif a == 'down':
                man = current_board[snake.head_location[0] + 1][snake.head_location[1]]  
            elif a == 'left':
                man = current_board[snake.head_location[0]][snake.head_location[1] - 1] 
            elif a == 'right':
                man = current_board[snake.head_location[0]][snake.head_location[1] + 1]
            
            a_d.append({
                "action": a,
                "man": abs(man[0]) + abs(man[1])
            })
        return a_d
    
    def near_edge_action(self, _next, snake, board):
        for index in np.ndindex(board.height, board.width):
            if _next == 'vertical':
                if index[0] >= 1 and index[0] < int(round(((board.height - 2) / 2), 0)):
                    if snake.head_location == index:
                        return 'down'
                if index[0] <= (board.height - 2) and index[0] >= int(round(((board.height - 2) / 2), 0)):
                    if snake.head_location == index:
                        return 'up'
            elif _next == "horizontal":
                if index[1] >= 1 and index[1] < int(round(((board.width - 2) / 2), 0)):
                    if snake.head_location == index:
                        return 'right'
                if index[1] <= (board.width - 2) and index[1] >= int(round(((board.width - 2) / 2), 0)):
                    if snake.head_location == index:
                        return 'left'
    
    def x_y(self, direction):
        y, x = 0, 0
        if direction == self.directions[0]:
            y = -1
        elif direction == self.directions[1]:
            y = 1
        elif direction == self.directions[2]:
            x = -1
        elif direction == self.directions[3]:
            x = 1
        
        return y, x
    
    def clear_path_check(self, num, snake, direction, board):
        y, x = self.x_y(direction)
        hit = False
        path = 0
        while (path != num):
            path += 1
            index = [snake.head_location[0] + y, snake.head_location[1] + y]
            if tuple(index) in snake.middle_cells or tuple(index) in board.wall_cells:
                hit = True
        
        return hit
                
    def snake_length_low(self, goal, actions, previous_moves, manhattan, snake, board):
        if goal == "food" or snake.length == 1:
            if snake.length > 20:
                for a in actions:
                    if self.clear_path_check(snake.length, snake, a, board) == False:
                        return a
            lowest = sorted(manhattan, key=itemgetter('man'))
            try:
                return lowest[0]["action"]
            except:
                return None
        elif goal == "tail":
            for k, v in previous_moves.items():
                if v > 0:
                    if k == self.directions[0]:
                        if self.directions[1] in actions and self.clear_path_check(v, snake, self.directions[1], board) == False:
                            return self.directions[1]
                        elif self.directions[0] in actions and self.clear_path_check(v, snake, self.directions[0], board) == False:
                            return self.directions[0]
                    elif k == self.directions[1]:
                        if self.directions[0] in actions and self.clear_path_check(v, snake, self.directions[0], board) == False:
                            return self.directions[0]
                        elif self.directions[1] in actions and self.clear_path_check(v, snake, self.directions[1], board) == False:
                            return self.directions[1]
                    elif k == self.directions[2]:
                        if self.directions[3] in actions and self.clear_path_check(v, snake, self.directions[3], board) == False:
                            return self.directions[3]
                        elif self.directions[2] in actions and self.clear_path_check(v, snake, self.directions[2], board) == False:
                            return self.directions[2]
                    elif k == self.directions[3]:
                        if self.directions[2] in actions and self.clear_path_check(v, snake, self.directions[2], board) == False:
                            return self.directions[2]
                        elif self.directions[3] in actions and self.clear_path_check(v, snake, self.directions[3], board) == False:
                            return self.directions[3]
                    continue
            snake.goal_tail = snake.head_location

    
    def choose_action(self, current_cell, current_board, avoid, previous_moves, goal, snake, board):
        actions = self.get_available_actions(avoid) 
        manhattan = self.get_manhattan_distances(actions, current_board, snake)
        if snake.length < board.width and snake.length < board.height:
            return self.snake_length_low(goal, actions, previous_moves, manhattan, snake, board)
        else:
            return None

    """
    def check_for_body(self, directions, snake, board):
        pattern = ['up', 'left', 'down', 'right']
        result3 = []
        for i in directions:
            distance = 0
            x = 0
            y = 0
            if i == 'up':
                y = -1
            elif i == 'left':
                x = -1
            elif i == 'down':
                y = 1
            elif i == 'right':
                x = 1
            l = list(snake.head_location)
            previous_x = -1 if x == 0 else x
            previous_y = -1 if y == 0 else y
            headings = [i]
            turns = 0
            while (tuple(l) not in board.wall_cells):
                l = [l[0] + y, l[1] + x]
                if tuple(l) in snake.middle_cells:
                    if headings == pattern or turns > 3:
                        break
                    if distance == 0:
                        break
                    l = [l[0] - y, l[1] - x]
                    turns += 1
                    if y == -1 or y == 1:
                        y = 0
                        x = 1 if previous_x == -1 else -1
                        previous_x = x
                        headings.append('right' if x == 1 else 'left')
                    elif x == -1 or x == 1:
                        x = 0
                        y = 1 if previous_y == -1 else 1
                        previous_y = y
                        headings.append('up' if y == 1 else 'down')
                else:
                    distance += 1
            result3.append({
                "direction": i,
                "distance": distance,
                "turns": turns
            })
        return result3
 
    def choose_action(self, current_cell, current_board, avoid, previous_moves, snake, board):
        # Current distance
        current = current_cell
        # Directions
        directions = ['up', 'down', 'left', 'right']
        for i in avoid:
            if i in directions:
                directions.remove(i)    
            
        if len(directions) >= 2:    
            if len(previous_moves) == 10:
                if previous_moves.count('up') == 9:
                    try:
                        directions.remove('up')
                    except ValueError:
                        pass
                elif previous_moves.count('down') == 9:
                    try:
                        directions.remove('down')
                    except ValueError:
                        pass
                elif previous_moves.count('left') == 9:
                    try:
                        directions.remove('left')
                    except ValueError:
                        pass
                elif previous_moves.count('right') == 9:
                    try:
                        directions.remove('right')
                    except ValueError:
                        pass

        result = self.check_for_body(directions, snake, board)
        length = len(result)
        
        # Calculate new distances
        for i in range(length):
            if directions[i] == 'up':
                manh = current_board[snake.head_location[0] - 1][snake.head_location[1]] 
            elif directions[i] == 'down':
                manh = current_board[snake.head_location[0] + 1][snake.head_location[1]]  
            elif directions[i] == 'left':
                manh = current_board[snake.head_location[0]][snake.head_location[1] - 1] 
            elif directions[i] == 'right':
                manh = current_board[snake.head_location[0]][snake.head_location[1] + 1]
            
            result[i]["manh"] = abs(manh[0]) + abs(manh[1])
        
        
        other = sorted(result, key=itemgetter('distance'), reverse=True)
        new_o = sorted(other, key=itemgetter('manh'))
        t = sorted(new_o, key=itemgetter('turns'))
        

        if length == 2:
            if t[0]["turns"] != t[1]["turns"]:
                if t[0]["distance"] < 5 and  t[1]["distance"] > 10:
                    print(t)
                    return t[1]["direction"]
                else:
                    print(t)
                    return t[0]["direction"]
            elif new_o[0]["distance"] != new_o[1]["distance"]:
                print(new_o)
                return new_o[0]["direction"]
            else:
                print(other)
                return other[0]["direction"]
            
       
        if length == 3:
            d_count = 0
            turn_count = 0
            for i in range(length):
                for j in range(length):
                    if i != j and t[i]['turns'] != t[j]['turns']:
                        turn_count += 1
                    if i != j and t[i]['distance'] < 10 and t[j]['distance'] >= 40:
                        d_count += 1
            if d_count >= 1:
                print(other)
                return other[0]["direction"]
            elif turn_count > 0:
                print(t)
                return t[0]["direction"]

        
        try:
            print(new_o)
            return new_o[0]['direction']
        except IndexError:
            return None


                        
   
        narrowed = []
        n_dir = []
        for i in range(len(directions)):
            if directions[i] == 'up' and new[i][0] < current_cell[0]:
                narrowed.append({"action": directions[i], "new": new[i], "manh": abs(new[i][0])+ abs(new[i][1])})
                n_dir.append(directions[i])
            elif directions[i] == 'down' and new[i][0] > current_cell[0]:
                narrowed.append({"action": directions[i], "new": new[i], "manh": abs(new[i][0])+ abs(new[i][1])})
                n_dir.append(directions[i])
            elif directions[i] == 'left' and new[i][1] < current_cell[1]:
                narrowed.append({"action": directions[i], "new": new[i], "manh": abs(new[i][0])+ abs(new[i][1])})
                n_dir.append(directions[i])
            elif directions[i] == 'right' and new[i][1] > current_cell[1]:
                narrowed.append({"action": directions[i], "new": new[i], "manh": abs(new[i][0])+ abs(new[i][1])})
                n_dir.append(directions[i])
        
     
        if len(narrowed) > 1:
            e = min(narrowed, key=lambda x: x["manh"])
            print(e)
            return e["action"]
        elif len(narrowed) == 1:
            result = self.check_for_body(directions, snake, board)
            e = max(result, key=lambda x: x["distance"])
            print(e)
            return e["direction"]
        else:
            return None
        """

                
        

    
       