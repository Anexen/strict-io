import csv
from typing import Iterable, Optional, Set, Type

from ._common import DEFAULT_NA_VALUES, use_compression
from ._typing import MaybeCompression, FileInput, Model


__all__ = ["read_csv"]


def read_csv(
    filename_or_obj: FileInput,
    schema: Type[Model],
    *,
    compression: MaybeCompression = "infer",
    header: bool = True,
    skipinitialspace: bool = False,
    sep: str = ",",
    na_values: Optional[Set[str]] = None,
) -> Iterable[Model]:

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

            yield schema.parse_obj(dict(zip(fieldnames, map(read_value, row))))
