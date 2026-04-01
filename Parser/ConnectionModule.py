from pydantic import BaseModel, model_validator, Field
from typing import Literal
import sys
import re


class ConnectionModule(BaseModel):
    zone_a: str = Field(...)
    zone_b: str = Field(...)
    max_link_capacity: int = Field(default=1, ge=1)

    @model_validator(mode="before")
    @classmethod
    def validate_connection_module(cls, data: str):
        '''
        connection: <name1>-<name2> [max_link_capacity=2]
        '''
        data_clean = " ".join(data.split())
        parts = data_clean.split(":")
        if parts[0].strip() != "connection":
            print("ERROR: Invalid connection module format")
            exit(1)
        part_valid = parts[1].strip().split()
        if len(part_valid) > 2:
            print("ERROR: Too many arguments in connection module")
            exit(1)
        print(part_valid)
        exit()


if __name__ == "__main__":
    print("Testing HubModule validation...")
    string = sys.argv[1]
    with open(sys.argv[1]) as f:
        strings = f.readlines()
        for string in strings:
            data = ConnectionModule.model_validate(string)
