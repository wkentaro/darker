import logging
from pathlib import Path
from typing import Any, Collection

from darker.exceptions import MissingPackageError
from darker.git import EditedLinenumsDiffer
from darker.utils import TextDocument, glob_any

try:
    import flynt

    flynt_fstringify_code_by_line = flynt.process.fstringify_code_by_line
except ImportError:
    # `flynt` is an optional dependency. Prevent the `ImportError` if it's missing.
    flynt = None

    def flynt_fstringify_code_by_line(  # type: ignore[misc]
        *args: Any, **kwargs: Any
    ) -> str:
        """Fake `flynt.fstringify_code_by_line()` to use when `flynt` isn't installed"""
        raise MissingPackageError(
            "No module named 'flynt'. Please install the 'flynt' package before using"
            " the --flynt / -i option."
        )


__all__ = ["apply_flynt", "flynt"]

logger = logging.getLogger(__name__)


def apply_flynt(
    content: TextDocument,
    src: Path,
    exclude: Collection[str],
    edited_linenums_differ: EditedLinenumsDiffer,
) -> TextDocument:
    """Run flynt on the given Python source file content

    This function includes all modifications from ``flynt`` in the result. It is the
    responsibility of the caller to filter output to modified lines only.

    :param content: The contents of the Python source code file to sort imports in
    :param src: The relative path to the file. This must be the actual path in the
                repository, which may differ from the path given on the command line in
                case of VSCode temporary files.
    :param exclude: The file path patterns to exclude from import sorting
    :param edited_linenums_differ: Helper for finding out which lines were edited
    :param config: Path to configuration file
    :param line_length: Maximum line length to use

    """
    if glob_any(src, exclude):
        return content
    edited_linenums = edited_linenums_differ.revision_vs_lines(
        src,
        content,
        context_lines=0,
    )
    if not edited_linenums:
        return content
    return _call_flynt_fstringify(content)


def _call_flynt_fstringify(content: TextDocument) -> TextDocument:
    """Call ``flynt.process.fstringify_code_by_line()``, return result `TextDocument`

    :param content: The contents of the Python source code file to fstringify

    """
    logger.debug("flynt.process.fstringify_code_by_line(code=...)")
    result, _ = flynt_fstringify_code_by_line(content.string)
    return TextDocument.from_str(
        result,
        encoding=content.encoding,
        mtime=content.mtime,
    )
