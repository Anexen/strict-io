from enum import Enum

from typing import Optional
from strict_io.csv import read_csv
from pydantic import BaseModel, Field


class Address(BaseModel):
    first_name: Optional[str]
    last_name: str
    address_line_1: Optional[str]
    address_line_2: str
    state: str
    postal_code: str


class Sex(Enum):
    MALE = "M"
    FEMALE = "F"


class BioStats(BaseModel):
    name: str = Field(alias="Name")
    sex: Sex = Field(alias="Sex")
    age: int = Field(alias="Age")
    height: int = Field(alias="Height (in)")
    weight: int = Field(alias="Weight (lbs)")


def test_no_heading():
    addresses = list(
        read_csv(
            "tests/data/addresses.csv",
            Address,
            header=False,
            skipinitialspace=True,
        )
    )
    assert len(addresses) == 6
    assert isinstance(addresses[0], Address)
    assert addresses[0].postal_code == "08075"


def test_skip_initial_space():
    stats = list(
        read_csv("tests/data/biostats.csv", BioStats, skipinitialspace=True)
    )
    assert len(stats) == 18
    assert isinstance(stats[0], BioStats)
    assert stats[0].sex == Sex.MALE
    assert stats[0].weight == 170
