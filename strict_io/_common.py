import os
from contextlib import nullcontext
from io import TextIOWrapper
from typing import ContextManager, Optional, TextIO

from ._typing import Compression, MaybeCompression


DEFAULT_NA_VALUES = {
    "",
    "#NA",
    "<NA>",
    "n/a",
    "#N/A",
    "N/A",
    "null",
    "NULL",
    "nan",
    "NaN",
    "-nan",
    "-NaN",
}


def infer_compression(filename_or_obj) -> Optional[Compression]:
    filename = os.fspath(filename_or_obj)

    if filename.endswith(".tar.gz"):
        return "tar"

    if filename.endswith(".gz") or filename.endswith(".gzip"):
        return "gzip"

    if filename.endswith(".zip"):
        return "zip"

    if filename.endswith(".bz2"):
        return "bz2"

    return None


class CloseStack:
    def __init__(self, resource, *other):
        super().__init__()
        self.resource = resource
        self.other = other

    def __enter__(self):
        for cm in self.other:
            cm.__enter__()
        return self.resource.__enter__()

    def __exit__(self, *args, **kwargs):
        self.resource.__exit__()
        for cm in reversed(self.other):
            cm.__exit__(*args, **kwargs)


def use_compression(
    filename_or_obj, compression: MaybeCompression
) -> ContextManager[TextIO]:
    if compression == "infer":
        compression = infer_compression(filename_or_obj)

    if compression == "gzip":
        import gzip

        return gzip.open(filename_or_obj, mode="rt")

    if compression == "zip":
        from zipfile import ZipFile

        zf = ZipFile(filename_or_obj)
        if not zf.filelist:
            zf.close()
            raise ValueError("Empty zip archive")

        # prevent operating on closed archive file
        zf_fileobj = TextIOWrapper(zf.open(zf.filelist[0]))
        return CloseStack(zf_fileobj, zf)

    if compression == "tar":
        import tarfile

        tf = tarfile.open(filename_or_obj, mode="r")
        member = tf.next()

        if member is None:
            tf.close()
            raise ValueError("Empty tar archive")

        fileobj = tf.extractfile(member)
        if fileobj is None:
            tf.close()
            raise ValueError(f"{member.name} is not a regular file")

        # prevent operating on closed archive file
        return CloseStack(TextIOWrapper(fileobj), tf)

    if compression == "bz2":
        import bz2

        return bz2.open(filename_or_obj, mode="rt")

    if compression is None:
        if isinstance(filename_or_obj, (str, os.PathLike)):
            return open(filename_or_obj, mode="rt")

        # caller is responsible for closing file
        return nullcontext(filename_or_obj)

    raise ValueError(f"Unknown or unsupported compression: {compression}")
