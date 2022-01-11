import sys
from typing import Optional, Union


if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

Compression = Literal["gzip", "zip", "tar", "bz2"]
MaybeCompression = Optional[Union[Compression, Literal["infer"]]]
