import pygame, random, math

n = 8
max_pits = n * 0.25
max_beacons = n * 0.1

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    done = False

    font_main = pygame.font.SysFont(None, 50)
    text_main = font_main.render("MCO1: Miner", True, (75, 75, 226))
    font_sub = pygame.font.SysFont(None, 25)
    text_sub = font_sub.render("Group 42 - CSINTSY", True, (102, 102, 102))

    font_icons = pygame.font.SysFont(None, 35)
    miner_icon = font_icons.render("M", True, (201, 124, 93))
    pits_icons = font_icons.render("P", True, (120, 85, 137))
    beacons_icons = font_icons.render("B", True, (73, 109, 219))
    gold_icon = font_icons.render("G", True, (244, 232, 124))

    gold = [4, 4]
    pits = {1: [2, 4], 2: [6, 6]}
    beacons = {1: [4, 2]}

    font_direction = pygame.font.SysFont(None, 30)
    curr_direction = font_direction.render("Current Direction: East", True, (240, 246, 246))

    width = 35
    height = 35
    margin = 7

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill((25, 25, 25))

        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        done = False

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
                                        [((margin + width) * column + margin) + (320 - ((margin + width) * 8) // 2) + 8,
                                         ((margin + height) * row + margin) + text_main.get_height() + 10 + text_sub.get_height() + 20 + 8,
                                         width,
                                         height])
                            curr_box = True
                            break

                    for beacon in range(0, len(beacons)):
                        if row == beacons[beacon + 1][0] and column == beacons[beacon + 1][1]:
                            screen.blit(beacons_icons,
                                        [((margin + width) * column + margin) + (320 - ((margin + width) * 8) // 2) + 8,
                                         ((margin + height) * row + margin) + text_main.get_height() + 10 + text_sub.get_height() + 20 + 8,
                                         width,
                                         height])
                            curr_box = True
                            break

                    if not curr_box:
                        if row == 0 and column == 0:
                            screen.blit(miner_icon,
                                        [((margin + width) * column + margin) + (320 - ((margin + width) * 8) // 2) + 8,
                                         ((margin + height) * row + margin) + text_main.get_height() + 10 + text_sub.get_height() + 20 + 8,
                                         width,
                                         height])
                        elif row == gold[0] and column == gold[1]:
                            screen.blit(gold_icon,
                                        [((margin + width) * column + margin) + (320 - ((margin + width) * 8) // 2) + 8,
                                         ((margin + height) * row + margin) + text_main.get_height() + 10 + text_sub.get_height() + 20 + 8,
                                         width,
                                         height])
                        else:
                            pygame.draw.rect(screen, (200, 200, 200),
                                         [((margin + width) * column + margin) + (320 - ((margin + width) * 8) // 2),
                                          ((margin + height) * row + margin) + text_main.get_height() + 10 + text_sub.get_height() + 20,
                                          width,
                                          height])
                    curr_box = False

            direction_height = ((margin + height) * n + margin) + text_main.get_height() + 10 + text_sub.get_height() + 30
            screen.blit(curr_direction, (320 - curr_direction.get_width() // 2, direction_height))
            pygame.display.flip()

        pygame.display.flip()


main()