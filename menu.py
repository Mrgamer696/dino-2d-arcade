# coding=utf-8
import sys

sys.path.insert(0, '../../')

import os
import pygame
import pygame_menu
from random import randrange
from main import App


ABOUT = ['pygame-menu {0}'.format('1.0'),
         'Author: @{0}'.format('Mr.gamer'),
         '',  # new line
         'Github: {0}'.format('')]
DIFFICULTY = ['EASY']
FPS = 60.0
WINDOW_SIZE = (1920, 1080)

clock = None  # type: pygame.time.Clock
main_menu = None  # type: pygame_menu.Menu
surface = None  # type: pygame.Surface


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def change_difficulty(value, difficulty):
    """
    Change difficulty of the game.

    :param value: Tuple containing the data of the selected object
    :type value: tuple
    :param difficulty: Optional parameter passed as argument to add_selector
    :type difficulty: str
    :return: None
    """
    selected, index = value
    print('Selected difficulty: "{0}" ({1}) at index {2}'.format(selected, difficulty, index))
    DIFFICULTY[0] = difficulty


def random_color():
    """
    Return random color.

    :return: Color tuple
    :rtype: tuple
    """
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


def play_function(difficulty, font, test=False):
    """
    Main game function.

    :param difficulty: Difficulty of the game
    :type difficulty: tuple, list
    :param font: Pygame font
    :type font: :py:class:`pygame.font.Font`
    :param test: Test method, if true only one loop is allowed
    :type test: bool
    :return: None
    """
    difficulty = difficulty[0]

    # Define globals
    global main_menu
    global clock

    if difficulty == 'EASY':
        f = font.render('Playing as a baby (easy)', 1, (255, 255, 255))
    elif difficulty == 'MEDIUM':
        f = font.render('Playing as a kid (medium)', 1, (255, 255, 255))
    elif difficulty == 'HARD':
        f = font.render('Playing as a champion (hard)', 1, (255, 255, 255))
    else:
        raise Exception('Unknown difficulty {0}'.format(difficulty))


    # Reset main menu and disable
    # You also can set another menu, like a 'pause menu', or just use the same
    # main_menu as the menu that will check all your input.
    main_menu.disable()
    main_menu.reset(1)

    game = App(difficulty)
    game.on_execute()


def main_background():
    """
    Function used by menus, draw on background while menu is active.

    :return: None
    """
    global surface
    surface.fill((47, 213, 220))


def main(test=False):
    """
    Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global clock
    global main_menu
    global surface

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    surface = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
    pygame.display.set_caption('Example - Game Selector')
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus: Play Menu
    # -------------------------------------------------------------------------
    play_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        title='Play Menu',
        width=WINDOW_SIZE[0] * 0.7,
    )

    submenu_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    submenu_theme.widget_font_size = 40
    play_submenu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.5,
        theme=submenu_theme,
        title='Submenu',
        width=WINDOW_SIZE[0] * 0.7,
    )
    for i in range(30):
        play_submenu.add_button('Back {0}'.format(i), pygame_menu.events.BACK)
    play_submenu.add_button('Return to main menu', pygame_menu.events.RESET)

    play_menu.add_button('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                         play_function,
                         DIFFICULTY,
                         pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 40))
    play_menu.add_selector('Select difficulty ',
                           [('1 - Easy', 'EASY'),
                            ('2 - Medium', 'MEDIUM'),
                            ('3 - Hard', 'HARD')],
                           onchange=change_difficulty,
                           selector_id='select_difficulty')
    play_menu.add_button('Another menu', play_submenu)
    play_menu.add_button('Return to main menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus:About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    about_theme.widget_margin = (0, 0)
    about_theme.widget_offset = (0, 0.05)

    about_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=about_theme,
        title='About',
        width=WINDOW_SIZE[0] * 0.6,
    )
    for m in ABOUT:
        about_menu.add_label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=40)
    about_menu.add_label('')
    about_menu.add_button('Return to menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Main
    # -------------------------------------------------------------------------
    main_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    main_theme.menubar_close_button = False  # Disable close button

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=main_theme,
        title='Main Menu',
        width=WINDOW_SIZE[0] * 0.6
    )

    main_menu.add_button('Play', play_menu)
    main_menu.add_button('About', about_menu)
    main_menu.add_button('Quit', pygame_menu.events.EXIT)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        pygame.init()
        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()