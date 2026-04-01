from pydantic import BaseModel, model_validator, Field
from typing import Literal
import sys
import re


class HubModule(BaseModel):
    type: Literal["start_hub", "end_hub", "hub"] = Field(default="hub")
    name: str
    x: int
    y: int
    zone: Literal["normal", "priority", "restricted", "blocked"] = \
        Field(default="normal")
    max_drones: int | None = Field(default=1)
    color: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_hub_module(cls, data: str):
        '''
            start_hub    : 1222 0 0 [color: 'red']
        '''
        data_clean = " ".join(data.split())
        parts = data_clean.split(":")
        data_part2 = parts[1].split()
        if len(data_part2) < 3:
            print("ERROR: Invalid number of arguments for hub module")
            exit(1)
        if "-" in data_part2[0]:
            print("ERROR: '-' INVALID IN NAME")
            exit(1)
        hub_data = {
            "type": parts[0].lower().strip(),
            "name": data_part2[0],
            "x": data_part2[1],
            "y": data_part2[2]
        }
        if len(data_part2) > 3:
            options_str = parts[1][
                parts[1].index("[") + 1: parts[1].index("]")
                ]

            matches = re.findall(r'(\w+)\s*=\s*([^\s]+)', options_str)

            for key, value in matches:
                hub_data[key] = value.strip("'\"")
        return hub_data

    @model_validator(mode="after")
    def check_hub(self):
        if self.type in ("end_hub", "start_hub") and self.zone != "normal":
            raise ValueError("ERROR : end_hub and start_hub must be in normal"
                             "zone")
        return self


if __name__ == "__main__":
    print("Testing HubModule validation...")
    string = sys.argv[1]
    with open(sys.argv[1]) as f:
        strings = f.readlines()
        for string in strings:
            data = HubModule.model_validate(string)
            print(f"Result: {dict(data)}")
