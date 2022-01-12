import os
import sys
from typing import TYPE_CHECKING, BinaryIO, Optional, TypeVar, Union


if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

FileInput = Union[str, os.PathLike, BinaryIO]
Compression = Literal["gzip", "zip", "tar", "bz2"]
MaybeCompression = Optional[Union[Compression, Literal["infer"]]]

if TYPE_CHECKING:
    from pydantic import BaseModel


Model = TypeVar("Model", bound="BaseModel")
