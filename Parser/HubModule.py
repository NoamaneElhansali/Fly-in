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
        if self.type in ("end_hub", "start_hub") and self.zone != "normal":
            raise ValueError("ERROR : end_hub and start_hub must be in normal"
                             "zone")
        return Zone(self.name, self.x, self.y, self.zone, self.type, self.max_drones,
                    self.color)


if __name__ == "__main__":
    print("Testing HubModule validation...")
    string = sys.argv[1]
    with open(sys.argv[1]) as f:
        strings = f.readlines()
        for string in strings:
            data = HubModule.model_validate(string)
            print(f"Result: {dict(data)}")
