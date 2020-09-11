import random

from snake import *

class PlayerAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def convert_board_tuple(self, d):
        t = tuple(tuple(i) for i in d)
        return t
    
    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        o = self.convert_board_tuple(old_state)
        n = self.convert_board_tuple(new_state)
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
            if (state, action) in self.q:
                all_actions.append(
                    {"action": action, "q": self.q[state, action]})
                if self.q[state, action] == highest_q:
                    best.append(
                        {"action": action, "q": self.q[state, action]})
            else:
                all_actions.append({"action": action, "q": 0})
        # Make sure best is not empty
        if len(best) == 0:
            best.extend(all_actions)
        # Check if epsilon is true
        if epsilon:
            choose = ["random", "best"]
            answer = random.choices(
                choose, [self.epsilon, 1 - self.epsilon], k=1)
            if answer[0] == "random":
                a = None
                while(a is None or a["action"] in avoid):
                    a = random.choice(all_actions)
                return a["action"]
        # Or choose best action
        a = None
        while(a is None or a["action"] in avoid):
            a = random.choice(best)
        return a["action"]

    def remove_wall_snake(self, lst, directions):
        removed = []
        while(11251 in lst):
            i = lst.index(11251)
            lst.remove(11251)
            removed.append(directions.pop(i))
        return [lst, directions, removed]
    
    def remove_max(self, lst, directions, current):
        while(max(lst) == current or max(lst) > current):
            m = max(lst)
            i = lst.index(m)
            lst.remove(m)
            directions.pop(i)
            if len(lst) == 0:
                break
        return [lst, directions]
    
    def order_directions(self, current_cell, current_board, snake, board):
        d = ['up', 'down', 'left', 'right']
        directions = []
        x = snake.head_location[1] - board.food_cell[1]
        if x != abs(x):
            dx = d[3]
            otherx = d[2]
        else:
            dx = d[2]
            otherx = d[3]
        y = snake.head_location[0] - board.food_cell[0]
        if y != abs(y):
            dy = d[0]
            othery = d[1]
        else:
            dy = d[1]
            othery = d[0]
        yNum = 0
        xNum = 0
        for i in range(snake.head_location[0], board.food_cell[0] + 1):
            if current_board[i][snake.head_location[1]] == 11251:
                yNum += 1
        for i in range(snake.head_location[1], board.food_cell[1] + 1):
            if current_board[snake.head_location[0]][i] == 11251:
                xNum += 1
        
        if yNum > xNum:
            directions.extend([dx, otherx, othery, dy])
        else:
            directions.extend([dy, othery, otherx, dx])
        return directions

    def choose_action(self, current_cell, current_board, snake, board):
        # Current distance
        current = current_cell
        # List to store new distances
        new = []
        # Directions
        directions = self.order_directions(current_cell, current_board, snake, board)
        
        # Calculate new distances
        tup = list(snake.head_location)
        tup[0] -= 1
        up = current_board[tup[0]][tup[1]]
        
        tdown = list(snake.head_location)
        tdown[0] += 1
        down = current_board[tdown[0]][tdown[1]]
        
        tleft = list(snake.head_location)
        tleft[1] -= 1
        left = current_board[tleft[0]][tleft[1]]
        
        tright = list(snake.head_location)
        tright[1] += 1
        right = current_board[tright[0]][tright[1]]

        for i in directions:
            if i == 'up':
                new.append(up)
            elif i == 'down':
                new.append(down)
            elif i == 'left':
                new.append(left)
            else:
                new.append(right)

        n = new.copy()
        dr = directions.copy()
        # Eliminate moves that are not possible when snake length is higher than 1
        if snake.length > 1:
            for i in range(4):
                if snake.direction == 'up':
                    if directions[i] == 'down':
                        new.pop(i)
                        directions.pop(i)
                        break
                if snake.direction == 'down':
                    if directions[i] == 'up':
                        new.pop(i)
                        directions.pop(i)
                        break
                if snake.direction == 'left':
                    if directions[i] == 'right':
                        new.pop(i)
                        directions.pop(i)
                        break
                if snake.direction == 'right':
                    if directions[i] == 'left':
                        new.pop(i)
                        directions.pop(i)
                        break

        # Eliminate worse distances
        new_l_d = self.remove_wall_snake(new, directions)
        print("no walls ", new_l_d)
        if len(new_l_d[0]) == 1:
            return new_l_d[0][0]
        new2_l_d = self.remove_max(new_l_d[0], new_l_d[1], current)
        print("no bigger ", new2_l_d)
        if len(new2_l_d[0]) == 0:
            new_l_d = self.remove_wall_snake(n, dr)
            x = random.randint(0, len(new_l_d[0]) - 1)
            return new_l_d[1][x]
        
        # Return direction with the least distance
        x = new2_l_d[0].index(min(new2_l_d[0]), 0, len(new2_l_d[0]))
        return new2_l_d[1][x]