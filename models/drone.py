class Drone:
    def __init__(self, id, start_zone):
        self.id = id
        self.current_zone = start_zone
        self.position = None
        self.done = False
        self.path = []
        self.wait = 0
        self.target_zone = None
        self.just_arrived = False
