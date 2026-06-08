from pydantic import BaseModel, model_validator, Field
# from typing import Literal
import sys
import re
from models.connection import Connection


class ConnectionModule(BaseModel):
    zone_a: str = Field(...)
    zone_b: str = Field(...)
    max_link_capacity: int = Field(default=1, ge=1)

    @model_validator(mode="before")
    @classmethod
    def validate_connection_module(cls, data: str):
        pattern = r'''
        ^\s*connection\s*:\s*
        (?P<zone_a>[^\s-]+)
        \s*-\s*
        (?P<zone_b>[^\s-]+)
        (?:\s*\[\s*max_link_capacity\s*=\s*(\d+)\s*\])?
        \s*$
        '''
        matchs = re.match(pattern, data, re.VERBOSE)
        if not matchs:
            raise ValueError("Invalid connection format")
        max_link_capacity = int(matchs.group(3)) if matchs.group(3) else 1
        return {
            "zone_a": matchs.group("zone_a"),
            "zone_b": matchs.group("zone_b"),
            "max_link_capacity": max_link_capacity
        }

    @model_validator(mode="after")
    def check_connection(self):
        if self.zone_a == self.zone_b:
            raise ValueError(
                f"Hub '{self.zone_a}' cannot connect to itself."
            )
        return Connection(self.zone_a, self.zone_b, self.max_link_capacity)


if __name__ == "__main__":
    print("Testing HubModule validation...")
    string = sys.argv[1]
    with open(sys.argv[1]) as f:
        strings = f.readlines()
        for string in strings:
            data = ConnectionModule.model_validate(string)
            print(data)
