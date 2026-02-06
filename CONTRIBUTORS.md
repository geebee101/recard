---
title: CONTRIBUTORS
author: gpr
date: 2026-01-10
description: Laying out our rules, workflows and tools for all contributors and maintainers
---

# Contributors pls follow this

We don't care how you wrote your PR, AI our not. 
But guess what, we do care whether it is sloppy or not. If it is sloppy, we will not review it. And as we already spent too much time discovering that it was sloppy, we are not likely to spend more by commenting. Period. There is no appeal process. Just do better.


## THIS PROJECT


## TOOLS

### dev tools
Note: these instructions are for a local first project, they do not apply to collaboration on a project that we do not own.
* Any tool: start by running: the_tool --help or -h

#### Version control
* Version control, etc.: github and/or tangled are used. This means that individual projects might use either or both. Actual workflow is also project dependent.
* Setting up and preparing the environment, checking current status:
1. In a workaread, create a directory with the short project name, with a subdirectory: _workfiles
2. Create a new git repository: git init
3. Create .gitignore from a template

. Verify status: git status
* Define your remote with explicit names, e.g. 'tangled', 'github', NOT 'origin', 'github'
Useful commands and workflow:
  1. Review that your changes haven't revealed any secret
  2. git add :
  3. git commit -m <COMMIT MESSAGE>
      The <COMMIT MESSAGE> is a short string describing the *intent* of the changes, not a description or list of changes, which is what diff is for.
  4. git push <REMOTE> <OPT.BRANCH>
      <REMOTE> is typically 'tangled' and/or 'github'
* Other useful git commands: git log / git diff

### LANGUAGE: python Best Practices

#### Code Style
* Style guide: PEP8,  google style guide PGSG, at https://google.github.io/styleguide/pyguide.html
    https://peps.python.org/pep-0008/
Follow the PGSG where it makes sense. If a contributor encounters discrepancies between PGSG and the lint results, they should be analyzed and presented to maintainers, with a recommendation of either changing the settings of the linter or not applying a specific rule of the PGSG in a given case, or both.
- Use type hints for function signatures
* use pydantic for pre-emptive validation, not just types, but ranges, invalid values or formats, etc.
- Use `ruff` for formatting, `ruff` for linting
- Prefer `pathlib.Path` over `os.path` for path operations
- Use context managers (`with`) for file operations

#### Code documentation
* Use docstrings, PEP257 (docstrings), https://peps.python.org/pep-0257/
* document with docstring (PEP257)- ignore small functions and properties: getters, setters, one-liners, or no complex logic. Docstrings on these just add verbosity. Note ruff ignores properties as standard.
* docstrings will not update automatically example code, snips, tutorials and how-tos, contributors do!
* Generating docs: mkdocs (opt. Material for mkdocs TODO repo in maintenance, will they remove repo, should we clone???)
* Useful commands: TODO

#### Error Handling
```python
# GOOD: Specific exceptions with context
def read_config(path: Path) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ConfigError(f"Config file not found: {path}")
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in {path}: {e}")

# BAD: Bare except or swallowing errors with Exception
```
* prefer early returns over nested ifs.
* if not stated elsewhere in ref, use properties @property, rather than getters/setters.

#### Security
- Never use `eval()` or `exec()` on user input
- Use `subprocess.run()` with explicit args, never `shell=True` with user input
- Use parameterized queries for SQL (never f-strings)
- Validate and sanitize all external input

#### Dependencies, Env management, packaging
- Manage virtual environments, packages and final product build (packaging): Astral uv
- Pin dependency versions in 'pyproject.toml' and 'uv.lock'
- Use virtual environments 
- Run 'uv-secure' or `pip-audit` to check for vulnerabilities
Useful commands: ```
uv install <PACKAGE>
uv init to create an environment
uv run pytest
uv tool install uv-secure
uv tool install ruff
uv run pytest
uv add --dev pytest-cov
uv run pytest --cov=lexicard --cov-report=html
```

#### Testing
- Use `pytest` for testing
- Aim for high coverage with `pytest-cov`
- Mock external dependencies with `unittest.mock`

#### lambda and higher-order functions
About lambda functions and higher-order functions:  
* Use a list comprehension when you need to create a new list based on an existing one, or if you are applying simple transformations and filtering.
* Use a lambda function when you need a simple, temporary function as an argument to a higher-order function (like sorted(), min(), or a GUI callback).
* generally prefers list comprehensions over map() or filter() with a lambda because they combine the transformation and iteration logic into a single, highly readable construct. 

When lambda is the better choice, then:
* Keep lambda function bodies to a single, simple expression
* Use descriptive variable names (e.g., lambda student: student.grade)
* For complex logic, always prefer a standard def function
* For pydantic buttons, lambda can be used if simple and for pydantic functionality. Application logic should be in defined functions.

#### python libraries
* pydantic + Fast API
* nicegui

### IDE: Antigravity
This may vary for each developer. Abbreviation IDEAG
Useful commands: 
* `Ctrl + ,` Open Settings from anywhere.
* `Ctrl + E` toggle Agent and Editor windows



### QUALITY CONTROL
testing: pytest with coverage module and 
In IDEAG, UI testing should use the builtin Chrome.
* Testing: pytest TODO useful cmds, default setup?
Ignore properties, getters, setters, the goal is not to produce exhaustive unit tests, but to validate the behaviour of the product against the design goals and requirements.
* coverage should be 100% at all times. Small functions and properties do not need unit test, they need to be covered.

lint: ruff
format: ruff
* Lint, format: ruff. TODO useful cmds, specific settings if any
