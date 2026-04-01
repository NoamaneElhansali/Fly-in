from pydantic import BaseModel, Field, model_validator


class CheckParser(BaseModel):
    nb_drones: int = Field(..., gt=0)
    start_hub: str = Field(...)
    end_hub: str = Field(...)
    