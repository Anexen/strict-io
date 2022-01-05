import csv
import sys
import os
from typing import (
    BinaryIO,
    Iterable,
    Optional,
    Type,
    TypeVar,
    Union,
    Set,
    TYPE_CHECKING,
)

from ._common import DEFAULT_NA_VALUES, use_compression

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

if TYPE_CHECKING:
    from pydantic import BaseModel


T = TypeVar("T", bound="BaseModel")


__all__ = ["read_csv"]


def read_csv(
    filename_or_obj: Union[str, os.PathLike, BinaryIO],
    schema: Type[T],
    *,
    compression: Optional[Literal["infer", "gzip", "zip"]] = "infer",
    header: bool = True,
    skipinitialspace: bool = False,
    sep: str = ",",
    na_values: Optional[Set[str]] = None,
) -> Iterable[T]:

    if na_values is None:
        na_values = DEFAULT_NA_VALUES

    dialect = type(
        "CustomDialect",
        (csv.excel,),
        {"skipinitialspace": skipinitialspace, "delimiter": sep},
    )

    def read_value(value):
        if skipinitialspace:
            value = value.strip()

        return None if value in na_values else value

    with use_compression(filename_or_obj, compression) as f:
        reader = csv.reader(f, dialect=dialect)

        fieldnames = next(reader) if header else list(schema.__fields__.keys())

        for row in reader:

            if not row:
                continue

            row = dict(zip(fieldnames, map(read_value, row)))
            yield schema.parse_obj(row)
