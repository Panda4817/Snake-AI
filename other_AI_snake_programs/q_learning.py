import random
from operator import itemgetter, attrgetter

import numpy as np

from snake import *

# A class to work out Q values for each state


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
        o = old_state  # self.convert_board_tuple(old_state)
        n = new_state  # self.convert_board_tuple(new_state)
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

    """The following functions are a different implementation of AI snake which was used with q-learning."""

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
                man = current_board[snake.head_location[0] -
                                    1][snake.head_location[1]]
            elif a == 'down':
                man = current_board[snake.head_location[0] +
                                    1][snake.head_location[1]]
            elif a == 'left':
                man = current_board[snake.head_location[0]
                                    ][snake.head_location[1] - 1]
            elif a == 'right':
                man = current_board[snake.head_location[0]
                                    ][snake.head_location[1] + 1]

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
