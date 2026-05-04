class Drone:
    def __init__(self, id, start_zone):
        self.id = id
        self.current_zone = start_zone
        self.position = None
        self.done = False
        self.path = []
