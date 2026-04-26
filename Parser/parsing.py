from pydantic import BaseModel, model_validator, Field
# from typing import Literal
import sys
# import re
from .HubModule import HubModule
from .ConnectionModule import ConnectionModule


class Parser(BaseModel):
    nb_drones: int = Field(...)
    start_hub: object = Field(...)
    end_hub: object = Field(...)
    hubs: list
    connections: list 

    @model_validator(mode='before')
    @classmethod
    def clean_data(cls, lines):
        data = {
            "nb_drones": 0,
            'start_hub': {},
            'end_hub': {},
            'hubs': [],
            'connections': []
        }
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            elif line.startswith("nb_drones"):
                parts_nb_drones = line.split(':')
                if (len(parts_nb_drones) != 2):
                    raise ValueError("INVALID INPUT NB_DRONES")
                data['nb_drones'] = parts_nb_drones[1]
            elif line.startswith('hub'):
                data['hubs'].append(HubModule.model_validate(line))
            elif line.startswith('start_hub'):
                data['start_hub'] = HubModule.model_validate(line)
            elif line.startswith('end_hub'):
                data['end_hub'] = HubModule.model_validate(line)
            elif line.startswith('connection'):
                data['connections'].append(
                    ConnectionModule.model_validate(line))
        return data


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        data = Parser.model_validate(lines)
        print(data)