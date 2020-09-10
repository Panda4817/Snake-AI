import pygame
import sys
import time

import numpy as np

from snake import *
from snake_ai import *

# Initialise Pygame
pygame.init()
size = width, height = 1750, 750
screen = pygame.display.set_mode(size)

# Initialise board width, height and tile size
tile_size = 10
leftover = 25
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
num_episodes = 3
time_step = eval_env.reset()
policy = saved_policy


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
                # Set up training and evaluating environment
                time_step = eval_env.reset()
                num_episodes = 3
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

        # Check game over
        if eval_env.current_time_step().is_last():
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
            num_episodes -= 1
            if num_episodes > 0:
                time_step = eval_env.reset()
        else:
            action_step = policy.action(time_step)
            time_step = eval_env.step(action_step.action)

    elif tronGame is True:
        pass       

    pygame.display.flip()