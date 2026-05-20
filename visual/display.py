import pygame
import sys


class Display:
    def __init__(self, zones, connections, history_turn, nb_drones,
                 start_zone, end_zone):
        self.zones = zones
        self.connections = connections
        self.history_turn = history_turn
        self.nb_drones = nb_drones
        self.start = start_zone
        self.end = end_zone

    # def test(self):
    #     pygame.init()
    #     screen = pygame.display.set_mode((1200, 700))
    #     clock = pygame.time.Clock()
    #     running = True
    #     player = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    #     player2 = pygame.Vector2(screen.get_width() / 4, screen.get_height() / 4)
    #     dt = 0
    #     while running:
    #         if any(event.type == pygame.QUIT for event in pygame.event.get()):
    #             running = False
    #         screen.fill((0, 50, 0))
    #         # pygame.image.load()
    #         pygame.draw.circle(screen, "red", player, 40)
    #         pygame.draw.line(screen, "red", player2, player2, 5000)
    #         keys = pygame.key.get_pressed()
    #         if keys[pygame.K_w]:
    #             player.y -= 300 * dt
    #         if keys[pygame.K_s]:
    #             player.y += 300 * dt
    #         if keys[pygame.K_a]:
    #             player.x -= 300 * dt
    #         if keys[pygame.K_d]:
    #             player.x += 300 * dt
    #         pygame.display.flip()
    #         dt = clock.tick(6) / 1000
    #     pygame.quit()

    # def run_vis(self):

    # def test(self):
    #     pygame.init()

    #     WIDTH = 1700
    #     HEIGHT = 800
    #     X = 0
    #     Y = 0

    #     screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #     clock = pygame.time.Clock()

    #     # zones = {
    #     #     "start": (100, 500),
    #     #     "A": (300, 100),
    #     #     "goal": (500, 300),
    #     # }

    #     # connections = [
    #     #     ("start", "A"),
    #     #     ("A", "goal"),
    #     # ]

    #     # drone_pos = [100, 300]

    #     # progress = 0
    #     turn = 0
    #     while True:
    #         screen.fill((20, 20, 20))

    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()

    #         for conn in self.connections:
    #             pygame.draw.line(
    #                 screen,
    #                 'red' if self.zones[conn.zone_b].type == "restricted" else "white",
    #                 (self.zones[conn.zone_a].x * 100 + X,
    #                     self.zones[conn.zone_a].y * 100 + screen.get_height() / 2 + Y),
    #                 (self.zones[conn.zone_b].x * 100 + X,
    #                     self.zones[conn.zone_b].y * 100 + screen.get_height() / 2 + Y),
    #                 3
    #             )

    #         for name, zone in self.zones.items():
    #             pygame.draw.circle(screen, (0, 120, 255), (zone.x * 100 + X,
    #                                zone.y * 100 + screen.get_height() / 2 + Y), 20)

    #         keys = pygame.key.get_pressed()
    #         if keys[pygame.K_UP]:
    #             Y -= 10
    #         if keys[pygame.K_DOWN]:
    #             Y += 10
    #         if keys[pygame.K_LEFT]:
    #             X -= 10
    #         if keys[pygame.K_RIGHT]:
    #             X += 10
    #         # progress += 0.01
    #         # if progress > 1:
    #         #     progress = 1

    #         # sx, sy = zones["start"]
    #         # ex, ey = zones["A"]

    #         # x = sx + (ex - sx) * progress
    #         # y = sy + (ey - sy) * progress

    #         # pygame.draw.circle(screen, (255, 255, 0), (x, y), 10)

    #         pygame.display.flip()
            # clock.tick(80)

    def test(self):
        pygame.init()

        info = pygame.display.Info()
        WIDTH = info.current_w
        HEIGHT = info.current_h

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Drone Simulation")

        clock = pygame.time.Clock()

        cam_x = 0
        cam_y = 0

        current_turn = 0
        animations = []

        TURN_DURATION = 1.0

        drone_positions = {}

        for i in range(1, self.nb_drones + 1):
            drone_positions[i] = {
                "x": self.start.x * 100,
                "y": self.start.y * 100,
            }

        while True:
            dt = clock.tick(80) / 1000

            screen.fill((20, 20, 20))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_DOWN]:
                cam_y -= 10

            if keys[pygame.K_UP]:
                cam_y += 10

            if keys[pygame.K_RIGHT]:
                cam_x -= 10

            if keys[pygame.K_LEFT]:
                cam_x += 10

            if not animations and current_turn < len(self.history_turn):
                turn_data = self.history_turn[current_turn]

                for move in turn_data["moves"]:
                    drone_id = move["drone"]

                    start = self.zones[move["from"]]
                    end = self.zones[move["to"]]

                    animations.append({
                        "drone": drone_id,

                        "sx": start.x * 100,
                        "sy": start.y * 100,

                        "ex": end.x * 100,
                        "ey": end.y * 100,

                        "progress": 0,
                    })

                current_turn += 1

            for conn in self.connections:
                a = self.zones[conn.zone_a]
                b = self.zones[conn.zone_b]

                ax = a.x * 100 + cam_x
                ay = a.y * 100 + HEIGHT / 2 + cam_y

                bx = b.x * 100 + cam_x
                by = b.y * 100 + HEIGHT / 2 + cam_y

                color = (
                    "red"
                    if b.type == "restricted"
                    else "white"
                )

                pygame.draw.line(
                    screen,
                    color,
                    (ax, ay),
                    (bx, by),
                    3
                )

            for name, zone in self.zones.items():
                x = zone.x * 100 + cam_x
                y = zone.y * 100 + HEIGHT / 2 + cam_y

                color = (0, 120, 255)

                if zone.type == "restricted":
                    color = (255, 80, 80)

                elif zone.type == "priority":
                    color = (80, 255, 80)
                pygame.draw.circle(
                    screen,
                    zone.color if zone.color else color,
                    (int(x), int(y)),
                    20
                )

                font = pygame.font.SysFont(None, 24)

                text = font.render(name, True, (255, 255, 255))

                screen.blit(
                    text,
                    (x - 20, y - 40)
                )

            finished = []

            for anim in animations:
                anim["progress"] += dt

                p = min(
                    anim["progress"] / TURN_DURATION,
                    1
                )

                p = p * p * (3 - 2 * p)

                x = anim["sx"] + (
                    anim["ex"] - anim["sx"]
                ) * p

                y = anim["sy"] + (
                    anim["ey"] - anim["sy"]
                ) * p

                screen_x = x + cam_x
                screen_y = y + HEIGHT / 2 + cam_y

                # pygame.draw.circle(
                #     screen,
                #     (255, 255, 0),
                #     (int(screen_x), int(screen_y)),
                #     10
                # )
                drone_positions[anim["drone"]] = {
                    "x": x,
                    "y": y,
                }

                font = pygame.font.SysFont(None, 22)

                label = font.render(
                    f"D{anim['drone']}",
                    True,
                    (255, 255, 255)
                )

                screen.blit(
                    label,
                    (screen_x + 10, screen_y - 10)
                )
                if p >= 1:
                    finished.append(anim)
                    drone_positions[anim["drone"]] = {
                        "x": anim["ex"],
                        "y": anim["ey"],
                    }
            for drone_id, pos in drone_positions.items():

                screen_x = pos["x"] + cam_x
                screen_y = pos["y"] + HEIGHT / 2 + cam_y

                pygame.draw.circle(
                    screen,
                    (255, 255, 0),
                    (int(screen_x), int(screen_y)),
                    10
                )

                font = pygame.font.SysFont(None, 22)

                label = font.render(
                    f"D{drone_id}",
                    True,
                    (255, 255, 255)
                )

                screen.blit(
                    label,
                    (screen_x + 10, screen_y - 10)
                )

            for anim in finished:
                animations.remove(anim)

            pygame.display.flip()

if __name__ == "__main__":
    dis = Display()
    dis.test()
