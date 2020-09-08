import pygame
import sys
import time

from snake import *

# Initialise Pygame
pygame.init()
size = width, height = 1750, 750
screen = pygame.display.set_mode(size)


# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Fonts
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
smallFont = pygame.font.Font("OpenSans-Regular.ttf", 18)

# Game mode variables
humanGame = False
aiGame = False
tronGame = False
instructions = False
homeScreen = True


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
    screen.fill(black)

    # Common buttons
    humanButton = pygame.Rect((width / 4), (1 / 5) * height, width / 2, 50)
    human = mediumFont.render("Human plays Snake", True, black)
    humanRect = human.get_rect()
    humanRect.center = humanButton.center
    
    aiButton = pygame.Rect((width / 4), (2 / 5) * height, width / 2, 50)
    ai = mediumFont.render("AI plays Snake", True, black)
    aiRect = ai.get_rect()
    aiRect.center = aiButton.center

    tronButton = pygame.Rect((width / 4), (3 / 5) * height, width / 2, 50)
    tron = mediumFont.render("Tron Snake", True, black)
    tronRect = tron.get_rect()
    tronRect.center = tronButton.center

    howToPlayButton = pygame.Rect((width / 4), (4 / 5) * height, width / 2, 50)
    howToPlay = mediumFont.render("How to play", True, black)
    howToPlayRect = howToPlay.get_rect()
    howToPlayRect.center = howToPlayButton.center
    
    backButton = pygame.Rect((width / 4), (4 / 5) * height, width / 2, 50)
    back = mediumFont.render("Back", True, black)
    backRect = back.get_rect()
    backRect.center = backButton.center

    if homeScreen is True:
        # Setup board
        new_board = Board()
        new_board.setup()
        new_board.place_food()
        

        # Draw title
        title = largeFont.render("Play Snake", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        
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
                snake = Snake()
                snake.setup(new_board)
                time.sleep(0.2)
                humanGame = True
                homeScreen = False
            elif aiButton.collidepoint(mouse):
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
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw instructions
        texts = [
            'Use arrow keys to control the snake: red squares.',
            'Eat the food: green squares.',
            'Avoid the edge and your own body.',
            'AI trains and then plays snake. Human watches.',
            'Human: blue snake vs AI: yellow snake.',
            'Avoid AI snake, your own body and walls.',
            'Eat the food: green squares.'
        ]
        gameTitles = [
            'Human plays Snake',
            'AI plays Snake',
            'Tron Snake'
        ]
        for i, gameTitle in enumerate(gameTitles):
            line = mediumFont.render(gameTitle, True, green)
            lineRect = line.get_rect()
            # lineRect = pygame.Rect((width / 4), ((i) / 4) * height + 70, width / 2, 10)
            lineRect.center = ((width / 2), ((i) / 4) * height + 100)
            screen.blit(line, lineRect)
        for i, text in enumerate(texts):
            line = smallFont.render(text, True, white)
            lineRect = line.get_rect()
            if i >= 0 and i <= 2:
                # lineRect = pygame.Rect((width / 4), ((i + 10) / 100) * height + 20 * (i + 2), width / 2, 10)
                lineRect.center = ((width / 2), ((i + 10) / 100) * height + 25 * (i + 2))
            elif i == 3:
                # lineRect = pygame.Rect((width / 4), ((i + 30) / 100) * height + 20 * i, width / 2, 10)
                lineRect.center = ((width / 2), ((i + 30) / 100) * height + 25 * i)
            elif i > 3:
                # lineRect = pygame.Rect((width / 4), ((i + 50) / 100) * height + 20 * i, width / 2, 10)
                lineRect.center = ((width / 2), ((i + 50) / 100) * height + 25 * i)
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
        tile_size = 10
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
        scoretitleRect = pygame.Rect(155 * tile_size, 5 * tile_size, 250, 100)
        screen.blit(scoretitle, scoretitleRect)
        score = largeFont.render(str(snake.food_count), True, white)
        scoreRect = score.get_rect()
        scoreRect = pygame.Rect(155 * tile_size, 10 * tile_size, 250, 100)
        screen.blit(score, scoreRect)
        
        # Check game over
        if snake.check_game_status(new_board):
            # Show game over title
            game_over = largeFont.render("Game Over", True, white)
            goRect = game_over.get_rect()
            goRect.center = ((width / 4), 50)
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
        pass

    elif tronGame is True:
        pass       

    pygame.display.flip()