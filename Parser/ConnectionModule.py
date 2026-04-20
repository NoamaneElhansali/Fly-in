from pydantic import BaseModel, model_validator, Field
# from typing import Literal
import sys
import re


class ConnectionModule(BaseModel):
    zone_a: str = Field(...)
    zone_b: str = Field(...)
    max_link_capacity: int = Field(default=1, ge=1)

    @model_validator(mode="before")
    @classmethod
    def validate_connection_module(cls, data: str):
        pattern = r'''
        ^\s*connection\s*:\s*
        (?P<zone_a>[A-Za-z0-9_]+)
        \s*-\s*
        (?P<zone_b>[A-Za-z0-9_]+)
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
        return self


if __name__ == "__main__":
    print("Testing HubModule validation...")
    string = sys.argv[1]
    with open(sys.argv[1]) as f:
        strings = f.readlines()
        for string in strings:
            data = ConnectionModule.model_validate(string)
            print(data)
