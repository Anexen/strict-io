import os
from io import TextIOWrapper
from contextlib import nullcontext


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


def infer_compression(filename_or_obj):
    filename = os.fspath(filename_or_obj)
    if filename.endswith(".gz") or filename.endswith(".gzip"):
        compression = "gzip"
    elif filename.endswith(".zip"):
        compression = "zip"
    else:
        compression = None

    return compression


def use_compression(filename_or_obj, compression):
    if compression == "infer":
        compression = infer_compression(filename_or_obj)

    if compression == "gzip":
        import gzip

        return gzip.open(filename_or_obj, mode="rt")

    if compression == "zip":
        from zipfile import ZipFile

        with ZipFile(filename_or_obj) as zipfile:
            return TextIOWrapper(zipfile.open(zipfile.filelist[0]))

    if compression is None:
        if isinstance(filename_or_obj, (str, os.PathLike)):
            return open(filename_or_obj, "rt")

        # caller is responsible for closing file
        return nullcontext(filename_or_obj)

    raise ValueError(f"Unknown or unsupported compression: {compression}")
