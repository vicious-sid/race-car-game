import pygame
import random

pygame.init()
display_with = 1600
display_height = 900
black = (0, 0, 0)
white = (255, 255, 255)
red = (237, 28, 36)
blue = (63, 72, 204)
green = (34, 177, 76)
dark_red = (200, 28, 36)

pause = False
troll = False

large_text = pygame.font.Font('./assets/DroidSans.ttf', 115)
small_text = pygame.font.Font('./assets/DroidSans.ttf', 20)

car_with = 124

game_display = pygame.display.set_mode((display_with, display_height))
pygame.display.set_caption('My Obstacles')
clock = pygame.time.Clock()

car_img = pygame.image.load('./assets/race_car.png')


def things_doged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("doged: " + str(count), True, black)
    game_display.blit(text, (0, 0))


def things(thing_x, thing_y, thing_w, thing_h, color):
    pygame.draw.rect(game_display, color, [thing_x, thing_y, thing_w, thing_h])


def car(x, y):
    game_display.blit(car_img, (x, y))


def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def message_display(text):
    # large_text
    text_suface, text_rectangle = text_objects(text, large_text)
    text_rectangle.center = ((display_with / 2), (display_height / 2))
    game_display.blit(text_suface, text_rectangle)
    pygame.display.update()
    pygame.time.wait(5000)
    game_loop()


def crashed():
    crash = True

    while crash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
        game_display.fill(white)
        # large_text
        text_suface, text_rectangle = text_objects('You Crashed', large_text)
        text_rectangle.center = ((display_with / 2), (display_height / 2))
        game_display.blit(text_suface, text_rectangle)

        buton('Retry', 400, 600, 160, 100, blue, green, game_loop)
        buton('QUIT', 1050, 600, 150, 100, dark_red, red, game_quit)

        pygame.display.update()
        clock.tick(60)


def game_quit():
    pygame.quit()
    quit()


# def troll_intro():
#     while troll:
#         troll_button = [('Click Me', 400, 600, 160, 100, blue, green, troll_intro),
#                         ('no seriosley', 400, 200, 160, 100, blue, green, troll_intro),
#                         ('i mean it', 500, 100, 160, 100, blue, green, troll_intro),
#                         ]
#         i = 0
#         for i in range(0, 2):
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     game_quit()
#             button_list = [troll_button[i]]
#             display_menu(white, button_list)
#             i += 1


def display_menu(bg_color, button_list):
    game_display.fill(bg_color)
    for button_def in button_list:
        print(repr(button_def))
        buton(button_def[0], button_def[1], button_def[2], button_def[3], button_def[4], button_def[5], button_def[6],
              button_def[7])
    pygame.display.flip()
    clock.tick(60)


def buton(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display, blue, (x, y, w, h))
        if click[0] ==\
                1 and action is not None:
            action()
            # if action == 'play':
            #     game_loop()
            # elif action == 'quit':
            #     pygame.quit()
            #     quit()
    else:
        pygame.draw.rect(game_display, green, (x, y, w, h))
    # small_text
    text_suface, text_rectangle = text_objects(msg, small_text)
    text_rectangle.center = ((x + (w / 2)), (y + (h / 2)))
    game_display.blit(text_suface, text_rectangle)
    if 1050 + 150 > mouse[0] > 1050 and 600 + 100 > mouse[1] > 600:
        pygame.draw.rect(game_display, ic, (1050, 600, 150, 100))
    else:
        pygame.draw.rect(game_display, ac, (1050, 600, 150, 100))
    # small_text
    text_suface, text_rectangle = text_objects('QUIT', small_text)
    text_rectangle.center = ((1050 + (150 / 2)), (600 + (100 / 2)))
    game_display.blit(text_suface, text_rectangle)


def game_unpause():
    global pause
    pause = False


def game_paused():
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
        game_display.fill(white)
        # large_text
        text_suface, text_rectangle = text_objects('Game Paused', large_text)
        text_rectangle.center = ((display_with / 2), (display_height / 2))
        game_display.blit(text_suface, text_rectangle)
        # print('PAUSED')
        buton('Continue', 400, 600, 160, 100, blue, green, game_unpause)
        buton('QUIT', 1050, 600, 150, 100, dark_red, red, game_quit)

        pygame.display.update()
        clock.tick(60)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
        game_display.fill(white)
        # large_text
        text_suface, text_rectangle = text_objects('My Obstacles', large_text)
        text_rectangle.center = ((display_with / 2), (display_height / 2))
        game_display.blit(text_suface, text_rectangle)

        buton('GO!', 400, 600, 150, 100, blue, green, game_loop)
        buton('QUIT', 1050, 600, 150, 100, dark_red, red, game_quit)

        pygame.display.update()
        clock.tick(60)


def game_loop():
    global pause
    global troll
    x = (display_with * 0.45)
    y = (display_height * 0.8)
    x_change = 0
    y_change = 0

    thing_startx = random.randrange(0, display_with)
    thing_starty = -600
    thing_speed = 4
    thing_with = 170
    thing_hight = 170

    doged = 0

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                # if event.key == pygame.K_UP:
                #     y_change = -5
                # elif event.key == pygame.K_DOWN:
                #     y_change = 5
                if event.key == pygame.K_q:
                    game_quit()
                if event.key == pygame.K_p:
                    pause = True
                    game_paused()
                # if event.key == pygame.K_t:
                #     troll = True
                #     # troll_intro()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
        #         y_change = 0
        # y += y_change
        x += x_change
        game_display.fill(green)

        # things(thing_x, thing_y, thing_w, thing_h, color)
        things(thing_startx, thing_starty, thing_with, thing_hight, red)
        thing_starty += thing_speed
        car(x, y)
        things_doged(doged)
        if x > display_with - car_with or x < 0:
            crashed()
        if thing_starty > display_height:
            thing_starty = 0 - thing_hight
            thing_startx = random.randrange(0, display_with)
            doged += 1
            thing_speed += .1

        if y < thing_starty + thing_hight:
            if x > thing_startx and x < thing_startx + thing_with or x + car_with > thing_startx and x + car_with < thing_startx + thing_with:
                crashed()

        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
pygame.quit()
quit()
