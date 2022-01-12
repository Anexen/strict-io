from typing import Iterable, Type

from ._common import use_compression
from ._typing import FileInput, MaybeCompression, Model


__all__ = ["read_json_lines"]


def read_json_lines(
    filename_or_obj: FileInput,
    schema: Type[Model],
    *,
    compression: MaybeCompression = "infer",
) -> Iterable[Model]:
    with use_compression(filename_or_obj, compression) as f:
        for line in f:
            yield schema.parse_raw(line)
