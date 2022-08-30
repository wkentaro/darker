"""Help and usage instruction texts used for the command line parser"""


def get_extra_instruction(dependency: str) -> str:
    """Generate the instructions to install Darker with particular extras

    :param dependency: Name of the extra package to install
    :return: Instructions for installing Darker with the extra package

    """
    return f"Please run `pip install darker[{dependency}]`"


DESCRIPTION_PARTS = [
    "Re-format Python source files by using\n",
    "- `flynt` to convert format strings to use f-strings\n",
    "- `isort` to sort Python import definitions alphabetically within logical"
    " sections\n",
    "- `black` to re-format code changed since the last Git commit",
]

try:
    import flynt
except ImportError:
    flynt = None
    DESCRIPTION_PARTS.extend(
        [
            "\n\n",
            get_extra_instruction("flynt"),
            " to enable converting old literal string formatting to f-strings",
        ]
    )

try:
    import isort
except ImportError:
    isort = None  # type: ignore[assignment]
    DESCRIPTION_PARTS.extend(
        [
            "\n",
            "\n",
            f"{get_extra_instruction('isort')} to enable sorting of import definitions",
        ]
    )
DESCRIPTION = "".join(DESCRIPTION_PARTS)


SRC = "Path(s) to the Python source file(s) to reformat"

REVISION = (
    "Git revision against which to compare the working tree. Tags, branch names, commit"
    " hashes, and other expressions like `HEAD~5` work here. Also a range like"
    " `master...HEAD` or `master...` can be used to compare the best common ancestor."
    " With the magic value `:PRE-COMMIT:`, Darker works in pre-commit compatible mode."
    " Darker expects the revision range from the `PRE_COMMIT_FROM_REF` and"
    " `PRE_COMMIT_TO_REF` environment variables. If those are not found, Darker works"
    " against `HEAD`."
)

DIFF = (
    "Don't write the files back, just output a diff for each file on stdout."
    " Highlight syntax if on a terminal and the `pygments` package is available, or if"
    " enabled by configuration."
)

CHECK = (
    "Don't write the files back, just return the status.  Return code 0 means"
    " nothing would change.  Return code 1 means some files would be"
    " reformatted."
)

STDOUT = (
    "Force complete reformatted output to stdout, instead of in-place. Only valid if"
    " there's just one file to reformat. Highlight syntax if on a terminal and the"
    " `pygments` package is available, or if enabled by configuration."
)

FLYNT_PARTS = [
    "Also convert string formatting to use f-strings using the `flynt` package"
]
if not flynt:
    FLYNT_PARTS.append(
        f". {get_extra_instruction('flynt')} to enable usage of this option."
    )
FLYNT = "".join(FLYNT_PARTS)

ISORT_PARTS = ["Also sort imports using the `isort` package"]
if not isort:
    ISORT_PARTS.append(
        f". {get_extra_instruction('isort')} to enable usage of this option."
    )
ISORT = "".join(ISORT_PARTS)

LINT = (
    "Also run a linter on changed files. `CMD` can be a name of path of the"
    " linter binary, or a full quoted command line. Highlight linter output syntax if"
    " on a terminal and the `pygments` package is available, or if enabled by"
    " configuration."
)

CONFIG = "Ask `black` and `isort` to read configuration from `PATH`."

VERBOSE = "Show steps taken and summarize modifications"
QUIET = "Reduce amount of output"
COLOR = (
    "Enable syntax highlighting even for non-terminal output. Overrides the environment"
    " variable PY_COLORS=0"
)
NO_COLOR = (
    "Disable syntax highlighting even for terminal output. Overrides the environment"
    " variable PY_COLORS=1"
)

VERSION = "Show the version of `darker`"

SKIP_STRING_NORMALIZATION = "Don't normalize string quotes or prefixes"
NO_SKIP_STRING_NORMALIZATION = (
    "Normalize string quotes or prefixes. This can be used to override"
    " `skip_string_normalization = true` from a configuration file."
)
SKIP_MAGIC_TRAILING_COMMA = (
    "Skip adding trailing commas to expressions that are split by comma"
    " where each element is on its own line. This includes function signatures."
    " This can be used to override"
    " `skip_magic_trailing_comma = true` from a configuration file."
)

LINE_LENGTH = "How many characters per line to allow [default: 88]"

WORKERS = "How many parallel workers to allow, or `0` for one per core [default: 1]"
