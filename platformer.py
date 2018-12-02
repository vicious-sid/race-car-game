import pygame
import os
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

large_text = pygame.font.Font('./assets/DroidSans.ttf', 115)
small_text = pygame.font.Font('./assets/DroidSans.ttf', 20)

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
pygame.display.set_caption('Platformer')
clock = pygame.time.Clock()


def scale_object(width, height):
    scaled_h = height*scale_h
    scaled_w = width*scale_w
    return scaled_w, scaled_h


def scale_placement(x, y):
    scaled_x = x * scale_w
    scaled_y = y * scale_h
    return scaled_x, scaled_y


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
        button('Continue', 400, 600, 160, 100, blue, green, game_unpause)
        button('QUIT', 1050, 600, 150, 100, dark_red, red, game_quit)

        pygame.display.update()
        clock.tick(60)


def platformer_game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
        game_display.fill(white)
        # large_text
        text_surface, text_rectangle = text_objects('platformer', large_text)
        text_rectangle.center = ((display_with / 2), (display_height / 4))
        game_display.blit(text_surface, text_rectangle)
        button('GO!', 400, 600, 150, 100, blue, green, game_quit)
        button('BACK', 1050, 600, 150, 100, dark_red, red, menu)
        pygame.display.update()
        clock.tick(60)

