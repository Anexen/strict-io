# strict-io

Read structured file into pydantic model(s).

# Usage

```python
from enum import Enum
from pydantic import BaseModel
from strict_io.csv import read_csv


class Variety(Enum):
    SETOSA = "Setosa"
    VERSICOLOR = "Versicolor"
    VIRGINICA = "Virginica"


class Iris(BaseModel):
    sepal_width: float
    sepal_length: float
    petal_width: float
    petal_length: float
    variety: Variety


read_csv("iris.csv")
```
