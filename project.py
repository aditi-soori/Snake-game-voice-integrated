import pygame
import time
import random
from playsound import playsound

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
l = [white,yellow,red,black]
high = [0]
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game using Audio')


clock = pygame.time.Clock()

snake_block = 20
snake_speed = 5

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def our_snake(snake_block, snake_list):
    i = 0
    for x in snake_list:
        if i == len(l):
            i = 0
        pygame.draw.rect(dis, l[i], [x[0], x[1], snake_block, snake_block])#Drawing the snake
        i = i+1


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 10, dis_height / 4])
    
def message1(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 10, dis_height / 3])
def message2(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 10, dis_height / 2])


def gameLoop():

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
    j = 0
    playsound('audio.mp3')
    while not game_over:
        flag = 'y'
        while game_close == True:
            high.append(Length_of_snake)
            #dis.fill(background)
            background_image = pygame.image.load("grass.jpg").convert()
            dis.blit(background_image, [0, 0])
            m = max(high)
            
            message("You Lost! Your score is : "+str(Length_of_snake), red)
            message1("Highest Score : "+str(m), yellow)
            message2("Press C-Play Again or Q-Quit", white)
            pygame.display.update()
            if flag=='y':
                playsound('audio1.wav')
                playsound('audio.mp3')
                flag ='n'
            flag = 'n'

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        #dis.fill(background)
        background_image = pygame.image.load("grass.jpg").convert()
        dis.blit(background_image, [0, 0])
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])#Drawimg apple

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)


        pygame.display.update()
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            if j == len(l)-1:
                dis.fill(l[0])
                j = -1
            else:
                dis.fill(l[j+1])
            j = j+1
            pygame.display.update()

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
