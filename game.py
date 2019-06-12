import pygame

pygame.init()

screen_size = [800, 600]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Wargame")

clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill([255, 255, 255])
    clock.tick(30)

    pygame.display.flip()

pygame.quit()
