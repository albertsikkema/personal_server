TITLE: Formatting Files with Ruff Format Command (Shell)
DESCRIPTION: This snippet illustrates different methods for using the `ruff format` command to automatically reformat Python code. It supports formatting entire directories, specific paths, glob patterns, individual files, and processing arguments from a file. This command applies consistent code style.
SOURCE: https://github.com/astral-sh/ruff/blob/main/README.md#_snippet_4

LANGUAGE: shell
CODE:
```
ruff format                          # Format all files in the current directory (and any subdirectories).
ruff format path/to/code/            # Format all files in `/path/to/code` (and any subdirectories).
ruff format path/to/code/*.py        # Format all `.py` files in `/path/to/code`.
ruff format path/to/code/to/file.py  # Format `file.py`.
ruff format @arguments.txt           # Format using an input file, treating its contents as newline-delimited command-line arguments.
```

----------------------------------------

TITLE: Installing Ruff with Standalone Installers
DESCRIPTION: This snippet demonstrates how to install Ruff using standalone shell scripts for macOS/Linux via `curl` and Windows via `powershell`. It also shows how to install a specific version of Ruff using these methods, which are available from version 0.5.0 onwards.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/faq.md#_snippet_1

LANGUAGE: console
CODE:
```
$ # On macOS and Linux.
$ curl -LsSf https://astral.sh/ruff/install.sh | sh

$ # On Windows.
$ powershell -c "irm https://astral.sh/ruff/install.ps1 | iex"

$ # For a specific version.
$ curl -LsSf https://astral.sh/ruff/0.5.0/install.sh | sh
$ powershell -c "irm https://astral.sh/ruff/0.5.0/install.ps1 | iex"
```

----------------------------------------

TITLE: Printing 'Hello World' (Python)
DESCRIPTION: This snippet prints the classic 'hello world' message to the console using Python's built-in `print` function. It serves as a basic example of outputting text to standard output.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ruff_notebook/resources/test/fixtures/jupyter/vscode_language_id_expected.ipynb#_snippet_1

LANGUAGE: python
CODE:
```

print("hello world")
```

----------------------------------------

TITLE: Type Narrowing with `is not None` in Python
DESCRIPTION: This snippet demonstrates how `is not None` acts as a type guard, removing `None` from a union type. It shows the type of `x` being narrowed to `Literal[1]` within the `if` block and `None` in the `else` block, while remaining `None | Literal[1]` outside.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/narrow/conditionals/is_not.md#_snippet_0

LANGUAGE: Python
CODE:
```
def _(flag: bool):
    x = None if flag else 1

    if x is not None:
        reveal_type(x)  # revealed: Literal[1]
    else:
        reveal_type(x)  # revealed: None

    reveal_type(x)  # revealed: None | Literal[1]
```

----------------------------------------

TITLE: Narrowing Value Literals in Python Truthiness Checks
DESCRIPTION: Demonstrates how Python's type checker narrows the type of a variable `x` (which can hold various literal values including `0`, `None`, `True`, `False`, strings, bytes, and tuples) within `if` and `else` blocks based on its truthiness. It also shows the effect of complex boolean expressions like `x and not x` and `x or not x` on type narrowing, revealing `Never` for unreachable code paths and the original union for always-true paths.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/narrow/truthiness.md#_snippet_0

LANGUAGE: Python
CODE:
```
from typing import Literal

def foo() -> Literal[0, -1, True, False, "", "foo", b"", b"bar", None] | tuple[()]:
    return 0

x = foo()

if x:
    reveal_type(x)  # revealed: Literal[-1, True, "foo", b"bar"]
else:
    reveal_type(x)  # revealed: Literal[0, False, "", b""] | None | tuple[()]

if not x:
    reveal_type(x)  # revealed: Literal[0, False, "", b""] | None | tuple[()]
else:
    reveal_type(x)  # revealed: Literal[-1, True, "foo", b"bar"]

if x and not x:
    reveal_type(x)  # revealed: Never
else:
    reveal_type(x)  # revealed: Literal[0, -1, "", "foo", b"", b"bar"] | bool | None | tuple[()]

if not (x and not x):
    reveal_type(x)  # revealed: Literal[0, -1, "", "foo", b"", b"bar"] | bool | None | tuple[()]
else:
    reveal_type(x)  # revealed: Never

if x or not x:
    reveal_type(x)  # revealed: Literal[0, -1, "", "foo", b"", b"bar"] | bool | None | tuple[()]
else:
    reveal_type(x)  # revealed: Never

if not (x or not x):
    reveal_type(x)  # revealed: Never
else:
    reveal_type(x)  # revealed: Literal[0, -1, "", "foo", b"", b"bar"] | bool | None | tuple[()]

if (isinstance(x, int) or isinstance(x, str)) and x:
    reveal_type(x)  # revealed: Literal[-1, True, "foo"]
else:
    reveal_type(x)  # revealed: Literal[b"", b"bar", 0, False, ""] | None | tuple[()]
```

----------------------------------------

TITLE: Adding Ruff as a Development Dependency with uv
DESCRIPTION: This command uses `uv` to add Ruff as a development dependency to the project. This makes the `ruff` executable available within the project's virtual environment for linting and formatting.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/tutorial.md#_snippet_3

LANGUAGE: console
CODE:
```
$ uv add --dev ruff
```

----------------------------------------

TITLE: Narrowing with `x != None` in Python
DESCRIPTION: This snippet demonstrates how comparing a variable `x` with `None` using `!=` narrows its type. In the `if` branch, `x` is revealed as `Literal[1]` (non-None), while in the `else` branch, it's revealed as `None`.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/narrow/conditionals/eq.md#_snippet_0

LANGUAGE: Python
CODE:
```
def _(flag: bool):
    x = None if flag else 1

    if x != None:
        reveal_type(x)  # revealed: Literal[1]
    else:
        reveal_type(x)  # revealed: None
```

----------------------------------------

TITLE: Annotating Variables with Optional in Python
DESCRIPTION: This snippet demonstrates how to use `typing.Optional` for type annotations in Python, showing its equivalence to `Union[T, None]` and how nested `Optional` types are flattened. It uses `reveal_type` to show the inferred types.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/annotations/optional.md#_snippet_0

LANGUAGE: Python
CODE:
```
from typing import Optional

a: Optional[int]
a1: Optional[bool]
a2: Optional[Optional[bool]]
a3: Optional[None]

def f():
    # revealed: int | None
    reveal_type(a)
    # revealed: bool | None
    reveal_type(a1)
    # revealed: bool | None
    reveal_type(a2)
    # revealed: None
    reveal_type(a3)
```

----------------------------------------

TITLE: Running Ruff Check in GitHub Actions CI
DESCRIPTION: This GitHub Actions workflow sets up Python, installs Ruff, and runs `ruff check` with `github` output format for inline annotations. It's a standard CI setup for linting Python projects, ensuring code quality on every push.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/integrations.md#_snippet_0

LANGUAGE: YAML
CODE:
```
name: CI
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff
      # Update output format to enable automatic inline annotations.
      - name: Run Ruff
        run: ruff check --output-format=github .
```

----------------------------------------

TITLE: Impact of Statically Known Truthiness on Short-Circuiting in Python
DESCRIPTION: This snippet shows how statically known truthiness (e.g., `True`) affects short-circuit evaluation. When `True or (x := 1)` is evaluated, the `(x := 1)` part is never reached due to short-circuiting, making `x` an unresolved reference. Conversely, in `True and (x := 1)`, the `(x := 1)` part is always evaluated because `True` is truthy, ensuring `x` is defined.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/boolean/short_circuit.md#_snippet_2

LANGUAGE: Python
CODE:
```
if True or (x := 1):
    # error: [unresolved-reference]
    reveal_type(x)  # revealed: Unknown

if True and (x := 1):
    reveal_type(x)  # revealed: Literal[1]
```

----------------------------------------

TITLE: Using `typing.Callable` for Fixed Positional Arguments (Python)
DESCRIPTION: This snippet demonstrates how to use `typing.Callable` to define a function signature with specific positional argument types and a return type. It shows how type checkers infer the return type and identify errors when arguments of incorrect types are passed.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/call/annotation.md#_snippet_0

LANGUAGE: Python
CODE:
```
from typing import Callable

def _(c: Callable[[], int]):
    reveal_type(c())  # revealed: int

def _(c: Callable[[int, str], int]):
    reveal_type(c(1, "a"))  # revealed: int

    # error: [invalid-argument-type] "Argument is incorrect: Expected `int`, found `Literal["a"]`"
    # error: [invalid-argument-type] "Argument is incorrect: Expected `str`, found `Literal[1]`"
    reveal_type(c("a", 1))  # revealed: int
```

----------------------------------------

TITLE: Detecting Unresolved References in Python
DESCRIPTION: This check flags references to variables or names that have not been defined within their scope. Using an undefined name will cause a `NameError` at runtime.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty/docs/rules.md#_snippet_46

LANGUAGE: Python
CODE:
```
print(x)  # NameError: name 'x' is not defined
```

----------------------------------------

TITLE: Ignoring Specific Ruff Lint Rules
DESCRIPTION: This setting defines a list of specific linting rules that Ruff should ignore, effectively disabling them. This is useful for suppressing rules that might conflict with project-specific conventions or for temporarily bypassing certain checks. Rules are identified by their codes.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/editors/settings.md#_snippet_19

LANGUAGE: json
CODE:
```
{
    "ruff.lint.ignore": ["E4", "E7"]
}
```

LANGUAGE: lua
CODE:
```
require('lspconfig').ruff.setup {
  init_options = {
    settings = {
      lint = {
        ignore = {"E4", "E7"}
      }
    }
  }
}
```

LANGUAGE: json
CODE:
```
{
  "lsp": {
    "ruff": {
      "initialization_options": {
        "settings": {
          "lint": {
            "ignore": ["E4", "E7"]
          }
        }
      }
    }
  }
}
```

----------------------------------------

TITLE: Importing Modules and Accessing Math Constant in Python
DESCRIPTION: This snippet imports the standard `math` and `os` modules. It then demonstrates accessing the `pi` constant from the `math` module, which represents the mathematical constant pi (approximately 3.14159).
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ruff_notebook/resources/test/fixtures/jupyter/add_missing_cell_id.ipynb#_snippet_0

LANGUAGE: python
CODE:
```
import math
import os

math.pi
```

----------------------------------------

TITLE: Enabling Postponed Evaluation of Type Annotations in Python
DESCRIPTION: This snippet shows how to enable postponed evaluation of type annotations using `from __future__ import annotations`. This allows forward references in type hints and simplifies type annotation syntax by removing the need for string literal quotes for types that are not yet defined, improving readability and reducing boilerplate.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_vendored/vendor/typeshed/stdlib/_typeshed/README.md#_snippet_1

LANGUAGE: python
CODE:
```
from __future__ import annotations
```

----------------------------------------

TITLE: Ignoring Specific Ruff Rule for an Entire File in Python
DESCRIPTION: This Python example illustrates how to suppress a specific Ruff linting rule (e.g., `UP035`) for an entire file. By adding `# ruff: noqa: {code}` anywhere in the file, preferably at the top, all instances of that rule within the file will be ignored.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/tutorial.md#_snippet_19

LANGUAGE: python
CODE:
```
# ruff: noqa: UP035
from typing import Iterable

def sum_even_numbers(numbers: Iterable[int]) -> int:
    """Given an iterable of integers, return the sum of all even numbers in the iterable."""
    return sum(num for num in numbers if num % 2 == 0)
```

----------------------------------------

TITLE: Inferring Parameter Types in Python Functions
DESCRIPTION: This snippet demonstrates how Python's type inference works for various parameter kinds, including positional-only, positional-or-keyword, keyword-only, variadic positional (*args), and variadic keyword (**kwargs), showing the inferred types using `reveal_type`.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/function/parameters.md#_snippet_0

LANGUAGE: Python
CODE:
```
from typing import Literal

def f(a, b: int, c=1, d: int = 2, /, e=3, f: Literal[4] = 4, *args: object, g=5, h: Literal[6] = 6, **kwargs: str):
    reveal_type(a)  # revealed: Unknown
    reveal_type(b)  # revealed: int
    reveal_type(c)  # revealed: Unknown | Literal[1]
    reveal_type(d)  # revealed: int
    reveal_type(e)  # revealed: Unknown | Literal[3]
    reveal_type(f)  # revealed: Literal[4]
    reveal_type(g)  # revealed: Unknown | Literal[5]
    reveal_type(h)  # revealed: Literal[6]
    reveal_type(args)  # revealed: tuple[object, ...]
    reveal_type(kwargs)  # revealed: dict[str, str]
```

----------------------------------------

TITLE: Installing Ruff with uv, pip, or pipx
DESCRIPTION: This section provides commands for installing Ruff using common Python package managers. Users can choose to install Ruff globally with `uv tool install`, add it as a development dependency to a project with `uv add --dev`, or install it using `pip` or `pipx`.
SOURCE: https://github.com/astral-sh/ruff/blob/main/README.md#_snippet_1

LANGUAGE: shell
CODE:
```
# With uv.
uv tool install ruff@latest  # Install Ruff globally.
uv add --dev ruff            # Or add Ruff to your project.

# With pip.
pip install ruff

# With pipx.
pipx install ruff
```

----------------------------------------

TITLE: Installing Third-Party Type Stubs with pip (Bash)
DESCRIPTION: This command demonstrates how to install type stubs for third-party Python packages like html5lib and requests using pip. These stub packages, following PEP 561, are automatically released to PyPI and are essential for type checkers to provide accurate analysis for external libraries.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_vendored/vendor/typeshed/README.md#_snippet_0

LANGUAGE: bash
CODE:
```
$ pip install types-html5lib types-requests
```

----------------------------------------

TITLE: Recommended Ruff Rule Selection in pyproject.toml
DESCRIPTION: This `pyproject.toml` configuration provides a recommended set of popular Ruff rules to enable. It includes rule prefixes for pycodestyle ('E'), Pyflakes ('F'), pyupgrade ('UP'), flake8-bugbear ('B'), flake8-simplify ('SIM'), and isort ('I'), offering a balanced linting setup.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/linter.md#_snippet_3

LANGUAGE: TOML
CODE:
```
[tool.ruff.lint]
select = [
    # pycodestyle
    "E",
    # Pyflakes
    "F",
    # pyupgrade
    "UP",
    # flake8-bugbear
    "B",
    # flake8-simplify
    "SIM",
    # isort
    "I",
]
```

----------------------------------------

TITLE: Default Ruff Configuration in pyproject.toml
DESCRIPTION: This snippet shows Ruff's default configuration when integrated into a `pyproject.toml` file. It defines common directory exclusions, line length, indentation, target Python version, and default linting rules (Pyflakes and a subset of pycodestyle). It also sets default formatting options like quote style and line endings.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/configuration.md#_snippet_0

LANGUAGE: TOML
CODE:
```
[tool.ruff]
# Exclude a variety of commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pyenv",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    ".vscode",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "site-packages",
    "venv",
]

# Same as Black.
line-length = 88
indent-width = 4

# Assume Python 3.9
target-version = "py39"

[tool.ruff.lint]
# Enable Pyflakes (`F`) and a subset of the pycodestyle (`E`) codes by default.
# Unlike Flake8, Ruff doesn't enable pycodestyle warnings (`W`) or
# McCabe complexity (`C901`) by default.
select = ["E4", "E7", "E9", "F"]
ignore = []

# Allow fix for all enabled rules (when `--fix`) is provided.
fixable = ["ALL"]
unfixable = []

# Allow unused variables when underscore-prefixed.
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[tool.ruff.format]
# Like Black, use double quotes for strings.
quote-style = "double"

# Like Black, indent with spaces, rather than tabs.
indent-style = "space"

# Like Black, respect magic trailing commas.
skip-magic-trailing-comma = false

# Like Black, automatically detect the appropriate line ending.
line-ending = "auto"

# Enable auto-formatting of code examples in docstrings. Markdown,
# reStructuredText code/literal blocks and doctests are all supported.
#
# This is currently disabled by default, but it is planned for this
# to be opt-out in the future.
docstring-code-format = false

# Set the line length limit used when formatting code snippets in
# docstrings.
#
# This only has an effect when the `docstring-code-format` setting is
# enabled.
docstring-code-line-length = "dynamic"
```

----------------------------------------

TITLE: Automatically Fixing Linting Errors with Ruff
DESCRIPTION: This command runs the Ruff linter with the `--fix` option, automatically resolving the previously identified unused import error. The output confirms that one error was fixed.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/tutorial.md#_snippet_5

LANGUAGE: console
CODE:
```
$ uv run ruff check --fix
Found 1 error (1 fixed, 0 remaining).
```

----------------------------------------

TITLE: Installing Ruff with uv, pip, and pipx
DESCRIPTION: This snippet provides various command-line methods to install Ruff using `uv` (globally or per project), `pip`, and `pipx`. These methods are recommended for integrating Ruff into Python development environments without requiring a Rust toolchain.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/faq.md#_snippet_0

LANGUAGE: console
CODE:
```
$ # Install Ruff globally.
$ uv tool install ruff@latest

$ # Or add Ruff to your project.
$ uv add --dev ruff

$ # With pip.
$ pip install ruff

$ # With pipx.
$ pipx install ruff
```

----------------------------------------

TITLE: Formatting Python Files with Ruff CLI
DESCRIPTION: Demonstrates basic usage of the `ruff format` command-line interface to format Python files and directories. It shows how to format all files in the current directory, a specific directory, or a single file. The command formats files in-place by default.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/formatter.md#_snippet_0

LANGUAGE: Shell
CODE:
```
ruff format                   # Format all files in the current directory.
ruff format path/to/code/     # Format all files in `path/to/code` (and any subdirectories).
ruff format path/to/file.py   # Format a single file.
```

----------------------------------------

TITLE: Comprehensive Ruff Linting and Formatting (ruff.toml)
DESCRIPTION: This comprehensive `ruff.toml` configuration snippet illustrates how to enable specific linting rules (including `flake8-bugbear`), ignore line-length violations, prevent fixes for certain issues, define per-file import ignores, and enforce single quotes for code formatting.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/configuration.md#_snippet_4

LANGUAGE: toml
CODE:
```
[lint]
# 1. Enable flake8-bugbear (`B`) rules, in addition to the defaults.
select = ["E4", "E7", "E9", "F", "B"]

# 2. Avoid enforcing line-length violations (`E501`)
ignore = ["E501"]

# 3. Avoid trying to fix flake8-bugbear (`B`) violations.
unfixable = ["B"]

# 4. Ignore `E402` (import violations) in all `__init__.py` files, and in selected subdirectories.
[lint.per-file-ignores]
"__init__.py" = ["E402"]
"**/{tests,docs,tools}/*" = ["E402"]

[format]
# 5. Use single quotes in `ruff format`.
quote-style = "single"
```

----------------------------------------

TITLE: Defining a Function with a Mutable Default Argument in Python
DESCRIPTION: This snippet defines a Python function `mutable_argument` with a mutable default argument `z` initialized to an empty set. Calling this function without an argument will use the same set object across multiple calls, which can lead to unexpected behavior if the set is modified. It prints the current state of the set.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ruff_notebook/resources/test/fixtures/jupyter/valid.ipynb#_snippet_1

LANGUAGE: python
CODE:
```
def mutable_argument(z=set()):
  print(f"cell two: {z}")

mutable_argument()
```

----------------------------------------

TITLE: Default Ruff Configuration in ruff.toml
DESCRIPTION: This snippet illustrates Ruff's default configuration when defined in a standalone `ruff.toml` file. It includes the same settings as the `pyproject.toml` version, covering directory exclusions, code style (line length, indentation), target Python version, and default linting and formatting rules.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/configuration.md#_snippet_1

LANGUAGE: TOML
CODE:
```
# Exclude a variety of commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pyenv",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    ".vscode",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "site-packages",
    "venv",
]

# Same as Black.
line-length = 88
indent-width = 4

# Assume Python 3.9
target-version = "py39"

[lint]
# Enable Pyflakes (`F`) and a subset of the pycodestyle (`E`) codes by default.
# Unlike Flake8, Ruff doesn't enable pycodestyle warnings (`W`) or
# McCabe complexity (`C901`) by default.
select = ["E4", "E7", "E9", "F"]
ignore = []

# Allow fix for all enabled rules (when `--fix`) is provided.
fixable = ["ALL"]
unfixable = []

# Allow unused variables when underscore-prefixed.
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[format]
# Like Black, use double quotes for strings.
quote-style = "double"

# Like Black, indent with spaces, rather than tabs.
indent-style = "space"

# Like Black, respect magic trailing commas.
skip-magic-trailing-comma = false

# Like Black, automatically detect the appropriate line ending.
line-ending = "auto"

# Enable auto-formatting of code examples in docstrings. Markdown,
# reStructuredText code/literal blocks and doctests are all supported.
#
# This is currently disabled by default, but it is planned for this
# to be opt-out in the future.
docstring-code-format = false

# Set the line length limit used when formatting code snippets in
# docstrings.
#
# This only has an effect when the `docstring-code-format` setting is
# enabled.
docstring-code-line-length = "dynamic"
```

----------------------------------------

TITLE: Python Decorator `functools.cache`
DESCRIPTION: Demonstrates the use of `functools.cache` (or `functools.lru_cache` in older Python versions) to memoize function results. This decorator stores the results of expensive function calls and returns the cached result when the same inputs occur again, improving performance.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/decorators.md#_snippet_6

LANGUAGE: Python
CODE:
```
from functools import cache

@cache
def f(x: int) -> int:
    return x**2

# TODO: Should be `_lru_cache_wrapper[int]`
reveal_type(f)  # revealed: _lru_cache_wrapper[Unknown]

# TODO: Should be `int`
reveal_type(f(1))  # revealed: Unknown
```

----------------------------------------

TITLE: Type Narrowing in Elif-Else Blocks - Python
DESCRIPTION: This snippet illustrates how type narrowing works in `if-elif` chains. Even when a condition is met (e.g., `x == 1`), the type of `x` might not narrow to a `Literal` if it could be a subclass. In subsequent `elif` blocks, the type is narrowed by excluding previously checked values.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/narrow/conditionals/elif_else.md#_snippet_0

LANGUAGE: Python
CODE:
```
def _(x: int):
    if x == 1:
        # cannot narrow; could be a subclass of `int`
        reveal_type(x)  # revealed: int
    elif x == 2:
        reveal_type(x)  # revealed: int & ~Literal[1]
    elif x != 3:
        reveal_type(x)  # revealed: int & ~Literal[1] & ~Literal[2] & ~Literal[3]
```

----------------------------------------

TITLE: Running Ruff from Command Line
DESCRIPTION: Shows basic command-line usage of Ruff after installation, for linting and formatting files in the current directory.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/installation.md#_snippet_2

LANGUAGE: Console
CODE:
```
$ ruff check   # Lint all files in the current directory.
$ ruff format  # Format all files in the current directory.
```

----------------------------------------

TITLE: Slicing Strings in Python
DESCRIPTION: This snippet illustrates various string slicing operations in Python, including specifying start, stop, and step values. It covers cases with positive and negative indices, omitted parameters, `None` values, and boolean indices for slices. The examples also demonstrate `zero-stepsize-in-slice` errors and how type revelation changes for literal strings versus dynamically sliced strings.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/subscript/string.md#_snippet_1

LANGUAGE: Python
CODE:
```
def _(m: int, n: int, s2: str):
    s = "abcde"

    reveal_type(s[0:0])  # revealed: Literal[""]
    reveal_type(s[0:1])  # revealed: Literal["a"]
    reveal_type(s[0:2])  # revealed: Literal["ab"]
    reveal_type(s[0:5])  # revealed: Literal["abcde"]
    reveal_type(s[0:6])  # revealed: Literal["abcde"]
    reveal_type(s[1:3])  # revealed: Literal["bc"]

    reveal_type(s[-3:5])  # revealed: Literal["cde"]
    reveal_type(s[-4:-2])  # revealed: Literal["bc"]
    reveal_type(s[-10:10])  # revealed: Literal["abcde"]

    reveal_type(s[0:])  # revealed: Literal["abcde"]
    reveal_type(s[2:])  # revealed: Literal["cde"]
    reveal_type(s[5:])  # revealed: Literal[""]
    reveal_type(s[:2])  # revealed: Literal["ab"]
    reveal_type(s[:0])  # revealed: Literal[""]
    reveal_type(s[:2])  # revealed: Literal["ab"]
    reveal_type(s[:10])  # revealed: Literal["abcde"]
    reveal_type(s[:])  # revealed: Literal["abcde"]

    reveal_type(s[::-1])  # revealed: Literal["edcba"]
    reveal_type(s[::2])  # revealed: Literal["ace"]
    reveal_type(s[-2:-5:-1])  # revealed: Literal["dcb"]
    reveal_type(s[::-2])  # revealed: Literal["eca"]
    reveal_type(s[-1::-3])  # revealed: Literal["eb"]

    reveal_type(s[None:2:None])  # revealed: Literal["ab"]
    reveal_type(s[1:None:1])  # revealed: Literal["bcde"]
    reveal_type(s[None:None:None])  # revealed: Literal["abcde"]

    start = 1
    stop = None
    step = 2
    reveal_type(s[start:stop:step])  # revealed: Literal["bd"]

    reveal_type(s[False:True])  # revealed: Literal["a"]
    reveal_type(s[True:3])  # revealed: Literal["bc"]

    s[0:4:0]  # error: [zero-stepsize-in-slice]
    s[:4:0]  # error: [zero-stepsize-in-slice]
    s[0::0]  # error: [zero-stepsize-in-slice]
    s[::0]  # error: [zero-stepsize-in-slice]

    substring1 = s[m:n]
    reveal_type(substring1)  # revealed: LiteralString

    substring2 = s2[0:5]
    reveal_type(substring2)  # revealed: str
```

----------------------------------------

TITLE: Installing Ruff with Homebrew
DESCRIPTION: Command to install Ruff using Homebrew, a package manager for macOS and Linux.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/installation.md#_snippet_4

LANGUAGE: Console
CODE:
```
$ brew install ruff
```

----------------------------------------

TITLE: Detecting Invalid Return Type in Python
DESCRIPTION: This diagnostic identifies functions where the returned object's type is incompatible with the function's annotated return type. Such mismatches can lead to confusion for users calling the function and potential runtime errors. The example shows a function annotated to return an integer, but it returns a string, triggering the error.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty/docs/rules.md#_snippet_26

LANGUAGE: Python
CODE:
```
def func() -> int:
    return "a"  # error: [invalid-return-type]
```

----------------------------------------

TITLE: Integrating Ruff with EFM Language Server for Linting and Formatting
DESCRIPTION: This YAML configuration defines how the `efm-langserver` should use Ruff for Python linting and formatting. It specifies the commands, input methods (stdin), and output formats for Ruff's `check` and `format` operations.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/editors/setup.md#_snippet_9

LANGUAGE: YAML
CODE:
```
tools:
  python-ruff:
    lint-command: "ruff check --stdin-filename ${INPUT} --output-format concise --quiet -"
    lint-stdin: true
    lint-formats:
      - "%f:%l:%c: %m"
    format-command: "ruff format --stdin-filename ${INPUT} --quiet -"
    format-stdin: true
```

----------------------------------------

TITLE: Declaring Python Project Dependencies
DESCRIPTION: This snippet defines the Python package dependencies for a project. It includes standard PyPI packages with exact version pinning, as well as packages installed directly from Git repositories, specifying commit hashes for reproducibility.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/requirements-insiders.txt#_snippet_0

LANGUAGE: Python
CODE:
```
PyYAML==6.0.2
ruff==0.11.11
mkdocs==1.6.1
mkdocs-material @ git+ssh://git@github.com/astral-sh/mkdocs-material-insiders.git@39da7a5e761410349e9a1b8abf593b0cdd5453ff
mkdocs-redirects==1.2.2
mdformat==0.7.22
mdformat-mkdocs==4.1.2
mkdocs-github-admonitions-plugin @ git+https://github.com/PGijsbers/admonitions.git#7343d2f4a92e4d1491094530ef3d0d02d93afbb7
```

----------------------------------------

TITLE: Defining Property Getter and Setter in Python
DESCRIPTION: Illustrates how to add a setter method to a property using the `@<property_name>.setter` decorator. The setter method takes the value to be set as an argument. Shows type checking for assignments, including an invalid assignment example.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/properties.md#_snippet_1

LANGUAGE: Python
CODE:
```
class C:
    @property
    def my_property(self) -> int:
        return 1

    @my_property.setter
    def my_property(self, value: int) -> None:
        pass

c = C()
reveal_type(c.my_property)  # revealed: int
c.my_property = 2

# error: [invalid-assignment]
c.my_property = "a"
```

----------------------------------------

TITLE: Indexing Strings in Python
DESCRIPTION: This snippet demonstrates how to access individual characters in a Python string using both positive and negative integer indices. It also shows how boolean values are interpreted as indices (False=0, True=1) and illustrates `index-out-of-bounds` errors when accessing non-existent positions. The `reveal_type` calls indicate the inferred literal or general string types.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/subscript/string.md#_snippet_0

LANGUAGE: Python
CODE:
```
s = "abcde"

reveal_type(s[0])  # revealed: Literal["a"]
reveal_type(s[1])  # revealed: Literal["b"]
reveal_type(s[-1])  # revealed: Literal["e"]
reveal_type(s[-2])  # revealed: Literal["d"]

reveal_type(s[False])  # revealed: Literal["a"]
reveal_type(s[True])  # revealed: Literal["b"]

a = s[8]  # error: [index-out-of-bounds] "Index 8 is out of bounds for string `Literal[\"abcde\"]` with length 5"
reveal_type(a)  # revealed: Unknown

b = s[-8]  # error: [index-out-of-bounds] "Index -8 is out of bounds for string `Literal[\"abcde\"]` with length 5"
reveal_type(b)  # revealed: Unknown

def _(n: int):
    a = "abcde"[n]
    reveal_type(a)  # revealed: LiteralString
```

----------------------------------------

TITLE: Unioning Classes with `|` Operator (Python 3.10+)
DESCRIPTION: This snippet demonstrates how to union two classes using the `|` operator, a feature introduced in Python 3.10. It includes the `toml` configuration to specify the Python version and the Python code showing the `reveal_type` output as `UnionType`.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/binary/classes.md#_snippet_0

LANGUAGE: TOML
CODE:
```
[environment]
python-version = "3.10"
```

LANGUAGE: Python
CODE:
```
class A: ...
class B: ...

reveal_type(A | B)  # revealed: UnionType
```

----------------------------------------

TITLE: Defining Generic Methods within Python Generic Classes
DESCRIPTION: This snippet demonstrates how to define methods that are themselves generic within a generic class. It shows that generic methods can refer to the type variables of the enclosing generic class and also introduce new, distinct type variables that are only in scope for that specific method.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/generics/pep695/classes.md#_snippet_26

LANGUAGE: Python
CODE:
```
class C[T]:
    def method[U](self, u: U) -> U:
        return u
    # error: [unresolved-reference]
    def cannot_use_outside_of_method(self, u: U): ...

    # TODO: error
    def cannot_shadow_class_typevar[T](self, t: T): ...

c: C[int] = C[int]()
reveal_type(c.method("string"))  # revealed: Literal["string"]
```

----------------------------------------

TITLE: Narrowing with Single Type `isinstance` Checks in Python
DESCRIPTION: This snippet demonstrates type narrowing when `isinstance` is used with a single type or a simple tuple of types. It shows how the type of a variable `x` is refined to `Literal[1]` when checked against `int` and `Literal["a"]` when checked against `str`. It also illustrates how `reveal_type` shows `Never` for impossible paths and how `object` in a tuple doesn't narrow.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/narrow/isinstance.md#_snippet_0

LANGUAGE: Python
CODE:
```
def _(flag: bool):
    x = 1 if flag else "a"

    if isinstance(x, int):
        reveal_type(x)  # revealed: Literal[1]

    if isinstance(x, str):
        reveal_type(x)  # revealed: Literal["a"]
        if isinstance(x, int):
            reveal_type(x)  # revealed: Never

    if isinstance(x, (int, object)):
        reveal_type(x)  # revealed: Literal[1, "a"]
```

----------------------------------------

TITLE: Ruff Configuration in pyproject.toml (Line Length and Docstrings)
DESCRIPTION: This `pyproject.toml` snippet illustrates a basic Ruff configuration, setting the `line-length` to 88 and specifying the `google` docstring convention. It shows the standard `[tool.ruff]` section header required when configuring Ruff within `pyproject.toml`.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/faq.md#_snippet_20

LANGUAGE: TOML
CODE:
```
[tool.ruff]
line-length = 88

[tool.ruff.lint.pydocstyle]
convention = "google"
```

----------------------------------------

TITLE: Handling Exceptions with Finally and Variable Redefinition in Python
DESCRIPTION: This snippet demonstrates type inference behavior in a `try-except-finally` block. It shows how the type of variable `x` changes based on the execution path (try, except) and how it's re-assigned within the `finally` block, affecting its type after the block. The `reveal_type` comments indicate the inferred types at different stages, highlighting current inference limitations in the `finally` suite.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/exception/control_flow.md#_snippet_8

LANGUAGE: Python
CODE:
```
class A: ...
class B: ...
class C: ...

def could_raise_returns_A() -> A:
    return A()

def could_raise_returns_B() -> B:
    return B()

def could_raise_returns_C() -> C:
    return C()

x = 1

try:
    reveal_type(x)  # revealed: Literal[1]
    x = could_raise_returns_A()
    reveal_type(x)  # revealed: A
except TypeError:
    reveal_type(x)  # revealed: Literal[1] | A
    x = could_raise_returns_B()
    reveal_type(x)  # revealed: B
    x = could_raise_returns_C()
    reveal_type(x)  # revealed: C
finally:
    # TODO: should be `Literal[1] | A | B | C`
    reveal_type(x)  # revealed: A | C
    x = 2
    reveal_type(x)  # revealed: Literal[2]

reveal_type(x)  # revealed: Literal[2]
```

----------------------------------------

TITLE: Handling Multiple Exceptions with `except*` (Python)
DESCRIPTION: This Python example illustrates catching an `ExceptionGroup` that may contain either `TypeError` or `AttributeError` instances using `except* (TypeError, AttributeError)`. The `e` variable's type is `ExceptionGroup[TypeError | AttributeError]`, allowing for handling a group of specified exceptions.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/exception/except_star.md#_snippet_3

LANGUAGE: py
CODE:
```
try:
    help()
except* (TypeError, AttributeError) as e:
    reveal_type(e)  # revealed: ExceptionGroup[TypeError | AttributeError]
```

----------------------------------------

TITLE: Detecting Calls to Non-Callable Objects in Python
DESCRIPTION: Checks for attempts to call non-callable objects. Calling a non-callable object will result in a `TypeError` at runtime, indicating a fundamental programming error that should be caught during static analysis.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty/docs/rules.md#_snippet_1

LANGUAGE: Python
CODE:
```
4()  # TypeError: 'int' object is not callable
```

----------------------------------------

TITLE: Annotating Non-Returning Functions with Never - Python
DESCRIPTION: This snippet demonstrates how `Never` is used as a return type annotation for functions that are guaranteed never to return control to their caller. This includes functions that always raise an exception, call `sys.exit()`, enter an infinite loop, or recursively call themselves indefinitely.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/type_compendium/never.md#_snippet_2

LANGUAGE: Python
CODE:
```
from typing_extensions import Never

def raises_unconditionally() -> Never:
    raise Exception("This function always raises an exception")

def exits_unconditionally() -> Never:
    import sys

    return sys.exit(1)

def loops_forever() -> Never:
    while True:
        pass

def recursive_never() -> Never:
    return recursive_never()
```

----------------------------------------

TITLE: Detecting Possibly Unbound Attributes in Python
DESCRIPTION: This check identifies instances where an attribute might be accessed before it has been bound to an object. Attempting to access such an attribute will result in an AttributeError at runtime, indicating that the attribute does not exist on the object. This helps prevent runtime attribute access errors.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty/docs/rules.md#_snippet_51

LANGUAGE: python
CODE:
```
class A:
    if b:
        c = 0

A.c  # AttributeError: type object 'A' has no attribute 'c'
```

----------------------------------------

TITLE: Performing Basic Arithmetic Operations on Integers in Python
DESCRIPTION: This snippet demonstrates various binary arithmetic operations (addition, subtraction, multiplication, floor division, true division, modulo, bitwise OR, AND, XOR) on integer literals and variables in Python. It also shows type inference results using `reveal_type` and an example of an unsupported operation.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/binary/integers.md#_snippet_0

LANGUAGE: Python
CODE:
```
reveal_type(2 + 1)  # revealed: Literal[3]
reveal_type(3 - 4)  # revealed: Literal[-1]
reveal_type(3 * -1)  # revealed: Literal[-3]
reveal_type(-3 // 3)  # revealed: Literal[-1]
reveal_type(-3 / 3)  # revealed: float
reveal_type(5 % 3)  # revealed: Literal[2]
reveal_type(3 | 4)  # revealed: Literal[7]
reveal_type(5 & 6)  # revealed: Literal[4]
reveal_type(7 ^ 2)  # revealed: Literal[5]

# error: [unsupported-operator] "Operator `+` is unsupported between objects of type `Literal[2]` and `Literal["f"]`"
reveal_type(2 + "f")  # revealed: Unknown

def lhs(x: int):
    reveal_type(x + 1)  # revealed: int
    reveal_type(x - 4)  # revealed: int
    reveal_type(x * -1)  # revealed: int
    reveal_type(x // 3)  # revealed: int
    reveal_type(x / 3)  # revealed: int | float
    reveal_type(x % 3)  # revealed: int

def rhs(x: int):
    reveal_type(2 + x)  # revealed: int
    reveal_type(3 - x)  # revealed: int
    reveal_type(3 * x)  # revealed: int
    reveal_type(-3 // x)  # revealed: int
    reveal_type(-3 / x)  # revealed: int | float
    reveal_type(5 % x)  # revealed: int

def both(x: int):
    reveal_type(x + x)  # revealed: int
    reveal_type(x - x)  # revealed: int
    reveal_type(x * x)  # revealed: int
    reveal_type(x // x)  # revealed: int
    reveal_type(x / x)  # revealed: int | float
    reveal_type(x % x)  # revealed: int
```

----------------------------------------

TITLE: Parameterizing Python Literal Types
DESCRIPTION: This snippet demonstrates various ways to parameterize `typing.Literal` with different literal values, including integers, strings, bytes, booleans, None, and enum members. It also shows examples of invalid literal forms such as expressions or tuples.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/annotations/literal.md#_snippet_0

LANGUAGE: Python
CODE:
```
from typing import Literal
from enum import Enum

mode: Literal["w", "r"]
a1: Literal[26]
a2: Literal[0x1A]
a3: Literal[-4]
a4: Literal["hello world"]
a5: Literal[b"hello world"]
a6: Literal[True]
a7: Literal[None]
a8: Literal[Literal[1]]

class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

b1: Literal[Color.RED]

def f():
    reveal_type(mode)  # revealed: Literal["w", "r"]
    reveal_type(a1)  # revealed: Literal[26]
    reveal_type(a2)  # revealed: Literal[26]
    reveal_type(a3)  # revealed: Literal[-4]
    reveal_type(a4)  # revealed: Literal["hello world"]
    reveal_type(a5)  # revealed: Literal[b"hello world"]
    reveal_type(a6)  # revealed: Literal[True]
    reveal_type(a7)  # revealed: None
    reveal_type(a8)  # revealed: Literal[1]
    # TODO: This should be Color.RED
    reveal_type(b1)  # revealed: @Todo(Attribute access on enum classes)

# error: [invalid-type-form]
invalid1: Literal[3 + 4]
# error: [invalid-type-form]
invalid2: Literal[4 + 3j]
# error: [invalid-type-form]
invalid3: Literal[(3, 4)]

hello = "hello"
invalid4: Literal[
    1 + 2,  # error: [invalid-type-form]
    "foo",
    hello,  # error: [invalid-type-form]
    (1, 2, 3)  # error: [invalid-type-form]
]
```

----------------------------------------

TITLE: Basic Method Calls on Class and Instance Objects
DESCRIPTION: This comprehensive snippet demonstrates calling methods on both base and derived class instances, as well as directly on class objects by explicitly passing an instance. It also includes examples of common type-checking errors for method arguments.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/call/methods.md#_snippet_8

LANGUAGE: Python
CODE:
```
class Base:
    def method_on_base(self, x: int | None) -> str:
        return "a"

class Derived(Base):
    def method_on_derived(self, x: bytes) -> tuple[int, str]:
        return (1, "a")

reveal_type(Base().method_on_base(1))  # revealed: str
reveal_type(Base.method_on_base(Base(), 1))  # revealed: str

Base().method_on_base("incorrect")  # error: [invalid-argument-type]
Base().method_on_base()  # error: [missing-argument]
Base().method_on_base(1, 2)  # error: [too-many-positional-arguments]

reveal_type(Derived().method_on_base(1))  # revealed: str
reveal_type(Derived().method_on_derived(b"abc"))  # revealed: tuple[int, str]
reveal_type(Derived.method_on_base(Derived(), 1))  # revealed: str
reveal_type(Derived.method_on_derived(Derived(), b"abc"))  # revealed: tuple[int, str]
```

----------------------------------------

TITLE: Defining Generic PEP 695 Type Aliases (Python)
DESCRIPTION: This Python snippet demonstrates how to define generic PEP 695 type aliases using type parameters. `ListOrSet[T]` allows the alias to work with different types `T`. `reveal_type` on `__type_params__` shows the type variables associated with the generic alias.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/pep695_type_aliases.md#_snippet_6

LANGUAGE: py
CODE:
```
type ListOrSet[T] = list[T] | set[T]
reveal_type(ListOrSet.__type_params__)  # revealed: tuple[TypeVar | ParamSpec | TypeVarTuple, ...]
```

----------------------------------------

TITLE: Guard and Reveal Type in Guard in Python Match
DESCRIPTION: This Python code demonstrates the interaction of `reveal_type` within `if` guards in `match` statements. It shows that `reveal_type` reflects the type narrowing that has occurred up to the point of the guard's evaluation, even when combined with logical `and` operators.
SOURCE: https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/narrow/match.md#_snippet_9

LANGUAGE: Python
CODE:
```
def get_object() -> object:
    return object()

x = get_object()

reveal_type(x)  # revealed: object

match x:
    case str() | float() if type(x) is str and reveal_type(x):  # revealed: str
        pass
    case "foo" | 42 | None if isinstance(x, int) and reveal_type(x):  #  revealed: Literal[42]
        pass
    case False if x and reveal_type(x):  #  revealed: Never
        pass
    case "foo" if (x := "bar") and reveal_type(x):  #  revealed: Literal["bar"]
        pass

reveal_type(x)  # revealed: object
```

----------------------------------------

TITLE: Excluding Jupyter Notebooks from Ruff Formatting (TOML)
DESCRIPTION: This configuration prevents Ruff from formatting Jupyter Notebook (`.ipynb`) files, while still allowing them to be linted. It applies the `exclude` setting specifically to the `format` tool table, demonstrating selective application of rules.
SOURCE: https://github.com/astral-sh/ruff/blob/main/docs/configuration.md#_snippet_11

LANGUAGE: TOML
CODE:
```
[tool.ruff.format]
exclude = ["*.ipynb"]
```

LANGUAGE: TOML
CODE:
```
[format]
exclude = ["*.ipynb"]
```