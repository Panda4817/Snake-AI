import pygame
import sys
import time

from snake import *

pygame.init()
size = width, height = 1750, 750

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

screen = pygame.display.set_mode(size)

largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
smallFont = pygame.font.Font("OpenSans-Regular.ttf", 18)
startGame = False
instructions = False


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        """
        # captures the 'KEYDOWN' and 'KEYUP' events
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            # gets the key name
            key_name = pygame.key.name(event.key)

            # converts to uppercase the key name
            key_name = key_name.upper()

            # if any key is pressed
            if event.type == pygame.KEYDOWN:
                # prints on the console the key pressed
                print(f'{key_name} key pressed')

            # if any key is released
            elif event.type == pygame.KEYUP:
                # prints on the console the released key
                print(f'{key_name} key released')
        """
    screen.fill(black)

    # Common buttons
    playButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
    play = mediumFont.render("Play", True, black)
    playRect = play.get_rect()
    playRect.center = playButton.center
    howToPlayButton = pygame.Rect(4* (width / 8), (height / 2), width / 3, 50)
    howToPlay = mediumFont.render("How to play", True, black)
    howToPlayRect = howToPlay.get_rect()
    howToPlayRect.center = howToPlayButton.center
    backButton = pygame.Rect(5* (width / 8), (height / 2), width / 4, 50)
    back = mediumFont.render("Back", True, black)
    backRect = back.get_rect()
    backRect.center = backButton.center

    if startGame is False and instructions is False:
        # Setup board and snake
        new_board = Board()
        new_board.setup()
        new_board.place_food()
        snake = Snake()
        snake.setup(new_board)

        # Draw title
        title = largeFont.render("Play Snake", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        
        pygame.draw.rect(screen, white, playButton)
        screen.blit(play, playRect)
        
        pygame.draw.rect(screen, white, howToPlayButton)
        screen.blit(howToPlay, howToPlayRect)

        # Check if button is clicked
        click, _, _= pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playButton.collidepoint(mouse):
                time.sleep(0.2)
                startGame = True
            elif howToPlayButton.collidepoint(mouse):
                time.sleep(0.2)
                instructions = True
    
    elif startGame is False and instructions is True:

        # Draw title
        title = largeFont.render("How to play Snake", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw instructions
        text1 = smallFont.render("Use arrow keys to control the snake: red squares.", True, white)
        text2 = smallFont.render("Eat the food: green squares.", True, white)
        text3 = smallFont.render("Avoid the edge and your own body.", True, white)
        text1Rect = text1.get_rect()
        text1Rect.center = ((width / 2), (height / 2) - 75)
        text2Rect = text2.get_rect()
        text2Rect.center = ((width / 2), (height / 2) - 55)
        text3Rect = text3.get_rect()
        text3Rect.center = ((width / 2), (height / 2) - 35)
        screen.blit(text1, text1Rect)
        screen.blit(text2, text2Rect)
        screen.blit(text3, text3Rect)

        # Draw buttons
        pygame.draw.rect(screen, white, playButton)
        screen.blit(play, playRect)
        pygame.draw.rect(screen, white, backButton)
        screen.blit(back, backRect)

        # Check if button is clicked
        click, _, _= pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            instructions = False
            if playButton.collidepoint(mouse):
                time.sleep(0.2)    
                startGame = True
            elif backButton.collidepoint(mouse):
                time.sleep(0.2)
    else:
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
            game_over = largeFont.render("Game Over", True, white)
            goRect = game_over.get_rect()
            goRect = pygame.Rect(152 * tile_size, 20 * tile_size, 250, 100)
            screen.blit(game_over, goRect)
            
            bButton = pygame.Rect(155 * tile_size, 25 * tile_size, 100, 50)
            b = mediumFont.render("Back", True, black)
            bRect = b.get_rect()
            bRect.center = bButton.center
            pygame.draw.rect(screen, white, bButton)
            screen.blit(b, bRect)
            # Check if button is clicked
            click, _, _= pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if bButton.collidepoint(mouse):
                    startGame = False
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
            

    pygame.display.flip()