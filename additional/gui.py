import pygame, os, math

n = 8
max_pits = n * 0.25
max_beacons = n * 0.1


def homescreen():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('MCO1: Miner')
    done = True

    font_main = pygame.font.SysFont(None, 50)
    text_main = font_main.render("MCO1: Miner", True, (75, 75, 226))
    font_sub = pygame.font.SysFont(None, 25)
    text_sub = font_sub.render("Group 42 - CSINTSY", True, (102, 102, 102))

    font_input = pygame.font.SysFont(None, 25)
    text_input = font_input.render("Enter Number of Rows / Columns [8 - 64]:", True, (240, 246, 246))

    base_font = pygame.font.Font(None, 27)
    n_text = ''
    input_rect = pygame.Rect(
        440 // 2,
        text_main.get_height() + text_sub.get_height() + text_input.get_height() + 150 // 2,
        200, 30
    )

    text_algo = font_input.render("Choose Behavior:", True, (240, 246, 246))
    text_random = "Random"
    random_rect = pygame.Rect(
        400 // 2,
        text_main.get_height() + text_sub.get_height() + 400 // 2,
        100, 30
    )
    text_smart = "Smart"
    smart_rect = pygame.Rect(
        650 // 2,
        text_main.get_height() + text_sub.get_height() + 400 // 2,
        100, 30
    )

    text_enter = "Start"
    enter_rect = pygame.Rect(
        530 // 2,
        text_main.get_height() + text_sub.get_height() + 550 // 2,
        100, 30
    )

    n_active = (248, 249, 250)
    n_passive = (73, 80, 87)
    n_color = n_passive

    algo_active = (255, 183, 3)
    algo_passive = (0, 80, 157)
    algo_text_active = (255, 255, 255)
    algo_text_passive = (33, 37, 41)

    random_color = algo_passive
    random_color_text = algo_text_passive
    smart_color = algo_passive
    smart_color_text = algo_text_passive

    active_text = False
    active_random = False
    active_smart = False

    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active_text = True
                else:
                    active_text = False

                if random_rect.collidepoint(event.pos):
                    active_random = True
                    active_smart = False
                elif smart_rect.collidepoint(event.pos):
                    active_smart = True
                    active_random = False

                if enter_rect.collidepoint(event.pos):
                    if len(n_text) > 0 and str.isnumeric(n_text):
                        if int(n_text) >= 8 and int(n_text) <= 64:
                            if active_smart or active_random:
                                done = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    n_text = n_text[:-1]
                else:
                    n_text += event.unicode

        screen.fill((25, 25, 25))
        screen.blit(text_main, (320 - text_main.get_width() // 2, text_main.get_height() // 2))
        screen.blit(text_sub, (320 - text_sub.get_width() // 2, text_main.get_height() + 10 + text_sub.get_height() // 2))
        screen.blit(text_input, (320 - text_input.get_width() // 2, text_main.get_height() + text_sub.get_height() + 110 // 2))

        if active_text:
            n_color = n_active
        else:
            n_color = n_passive

        if active_random:
            random_color = algo_active
            random_color_text = algo_text_active
        else:
            random_color = algo_passive
            random_color_text = algo_text_passive

        if active_smart:
            smart_color = algo_active
            smart_color_text = algo_text_active
        else:
            smart_color = algo_passive
            smart_color_text = algo_text_passive

        pygame.draw.rect(screen, n_color, input_rect)

        text_surface = base_font.render(n_text, True, (33, 37, 41))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(200, text_surface.get_width() + 10)

        screen.blit(text_algo, (320 - text_algo.get_width() // 2, text_main.get_height() + text_sub.get_height() + text_surface.get_height() + 310 // 2))
        pygame.draw.rect(screen, random_color, random_rect)
        button_random = base_font.render(text_random, True, random_color_text)
        screen.blit(button_random, (random_rect.x + 13, random_rect.y + 5))

        pygame.draw.rect(screen, smart_color, smart_rect)
        button_smart = base_font.render(text_smart, True, smart_color_text)
        screen.blit(button_smart, (smart_rect.x + 20, smart_rect.y + 5))

        pygame.draw.rect(screen, (142, 202, 230), enter_rect)
        button_enter = base_font.render(text_enter, True, (255, 255, 255))
        screen.blit(button_enter, (enter_rect.x + 28, enter_rect.y + 5))

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('MCO1: Miner')
    done = False

    font_main = pygame.font.SysFont(None, 50)
    text_main = font_main.render("MCO1: Miner", True, (75, 75, 226))
    font_sub = pygame.font.SysFont(None, 25)
    text_sub = font_sub.render("Group 42 - CSINTSY", True, (102, 102, 102))

    font_icons = pygame.font.SysFont(None, 35)
    pits_icons = font_icons.render("P", True, (120, 85, 137))
    beacons_icons = font_icons.render("B", True, (73, 109, 219))

    gold = [4, 4]
    pits = {1: [2, 4], 2: [6, 6]}
    beacons = {1: [4, 2]}

    directory = os.getcwd()
    miner_icon = pygame.image.load(directory + r'\assets\miner_icon.png')
    miner_icon = pygame.transform.scale(miner_icon, (25, 25))

    gold_icon = pygame.image.load(directory + r'\assets\gold_icon.png')
    gold_icon = pygame.transform.scale(gold_icon, (25, 25))

    font_direction = pygame.font.SysFont(None, 30)
    curr_direction = font_direction.render("Current Direction: East", True, (240, 246, 246))

    box_width = 35
    box_height = 35
    box_margin = 7

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((25, 25, 25))
        screen.blit(text_main, (320 - text_main.get_width() // 2, text_main.get_height() // 2))
        screen.blit(text_sub, (320 - text_sub.get_width() // 2, text_main.get_height() + 10 + text_sub.get_height() // 2))

        curr_box = False
        for row in range(n):
            for column in range(n):
                for pit in range(0, len(pits)):
                    if row == pits[pit + 1][0] and column == pits[pit + 1][1]:
                        screen.blit(pits_icons,
                                    [((box_margin + box_width) * column + box_margin) + (320 - ((box_margin + box_width) * 8) // 2) + 8,
                                     ((box_margin + box_height) * row + box_margin) + text_main.get_height() + 10 + text_sub.get_height() + 20 + 8,
                                     box_width,
                                     box_height])
                        curr_box = True
                        break

                for beacon in range(0, len(beacons)):
                    if row == beacons[beacon + 1][0] and column == beacons[beacon + 1][1]:
                        screen.blit(beacons_icons,
                                    [((box_margin + box_width) * column + box_margin) + (320 - ((box_margin + box_width) * 8) // 2) + 8,
                                     ((box_margin + box_height) * row + box_margin) + text_main.get_height() + 10 + text_sub.get_height() + 20 + 8,
                                     box_width,
                                     box_height])
                        curr_box = True
                        break

                if not curr_box:
                    if row == 0 and column == 0:
                        screen.blit(miner_icon,
                                    [((box_margin + box_width) * column + box_margin) + (320 - ((box_margin + box_width) * 8) // 2) + 8,
                                     ((box_margin + box_height) * row + box_margin) + text_main.get_height() + 10 + text_sub.get_height() + 20 + 8,
                                     box_width,
                                     box_height])
                    elif row == gold[0] and column == gold[1]:
                        screen.blit(gold_icon,
                                    [((box_margin + box_width) * column + box_margin) + (320 - ((box_margin + box_width) * 8) // 2) + 8,
                                     ((box_margin + box_height) * row + box_margin) + text_main.get_height() + 10 + text_sub.get_height() + 20 + 8,
                                     box_width,
                                     box_height])
                    else:
                        pygame.draw.rect(screen, (200, 200, 200),
                                         [((box_margin + box_width) * column + box_margin) + (320 - ((box_margin + box_width) * 8) // 2),
                                          ((box_margin + box_height) * row + box_margin) + text_main.get_height() + 10 + text_sub.get_height() + 20,
                                          box_width,
                                          box_height])
                curr_box = False

        direction_height = ((box_margin + box_height) * n + box_margin) + text_main.get_height() + 10 + text_sub.get_height() + 30
        screen.blit(curr_direction, (320 - curr_direction.get_width() // 2, direction_height))

        pygame.display.flip()


homescreen()
main()