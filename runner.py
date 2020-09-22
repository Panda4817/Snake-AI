import pygame
import sys
import time

import numpy as np

from snake import *
from hamAI import hamiltonian_path, get_action

# Initialise Pygame
pygame.init()
size = width, height = 1220, 820
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

# AI variables
path = hamiltonian_path

# Tron variables
comp_board = Board(h=h, w=w)
computer = Snake()

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
                time.sleep(0.2)
                aiGame = True
                homeScreen = False
            elif tronButton.collidepoint(mouse):
                snake.reset(new_board)
                computer.reset(comp_board, new_board.food_cell)
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
                     'AI plays snake. Human watches.',
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
            gameTitleH = ((j / 5) * height) + titleH + leftover + leftover
            lineRect.center = ((width / 2), gameTitleH)
            screen.blit(lineTitle, lineRect)
            for i, t in enumerate(text['text']):
                line = mediumFont.render(t, True, white)
                lineRect = line.get_rect()
                lineRect.center = ((width / 2), gameTitleH + (i * leftover) + leftover + leftover)
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
                    pygame.draw.rect(screen, white, rect, 1)
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
            eaten = snake.check_food_status(new_board)
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
            snake.move_snake(new_board, eaten)

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
                    if (i, j) == snake.head_location:
                        pygame.draw.rect(screen, blue, rect)
                        pygame.draw.rect(screen, white, rect, 1)
                    else:
                        pygame.draw.rect(screen, red, rect)
                        pygame.draw.rect(screen, white, rect, 1)
                else:
                    pygame.draw.rect(screen, black, rect)
                row.append(rect)
            tiles.append(row)
        
        scoretitle = largeFont.render("AI Score:", True, white)
        scoretitleRect = scoretitle.get_rect()
        scoretitleRect = pygame.Rect((w + 2) * tile_size, 5 * tile_size, (leftover * 10), titleH)
        screen.blit(scoretitle, scoretitleRect)
        score = largeFont.render(str(snake.food_count), True, white)
        scoreRect = score.get_rect()
        scoreRect = pygame.Rect((w + 2) * tile_size, 10 * tile_size, (leftover * 10), titleH)
        screen.blit(score, scoreRect)

        lengthtitle = largeFont.render("AI Length:", True, white)
        lengthtitleRect = lengthtitle.get_rect()
        lengthtitleRect = pygame.Rect((w + 2) * tile_size, 15 * tile_size, (leftover * 10), titleH)
        screen.blit(lengthtitle, lengthtitleRect)
        length = largeFont.render(str(snake.length), True, white)
        lengthRect = length.get_rect()
        lengthRect = pygame.Rect((w + 2) * tile_size, 20 * tile_size, (leftover * 10), titleH)
        screen.blit(length, lengthRect)
        
        
        if snake.check_game_status(new_board) or new_board.food_cell == None:
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
            eaten = snake.check_food_status(new_board)
            if snake.head_location[1] == 2 and new_board.food_cell[0] < snake.head_location[0] and (snake.head_location[0], snake.head_location[1] - 1) not in snake.middle_cells and (snake.head_location[0] - 1, snake.head_location[1] - 1) not in snake.middle_cells:
                action = get_action((snake.head_location[0], snake.head_location[1] - 1), snake.head_location)
            elif snake.head_location[1] == new_board.width - 2 and new_board.food_cell[0] > snake.head_location[0] and new_board.food_cell[0] % 2 == 0 and (snake.head_location[0] + 1, snake.head_location[1]) not in snake.middle_cells and (snake.head_location[0] + 1, snake.head_location[1] - 1) not in snake.middle_cells and (snake.head_location[0] + 2, snake.head_location[1]) not in snake.middle_cells and snake.length < (((new_board.height - 2) * (new_board.width - 2)) / 2):
                action = get_action((snake.head_location[0] + 1, snake.head_location[1]), snake.head_location)
            elif snake.head_location[1] == 2 and new_board.food_cell[0] > snake.head_location[0] and new_board.food_cell[0] % 2 != 0 and (snake.head_location[0] + 1, snake.head_location[1]) not in snake.middle_cells and (snake.head_location[0] + 1, snake.head_location[1] + 1) not in snake.middle_cells and (snake.head_location[0] + 2, snake.head_location[1]) not in snake.middle_cells and snake.length < (((new_board.height - 2) * (new_board.width - 2)) / 2):
                action = get_action((snake.head_location[0] + 1, snake.head_location[1]), snake.head_location)
            else:
                head_index = path.index(snake.head_location)
                action = get_action(path[head_index + 1], snake.head_location)
            
            snake.direction = action
            snake.move_snake(new_board, eaten)
            action = None
       
    elif tronGame is True:
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
                    pygame.draw.rect(screen, blue, rect)
                    pygame.draw.rect(screen, white, rect, 1)
                elif comp_board.structure[i][j] == comp_board.snake:
                    pygame.draw.rect(screen, yellow, rect)
                    pygame.draw.rect(screen, red, rect, 1)
                else:
                    pygame.draw.rect(screen, black, rect)
                row.append(rect)
            tiles.append(row)

        aiscoretitle = mediumFont.render("AI Score:", True, white)
        aiscoretitleRect = aiscoretitle.get_rect()
        aiscoretitleRect = pygame.Rect((w + 2) * tile_size, 15 * tile_size, (leftover * 10), titleH)
        screen.blit(aiscoretitle, aiscoretitleRect)
        aiscore = largeFont.render(str(computer.food_count), True, white)
        aiscoreRect = aiscore.get_rect()
        aiscoreRect = pygame.Rect((w + 2) * tile_size, 20 * tile_size, (leftover * 10), titleH)
        screen.blit(aiscore, aiscoreRect)

        hscoretitle = mediumFont.render("Human Score:", True, white)
        hscoretitleRect = hscoretitle.get_rect()
        hscoretitleRect = pygame.Rect((w + 2) * tile_size, 5 * tile_size, (leftover * 10), titleH)
        screen.blit(hscoretitle, hscoretitleRect)
        hscore = largeFont.render(str(snake.food_count), True, white)
        hscoreRect = hscore.get_rect()
        hscoreRect = pygame.Rect((w + 2) * tile_size, 10 * tile_size, (leftover * 10), titleH)
        screen.blit(hscore, hscoreRect)

        if snake.check_game_status(new_board, computer):
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
                    tronGame = False
                    homeScreen = True
        else:
            # ai
            eaten = computer.check_food_status(comp_board, new_board)
            new_board.food_cell = comp_board.food_cell
            if computer.head_location[1] == 2 and comp_board.food_cell[0] < computer.head_location[0] and (computer.head_location[0], computer.head_location[1] - 1) not in computer.middle_cells and (computer.head_location[0] - 1, computer.head_location[1] - 1) not in computer.middle_cells:
                action = get_action((computer.head_location[0], computer.head_location[1] - 1), computer.head_location)
            elif computer.head_location[1] == comp_board.width - 2 and comp_board.food_cell[0] > computer.head_location[0] and comp_board.food_cell[0] % 2 == 0 and (computer.head_location[0] + 1, computer.head_location[1]) not in computer.middle_cells and (computer.head_location[0] + 1, computer.head_location[1] - 1) not in computer.middle_cells and (computer.head_location[0] + 2, computer.head_location[1]) not in computer.middle_cells and computer.length < (((comp_board.height - 2) * (comp_board.width - 2)) / 2):
                action = get_action((computer.head_location[0] + 1, computer.head_location[1]), computer.head_location)
            elif computer.head_location[1] == 2 and comp_board.food_cell[0] > computer.head_location[0] and comp_board.food_cell[0] % 2 != 0 and (computer.head_location[0] + 1, computer.head_location[1]) not in computer.middle_cells and (computer.head_location[0] + 1, computer.head_location[1] + 1) not in computer.middle_cells and (computer.head_location[0] + 2, computer.head_location[1]) not in computer.middle_cells and computer.length < (((comp_board.height - 2) * (comp_board.width - 2)) / 2):
                action = get_action((computer.head_location[0] + 1, computer.head_location[1]), computer.head_location)
            else:
                head_index = path.index(computer.head_location)
                action = get_action(path[head_index + 1], computer.head_location)
            
            computer.direction = action
            computer.move_snake(comp_board, eaten)
            action = None

            # human
            eaten = snake.check_food_status(new_board, comp_board)
            comp_board.food_cell = new_board.food_cell
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
            snake.move_snake(new_board, eaten)
            


    pygame.display.flip()