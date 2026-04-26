class Zone:
    def __init__(self,
                 name: str,
                 x: int,
                 y: int,
                 zone_type: str = 'NORMAL',
                 max_drones: int = 1,
                 color: str = None):
        name = name
        x = x
        y = y
        zone_type = zone_type
        max_drones = max_drones
        color = color