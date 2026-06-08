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
        self.cam_x = 0
        self.cam_y = 0
        self.current_turn = 0
        self.animations = []
        self.TURN_DURATION = 1.0
        self.drone_positions = self.create_drones_position()

    def create_drones_position(self):
        drone_positions = {}

        for i in range(1, self.nb_drones + 1):
            drone_positions[i] = {
                "x": self.start.x * 100,
                "y": self.start.y * 100,
            }
        return drone_positions

    def load_assets(self, WIDTH, HEIGHT):
        background = pygame.image.load("./img/image_background.jpeg")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        background_shadow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(
            background_shadow,
            (0, 0, 0, 100),
            (0, 0, WIDTH, HEIGHT)
        )

        img_drone = pygame.image.load("./img/image.png")
        img_drone = pygame.transform.scale(img_drone, (30, 30))
        glow = pygame.Surface((80, 80), pygame.SRCALPHA)

        pygame.draw.circle(
            glow,
            (255, 255, 100, 40),
            (40, 40),
            25
        )

        pygame.draw.circle(
            glow,
            (255, 0, 0, 80),
            (40, 40),
            15
        )
        return (
            background,
            background_shadow,
            img_drone,
            glow
        )

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.cam_y -= 10

        if keys[pygame.K_UP]:
            self.cam_y += 10

        if keys[pygame.K_RIGHT]:
            self.cam_x -= 10

        if keys[pygame.K_LEFT]:
            self.cam_x += 10
        if keys[pygame.K_q]:
            print("[EXIT]")
            sys.exit()

    def test(self):
        pygame.init()

        info = pygame.display.Info()
        WIDTH = info.current_w
        HEIGHT = info.current_h

        paused = False
        background, background_shadow, img_drone, glow = self.load_assets(
            WIDTH, HEIGHT)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Drone Simulation")

        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(80) / 1000
            self.handle_input()

            screen.blit(background, (0, 0))
            screen.blit(background_shadow, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused

                    if event.key == pygame.K_r:
                        paused = False
                        self.current_turn = 0
                        self.animations.clear()

                        self.drone_positions = self.create_drones_position()

            if (not paused
                    and not self.animations
                    and self.current_turn < len(self.history_turn)):
                turn_data = self.history_turn[self.current_turn]

                for move in turn_data["moves"]:
                    drone_id = move["drone"]

                    start = self.zones[move["from"]]
                    end = self.zones[move["to"]]

                    self.animations.append({
                        "drone": drone_id,

                        "sx": start.x * 100,
                        "sy": start.y * 100,

                        "ex": end.x * 100,
                        "ey": end.y * 100,

                        "progress": 0,
                    })

                self.current_turn += 1

            for conn in self.connections:
                a = self.zones[conn.zone_a]
                b = self.zones[conn.zone_b]

                ax = a.x * 100 + self.cam_x
                ay = a.y * 100 + HEIGHT / 2 + self.cam_y

                bx = b.x * 100 + self.cam_x
                by = b.y * 100 + HEIGHT / 2 + self.cam_y

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
                x = zone.x * 100 + self.cam_x
                y = zone.y * 100 + HEIGHT / 2 + self.cam_y

                color = (0, 120, 255)

                if zone.type == "restricted":
                    color = (255, 80, 80)

                elif zone.type == "priority":
                    color = (80, 255, 80)
                pygame.draw.circle(
                    screen,
                    zone.color if zone.color else color,
                    (int(x), int(y)),
                    25
                )

                font = pygame.font.SysFont(None, 24)

                text = font.render(name, True, (255, 255, 255))

                screen.blit(
                    text,
                    (x - 20, y - 40)
                )

            finished = []
            if paused:
                text = font.render(
                    "PAUSED",
                    True,
                    (255, 0, 0)
                )

                screen.blit(
                    text,
                    (WIDTH // 2 - 50, 50)
                )

            for anim in self.animations:
                anim["progress"] += dt

                p = min(
                    anim["progress"] / self.TURN_DURATION,
                    1
                )

                p = p * p * (3 - 2 * p)

                x = anim["sx"] + (
                    anim["ex"] - anim["sx"]
                ) * p

                y = anim["sy"] + (
                    anim["ey"] - anim["sy"]
                ) * p

                screen_x = x + self.cam_x
                screen_y = y + HEIGHT / 2 + self.cam_y

                self.drone_positions[anim["drone"]] = {
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
                    self.drone_positions[anim["drone"]] = {
                        "x": anim["ex"],
                        "y": anim["ey"],
                    }
            for drone_id, pos in self.drone_positions.items():

                screen_x = pos["x"] + self.cam_x
                screen_y = pos["y"] + HEIGHT / 2 + self.cam_y

                screen.blit(
                    glow,
                    (
                        screen_x - 40,
                        screen_y - 40
                    )
                )
                screen.blit(
                    img_drone,
                    (
                        int(screen_x - img_drone.get_width() / 2),
                        int(screen_y - img_drone.get_width() / 2)
                    )
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
                self.animations.remove(anim)

            pygame.display.flip()


if __name__ == "__main__":
    dis = Display()
    dis.test()
