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

    @model_validator(mode='after')
    def check_data(self):
        hub_names = {x.name for x in self.hubs}
        for conn in self.connections:
            if (conn.zone_a != self.start_hub.name
                    and conn.zone_a not in hub_names):
                raise ValueError(f"hub :{conn.zone_a} is not found !")
            if (conn.zone_b != self.end_hub.name
                    and conn.zone_b not in hub_names):
                raise ValueError(f"hub :{conn.zone_b} is not found !")
        if self.nb_drones <= 0:
            raise ValueError(
                "Number of drones must be greater than zero."
            )
        if not self.start_hub:
            raise ValueError(
                "Start hub is missing."
            )

        if not self.end_hub:
            raise ValueError(
                "End hub is missing."
            )
        hub_names = {hub.name for hub in self.hubs}

        if len(self.hubs) != len(set(hub_names)):
            raise ValueError(
                "Duplicate hub names are not allowed."
            )
        if self.start_hub.name in hub_names:
            raise ValueError(
                f"Hub '{self.start_hub.name}' is already defined as start hub."
            )
        if self.end_hub.name in hub_names:
            raise ValueError(
                f"Hub '{self.end_hub.name}' is already defined as end hub."
            )
        if not self.connections:
            raise ValueError(
                "No connections defined."
            )
        if not any(
            self.start_hub.name in [c.zone_a, c.zone_b]
            for c in self.connections
        ):
            raise ValueError(
                "Start hub is isolated."
            )
        if not any(
            self.end_hub.name in [c.zone_a, c.zone_b]
            for c in self.connections
        ):
            raise ValueError(
                "End hub is isolated."
            )
        return self


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        data = Parser.model_validate(lines)
        print(data)
