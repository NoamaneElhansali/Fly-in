import pygame


class Display:
    def __init__(self):
        pass

    def test(self):
        pygame.init()
        screen = pygame.display.set_mode((1200, 700))
        clock = pygame.time.Clock()
        running = True
        player = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        dt = 0
        while running:
            if any(event.type == pygame.QUIT for event in pygame.event.get()):
                running = False
            screen.fill((0, 50, 0))
            # pygame.image.load()
            pygame.draw.circle(screen, "red", player, 40)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.y -= 300 * dt
            if keys[pygame.K_s]:
                player.y += 300 * dt
            if keys[pygame.K_a]:
                player.x -= 300 * dt
            if keys[pygame.K_d]:
                player.x += 300 * dt
            pygame.display.flip()
            dt = clock.tick(60) / 1000
        pygame.quit()


if __name__ == "__main__":
    dis = Display()
    dis.test()