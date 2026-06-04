from pydantic import BaseModel, model_validator, Field
from typing import Literal
import sys
import re
from models.zone import Zone


class HubModule(BaseModel):
    type: Literal["start_hub", "end_hub", "hub"] = Field(default="hub")
    name: str = Field(..., min_length=1)
    x: int = Field(...)
    y: int = Field(...)
    zone: Literal["normal", "priority", "restricted", "blocked"] = \
        Field(default="normal")
    max_drones: int | None = Field(default=1)
    color: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_hub_module(cls, data: str):
        pattern = r'''
        ^\s*
        (?P<type>\w+)
        \s*:\s*
        (?P<name>[A-Za-z0-9_]+)
        \s+
        (?P<x>-?\d+)
        \s+
        (?P<y>-?\d+)
        (?:\s*\[\s*(?P<options>.*?)\s*\])?
        \s*$
        '''
        matchs = re.match(pattern, data, re.VERBOSE)
        if not matchs:
            raise ValueError(f"Invalid hub format: {data}")
        hub_data = {
            "type": matchs.group("type").lower(),
            "name": matchs.group("name"),
            "x": int(matchs.group("x")),
            "y": int(matchs.group("y")),
        }

        metadata = matchs.group("options")
        if metadata:
            ops = re.findall(r'(\w+)\s*=\s*([^\s]+)', metadata)

            for key, val in ops:
                if key in hub_data:
                    raise ValueError(f"Duplicate key: {key}")
                hub_data[key] = val
        return hub_data

    @model_validator(mode="after")
    def check_hub(self):
        COLORS = {
            "rainbow": (255, 0, 255),
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "cyan": (0, 255, 255),
            "magenta": (255, 0, 255),
            "gray": (128, 128, 128),
            "dark_gray": (64, 64, 64),
            "light_gray": (200, 200, 200),

            "orange": (255, 165, 0),
            "purple": (128, 0, 128),
            "pink": (255, 105, 180),
            "brown": (139, 69, 19),
            "lime": (50, 205, 50),
            "navy": (0, 0, 128),
            "teal": (0, 128, 128),
            "olive": (128, 128, 0),
            "maroon": (128, 0, 0),

            "gold": (255, 215, 0),
            "silver": (192, 192, 192),
            "bronze": (205, 127, 50),

            "sky_blue": (135, 206, 235),
            "deep_sky_blue": (0, 191, 255),
            "turquoise": (64, 224, 208),
            "aqua": (0, 255, 255),

            "violet": (238, 130, 238),
            "indigo": (75, 0, 130),
            "lavender": (230, 230, 250),

            "coral": (255, 127, 80),
            "salmon": (250, 128, 114),
            "tomato": (255, 99, 71),

            "beige": (245, 245, 220),
            "ivory": (255, 255, 240),
            "khaki": (240, 230, 140),

            "mint": (152, 255, 152),
            "forest_green": (34, 139, 34),

            "crimson": (220, 20, 60),
            "firebrick": (178, 34, 34),

            "chocolate": (210, 105, 30),
            "tan": (210, 180, 140),

            "plum": (221, 160, 221),
            "orchid": (218, 112, 214),

            "hot_pink": (255, 20, 147),
            "deep_pink": (255, 20, 147),

            "royal_blue": (65, 105, 225),
            "steel_blue": (70, 130, 180),

            "spring_green": (0, 255, 127),
            "sea_green": (46, 139, 87),

            "snow": (255, 250, 250),
            "wheat": (245, 222, 179),

            "transparent_black": (0, 0, 0, 128),
            "transparent_white": (255, 255, 255, 128),
            "darkred": (139, 0, 0)
        }
        if self.type in ("end_hub", "start_hub") and self.zone != "normal":
            raise ValueError("ERROR : end_hub and start_hub must be in normal"
                             "zone")
        return Zone(self.name, self.x, self.y, self.zone, self.type,
                    self.max_drones,
                    COLORS[self.color])


if __name__ == "__main__":
    print("Testing HubModule validation...")
    string = sys.argv[1]
    with open(sys.argv[1]) as f:
        strings = f.readlines()
        for string in strings:
            data = HubModule.model_validate(string)
            print(f"Result: {dict(data)}")
