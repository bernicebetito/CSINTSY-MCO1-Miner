import pygame

def main():
    global screen
    WIDTH = 35
    HEIGHT = 35
    MARGIN = 7
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    done = False

    font_main = pygame.font.SysFont(None, 50)
    text_main = font_main.render("MCO1: Miner", True, (75, 75, 226))
    font_sub = pygame.font.SysFont(None, 25)
    text_sub = font_sub.render("Group 42 - CSINTSY", True, (102, 102, 102))
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill((25, 25, 25))

        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        done = False

        font_main = pygame.font.SysFont(None, 50)
        text_main = font_main.render("MCO1: Miner", True, (75, 75, 226))
        font_sub = pygame.font.SysFont(None, 25)
        text_sub = font_sub.render("Group 42 - CSINTSY", True, (102, 102, 102))
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            screen.fill((25, 25, 25))

            screen.blit(text_main, (320 - text_main.get_width() // 2, text_main.get_height() // 2))
            screen.blit(text_sub, (320 - text_sub.get_width() // 2, text_main.get_height() + 10 + text_sub.get_height() // 2))

            for row in range(8):
                for column in range(8):
                    pygame.draw.rect(screen, (200, 200, 200),
                                     [((MARGIN + WIDTH) * column + MARGIN) + (320 - ((MARGIN + WIDTH) * 8) // 2),
                                      ((MARGIN + HEIGHT) * row + MARGIN) + text_main.get_height() + 10 + text_sub.get_height() + 20,
                                      WIDTH,
                                      HEIGHT])

            pygame.display.flip()

        pygame.display.flip()


main()