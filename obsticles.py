import pygame
import random

pygame.init()
# display_with = 1600
# display_height = 900
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
infoObject = pygame.display.Info()
print('inforObject', infoObject)
print('DISPLAY:', infoObject.current_w, infoObject.current_h)
display_with = infoObject.current_w
display_height = infoObject.current_h
scale_w = infoObject.current_w/1600
scale_h = infoObject.current_h/900
print('SCALE X/Y', scale_w, scale_h)
game_display = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
# game_display = pygame.display.set_mode((display_with, display_height))
pygame.display.set_caption('My Obstacles')
clock = pygame.time.Clock()

car_img = pygame.image.load('./assets/race_car.png')


def scale_object(width, height):
    scaled_h = height*scale_h
    scaled_w = width*scale_w
    return scaled_w, scaled_h


def scale_placement(x, y):
    scaled_x = x * scale_w
    scaled_y = y * scale_h
    return scaled_x, scaled_y


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("dodged: " + str(count), True, black)
    game_display.blit(text, (0, 0))


def road_blocks(thing_x, thing_y, thing_w, thing_h, color):
    pt_x, pt_y = scale_placement(thing_x, thing_y)
    pt_w, pt_h = scale_object(thing_w, thing_h)
    pygame.draw.rect(game_display, color, [pt_x, pt_y, pt_w, pt_h])


def car(x, y):
    sx, sy = scale_placement(x, y)
    game_display.blit(car_img, (sx, sy))


def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def message_display(text):
    # large_text
    text_surface, text_rectangle = text_objects(text, large_text)
    text_rectangle.center = ((display_with / 2), (display_height / 2))
    game_display.blit(text_surface, text_rectangle)
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
        button('Retry', 400, 600, 150, 100, blue, green, game_loop)
        button('MENU', 1050, 600, 150, 100, dark_red, red, menu)

        pygame.display.update()
        clock.tick(60)


def game_quit():
    pygame.quit()
    quit()


def menu():
    import menu
    menu.game_menu()


def display_menu(bg_color, button_list):
    game_display.fill(bg_color)
    for button_def in button_list:
        print(repr(button_def))
        button(button_def[0], button_def[1], button_def[2], button_def[3], button_def[4], button_def[5], button_def[6],
               button_def[7])
    pygame.display.flip()
    clock.tick(60)


def button(msg, t_x, t_y, t_w, t_h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    x, y = scale_placement(t_x, t_y)
    w, h = scale_object(t_w, t_h)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display, ic, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(game_display, ac, (x, y, w, h))
    # small_text
    text_surface, text_rectangle = text_objects(msg, small_text)
    text_rectangle.center = ((x + (w / 2)), (y + (h / 2)))
    game_display.blit(text_surface, text_rectangle)


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
        text_rectangle.center = ((display_with / 2), (display_height / 3))
        game_display.blit(text_suface, text_rectangle)
        # print('PAUSED')
        button('Continue', 400, 600, 150, 100, blue, green, game_unpause)
        button('MENU', 1050, 600, 150, 100, dark_red, red, menu)

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
        text_surface, text_rectangle = text_objects('My Obstacles', large_text)
        text_rectangle.center = ((display_with / 2), (display_height / 3))
        game_display.blit(text_surface, text_rectangle)
        button('GO!', 400, 600, 152, 100, blue, green, game_loop)
        button('BACK', 1050, 600, 152, 100, dark_red, red, menu)
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
    obstacle_width, obstacle_height = scale_object(170, 170)
    dodged = 0

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

        thing_startx

        # things(thing_x, thing_y, thing_w, thing_h, color)
        road_blocks(thing_startx, thing_starty, obstacle_width, obstacle_height, red)
        thing_starty += thing_speed
        car(x, y)
        things_dodged(dodged)
        if x > display_with - car_with or x < 0:
            crashed()
        if thing_starty > display_height:
            thing_starty = 0 - obstacle_height
            thing_startx = random.randrange(0, display_with)
            dodged += 1
            thing_speed += .1

        if y < thing_starty + obstacle_height:
            if x > thing_startx and x < thing_startx + obstacle_width or x + car_with > thing_startx and x + car_with < thing_startx + obstacle_width:
                crashed()

        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
pygame.quit()
quit()
