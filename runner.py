import pygame
import sys
import time

import numpy as np

from snake import *
from AIPlayer import *

# Initialise Pygame
pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)

# Initialise board width, height and tile size
tile_size = 10
leftover = 20
h = int(height / tile_size)
w = int((width - (leftover * tile_size)) / tile_size)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Fonts
largeFont = pygame.font.Font("OpenSans-Regular.ttf", int(round(width * 0.023, 0)))
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", int(round(width * 0.016, 0)))
smallFont = pygame.font.Font("OpenSans-Regular.ttf", int(round(width * 0.01, 0)))

# Initialise variables to track height of title and buttons
titleH = 50

# Game mode variables
humanGame = False
aiGame = False
tronGame = False
instructions = False
homeScreen = True

# Setup board and snake objects for human game
new_board = Board(h=h, w=w)
snake = Snake()

# ai variables
food = 'food'
tail = 'tail'
player = PlayerAI()
goal = food

"""
current_board = None
action = None
next_board = None
current_cell = None
next_cell = None
previous_moves = {}
goal = food
up_down = ['up', 'down']
left_right = ['left', 'right']
"""
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
    screen.fill(black)

    # Common buttons
    backButton = pygame.Rect((width / 4), (4 / 5) * height, width / 2, titleH)
    back = mediumFont.render("Back", True, black)
    backRect = back.get_rect()
    backRect.center = backButton.center

    if homeScreen is True:

        # Draw title
        title = largeFont.render("Play Snake", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), titleH)
        screen.blit(title, titleRect)

        # Draw buttons
        humanButton = pygame.Rect((width / 4), (1 / 5) * height, width / 2, titleH)
        human = mediumFont.render("Human plays Snake", True, black)
        humanRect = human.get_rect()
        humanRect.center = humanButton.center
        
        aiButton = pygame.Rect((width / 4), (2 / 5) * height, width / 2, titleH)
        ai = mediumFont.render("AI plays Snake", True, black)
        aiRect = ai.get_rect()
        aiRect.center = aiButton.center

        tronButton = pygame.Rect((width / 4), (3 / 5) * height, width / 2, titleH)
        tron = mediumFont.render("Tron Snake", True, black)
        tronRect = tron.get_rect()
        tronRect.center = tronButton.center

        howToPlayButton = pygame.Rect((width / 4), (4 / 5) * height, width / 2, titleH)
        howToPlay = mediumFont.render("How to play", True, black)
        howToPlayRect = howToPlay.get_rect()
        howToPlayRect.center = howToPlayButton.center
        
        pygame.draw.rect(screen, white, humanButton)
        screen.blit(human, humanRect)
        pygame.draw.rect(screen, white, aiButton)
        screen.blit(ai, aiRect)
        pygame.draw.rect(screen, white, tronButton)
        screen.blit(tron, tronRect)
        pygame.draw.rect(screen, white, howToPlayButton)
        screen.blit(howToPlay, howToPlayRect)

        # Check if button is clicked
        click, _, _= pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if humanButton.collidepoint(mouse):
                # setup human snake
                snake.reset(new_board)
                time.sleep(0.2)
                humanGame = True
                homeScreen = False
            elif aiButton.collidepoint(mouse):
                snake.reset(new_board)
                path = player.aStarSearch(snake.head_location, new_board.food_cell, new_board.ai_board, new_board.height, new_board.width)
                updated_ai_board = path.pop()
                start = path.pop()
                for (row, col) in path:
                    if (row, col) == new_board.food_cell or (row, col) == snake.goal_tail:
                        updated_ai_board = player.update_ai_board(row, col, False, updated_ai_board, float('inf'), float('inf'), float('inf'), -1, -1)
                    else:
                        updated_ai_board = player.update_ai_board(row, col, True, updated_ai_board, float('inf'), float('inf'), float('inf'), -1, -1)
                for i in range(new_board.height):
                    for j in range(new_board.width):
                        updated_ai_board[i][j][1] = float('inf')
                        updated_ai_board[i][j][2] = float('inf')
                        updated_ai_board[i][j][3] = float('inf')
                        updated_ai_board[i][j][4] = -1
                        updated_ai_board[i][j][5] = -1
                
                goal = food
                time.sleep(0.2)
                aiGame = True
                homeScreen = False
            elif tronButton.collidepoint(mouse):
                time.sleep(0.2)
                tronGame = True
                homeScreen = False
            elif howToPlayButton.collidepoint(mouse):
                time.sleep(0.2)
                instructions = True
                homeScreen = False
    
    elif instructions is True:

        # Draw title
        title = largeFont.render("How to play", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), titleH - leftover)
        screen.blit(title, titleRect)

        # Draw instructions
        texts = [
            {
                "gameTitle": 'Human plays Snake',
                "text": [
                    'Use arrow keys to control the snake: red squares.',
                    'Eat the food: green squares.',
                    'Avoid the edge and your own body.'
                ]
            },
            {
                "gameTitle": 'AI plays Snake',
                "text": [
                     'AI trains and then plays snake. Human watches.',
                ]
            },
            {
                "gameTitle": 'Tron Snake',
                "text": [
                    'Human: blue snake vs AI: yellow snake.',
                    'Avoid AI snake, your own body and walls.',
                    'Eat the food: green squares.'
                ]
            }    
        ]

        for j, text in enumerate(texts):
            lineTitle = mediumFont.render(text['gameTitle'], True, green)
            lineRect = lineTitle.get_rect()
            gameTitleH = ((j / 5) * height) + titleH + leftover
            lineRect.center = ((width / 2), gameTitleH)
            screen.blit(lineTitle, lineRect)
            for i, t in enumerate(text['text']):
                line = smallFont.render(t, True, white)
                lineRect = line.get_rect()
                lineRect.center = ((width / 2), gameTitleH + (i * leftover) + leftover)
                screen.blit(line, lineRect)

        # Draw buttons
        pygame.draw.rect(screen, white, backButton)
        screen.blit(back, backRect)

        # Check if button is clicked
        click, _, _= pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if backButton.collidepoint(mouse):
                instructions = False
                homeScreen = True
                time.sleep(0.2)

    elif humanGame is True:
        # Draw board and score
        tiles = []
        for i in range(new_board.height):
            row = []
            for j in range(new_board.width):
                rect = pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
                if (i, j) in new_board.wall_cells:
                    pygame.draw.rect(screen, white, rect)
                elif (i, j) == new_board.food_cell:
                    pygame.draw.rect(screen, green, rect)
                elif new_board.structure[i][j] == new_board.snake:
                    pygame.draw.rect(screen, red, rect)
                else:
                    pygame.draw.rect(screen, black, rect)
                row.append(rect)
            tiles.append(row)
        
        scoretitle = largeFont.render("Score:", True, white)
        scoretitleRect = scoretitle.get_rect()
        scoretitleRect = pygame.Rect((w + 5) * tile_size, 5 * tile_size, (leftover * 10), titleH)
        screen.blit(scoretitle, scoretitleRect)
        score = largeFont.render(str(snake.food_count), True, white)
        scoreRect = score.get_rect()
        scoreRect = pygame.Rect((w + 5) * tile_size, 10 * tile_size, (leftover * 10), titleH)
        screen.blit(score, scoreRect)
        
        # Check game over
        if snake.check_game_status(new_board):
            # Show game over title
            game_over = largeFont.render("Game Over", True, white)
            goRect = game_over.get_rect()
            goRect.center = ((width / 3), titleH)
            screen.blit(game_over, goRect)
            # Draw back button
            pygame.draw.rect(screen, white, backButton)
            screen.blit(back, backRect)
            
            # Check if button is clicked
            click, _, _= pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if backButton.collidepoint(mouse):
                    humanGame = False
                    homeScreen = True
        else:
            # check if snake is in food tile, if so increase snake length and score, place food in random place
            snake.check_food_status(new_board)
            # check if key pressed, if so change direction variable
            key_states = pygame.key.get_pressed()
            if snake.length == 1:
                if key_states[pygame.K_UP]:
                    snake.direction = snake.up
                if key_states[pygame.K_DOWN]:
                    snake.direction = snake.down
                if key_states[pygame.K_RIGHT]:
                    snake.direction = snake.right
                if key_states[pygame.K_LEFT]:
                    snake.direction = snake.left
            else:
                if key_states[pygame.K_UP] and snake.direction != snake.down:
                    snake.direction = snake.up
                elif key_states[pygame.K_DOWN] and snake.direction != snake.up:
                    snake.direction = snake.down
                elif key_states[pygame.K_RIGHT] and snake.direction != snake.left:
                    snake.direction = snake.right
                elif key_states[pygame.K_LEFT] and snake.direction != snake.right:
                    snake.direction = snake.left
            # snake moves 1 square in given direction
            snake.move_snake(new_board)

    elif aiGame is True:
        # Draw board and score
        tiles = []
        for i in range(new_board.height):
            row = []
            for j in range(new_board.width):
                rect = pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
                if (i, j) in new_board.wall_cells:
                    pygame.draw.rect(screen, white, rect)
                elif (i, j) == new_board.food_cell:
                    pygame.draw.rect(screen, green, rect)
                elif new_board.structure[i][j] == new_board.snake:
                    pygame.draw.rect(screen, red, rect)
                else:
                    pygame.draw.rect(screen, black, rect)
                row.append(rect)
            tiles.append(row)
        
        scoretitle = largeFont.render("AI Score:", True, white)
        scoretitleRect = scoretitle.get_rect()
        scoretitleRect = pygame.Rect((w + 5) * tile_size, 5 * tile_size, (leftover * 10), titleH)
        screen.blit(scoretitle, scoretitleRect)
        score = largeFont.render(str(snake.food_count), True, white)
        scoreRect = score.get_rect()
        scoreRect = pygame.Rect((w + 5) * tile_size, 10 * tile_size, (leftover * 10), titleH)
        screen.blit(score, scoreRect)
        
        
        if snake.check_game_status(new_board):
            #player.update(current_cell, action, next_cell, -1)
            # Show game over title
            game_over = largeFont.render("Game Over", True, white)
            goRect = game_over.get_rect()
            goRect.center = ((width / 3), titleH)
            screen.blit(game_over, goRect)
            # Draw back button
            pygame.draw.rect(screen, white, backButton)
            screen.blit(back, backRect)
            
            # Check if button is clicked
            click, _, _= pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if backButton.collidepoint(mouse):
                    aiGame = False
                    homeScreen = True
        else:
            count = 0
            for i in range(new_board.height):
                for j in range(new_board.width):
                    if updated_ai_board[i][j][0] == 1:
                        count += 1
            print(count)
            reachedFood = snake.check_food_status(new_board)    
            if snake.length > 1:
                if reachedFood:
                    goal = tail
                    print(goal)
                    print(snake.goal_tail)
                    updated_ai_board[snake.head_location[0]][snake.head_location[1]][0] = 0
                    updated_ai_board[snake.goal_tail[0]][snake.goal_tail[1]][0] = 0
                    path = player.aStarSearch(snake.head_location, snake.goal_tail, updated_ai_board, new_board.height, new_board.width)
                    path.pop()
                    start = path.pop()
                    if start != snake.head_location:
                        print("error: start != head_location snake is more than 1")
                        break
                
                
                if snake.update_goal_tail():
                    goal = food
                    print(goal)
                    print(new_board.food_cell)
                    path = player.aStarSearch(snake.head_location, new_board.food_cell, new_board.ai_board, new_board.height, new_board.width)
                    updated_ai_board = path.pop()
                    start = path.pop()
                    for (row, col) in path:
                        if (row, col) == new_board.food_cell or (row, col) == snake.goal_tail:
                            updated_ai_board = player.update_ai_board(row, col, False, updated_ai_board, float('inf'), float('inf'), float('inf'), -1, -1)
                        else:
                            updated_ai_board = player.update_ai_board(row, col, True, updated_ai_board, float('inf'), float('inf'), float('inf'), -1, -1)
                    for i in range(new_board.height):
                        for j in range(new_board.width):
                            updated_ai_board[i][j][1] = float('inf')
                            updated_ai_board[i][j][2] = float('inf')
                            updated_ai_board[i][j][3] = float('inf')
                            updated_ai_board[i][j][4] = -1
                            updated_ai_board[i][j][5] = -1
                    
                    if  start != snake.head_location:
                        print("error: start does not equal head_location snake is 1")
                        break
                
            
                
            """
                if len(previous_moves) == 1:
                    if up_down[0] in previous_moves or up_down[1] in previous_moves:
                        add_move = player.near_edge_action("horizontal", snake, new_board)
                    elif left_right[0] in previous_moves or left_right[1] in previous_moves:
                        add_move = player.near_edge_action("vertical", snake, new_board)
                    for k, v in previous_moves.items():
                        val = v
                        key = k
                    previous_moves.clear()
                    previous_moves.update({add_move: val, key: val})
                
                moves = len(previous_moves)
                total = sum(previous_moves.values())
                if total < snake.length:
                    while (int(sum(previous_moves.values()) > snake.length)):
                        for k, v in previous_moves.items():
                            v += 1

               
                print(goal)
                player.update(current_cell, action, next_cell, 0.7)
            elif current_cell != None and next_cell != None:
                if action == 'up' and next_cell[0] > current_cell[0]:
                    player.update(current_cell, action, next_cell, -0.2)
                elif action == 'down' and next_cell[0] < current_cell[0]:
                    player.update(current_cell, action, next_cell, -0.2)
                elif action == 'left' and next_cell[1] > current_cell[1]:
                    player.update(current_cell, action, next_cell, -0.2)
                elif action == 'right' and next_cell[1] < current_cell[1]:
                    player.update(current_cell, action, next_cell, -0.2)
                else:
                    player.update(current_cell, action, next_cell, 0.1)
            
            current_board = new_board.convert_to_distances_to_food(snake)
            current_cell = current_board[snake.head_location[0]][snake.head_location[1]]
            avoid = player.get_avoid_cells(snake, new_board)
            action = player.choose_action(current_cell, current_board, avoid, previous_moves, goal, snake, new_board)
            # action = player.choose_action_q(current_cell, avoid)
            if action != None:
                if goal == food:
                    if action != snake.direction:
                        previous_moves[action] = 1
                    else:
                        previous_moves[action] += 1
                elif goal == tail:
                    if action == up_down[0]:
                        try:
                            previous_moves[up_down[1]] -= 1
                        except KeyError:
                            previous_moves[up_down[0]] -= 1
                    elif action == up_down[1]:
                        try:
                            previous_moves[up_down[0]] -= 1
                        except KeyError:
                            previous_moves[up_down[1]] -= 1
                    elif action == left_right[0]:
                        try:
                            previous_moves[left_right[1]] -= 1
                        except KeyError:
                            previous_moves[left_right[0]] -= 1
                    elif action == left_right[1]:
                        try:
                            previous_moves[left_right[0]] -= 1
                        except KeyError:
                            previous_moves[left_right[1]] -= 1
                """
            if len(path) == 0:
                print("error: path length == 0")
                break
            
            action = player.get_action(path.pop(), snake.head_location)
            if action == None:
                print("error: action is None")
                break
            snake.direction = action
            snake.move_snake(new_board)
            print('current place ', snake.head_location)
            """
            next_board = new_board.convert_to_distances_to_food(snake)
            next_cell = next_board[snake.head_location[0]][snake.head_location[1]]
            """
       
    elif tronGame is True:
        pass       

    pygame.display.flip()