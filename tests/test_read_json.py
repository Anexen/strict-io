from typing import List

from pydantic import BaseModel

from strict_io.json import read_json_lines


class Family(BaseModel):
    id: int
    father: str
    mother: str
    children: List[str]


def test_read_json_lines():
    families = list(read_json_lines("tests/data/family.json", Family))
    assert len(families) == 3
    assert isinstance(families[0], Family)
    assert len(families[1].children) == 3
