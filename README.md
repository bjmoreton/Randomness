# Script Collection

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)  
**Author:** Richard Moreton  
**Description:** A collection of PowerShell, Python, C#, and other utility scripts for various tasks. Each script is documented individually and licensed under Apache 2.0.

---

## Table of Contents

- [Script Collection](#script-collection)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Scripts](#scripts)
    - [PowerShell](#powershell)
      - [cdnum](#cdnum)
        - [Description](#description-1)
        - [Features](#features)
        - [Installation](#installation)
        - [Usage](#usage)
        - [Examples](#examples)
    - [Python](#python)
      - [colors.py](#colorspy)
        - [Description](#description-2)
        - [Features](#features-1)
        - [Installation](#installation-1)
        - [Usage](#usage-1)
        - [Examples](#examples-1)
      - [dynamic_validator](#dynamic_validator)
        - [Description](#description-3)
        - [Features](#features-2)
        - [Installation](#installation-2)
        - [Usage](#usage-2)
        - [Examples](#examples-2)

---

## Description

This repository contains a collection of scripts in multiple programming languages.  
The goal is to provide small, reusable utilities for common tasks such as:

- Directory navigation
- File management
- Automation tasks
- Data processing

Each script or module is documented individually with usage instructions and examples.

---

## Scripts

### PowerShell

#### cdnum

###### Description

Quickly navigate upward through directory hierarchies using a numeric argument.

**Alias:** `..n` example `..n 2`

###### Features

- Move up N directories with `cdnum N`.
- Show current directory and depth with `cdnum`.
- Tab-completion for numbers 1–10.
- Alias `..n` for shorthand.

###### Installation

Place the `cdnum.psm1` file in your PowerShell Modules folder:

```text
$HOME\Documents\WindowsPowerShell\Modules\cdnum\
```

###### Usage

Import the module to use `cdnum`:

```powershell
Import-Module cdnum
```

or

Add the module to your PowerShell profile manually:

```powershell
Add-Content -Path $PROFILE -Value 'Import-Module cdnum'
. $PROFILE
```

###### Examples

Move up one directory:

```powershell
cdnum 1
```

Move up two directories:

```powershell
cdnum 2
```

Using alias:

```powershell
..n 3
```

Display current directory and depth:

```powershell
cdnum
```

### Python

#### colors.py

###### Description

A Python module providing ANSI color codes for terminal text and background styling.  
Supports standard colors, bright variants, 256-color mode, and blink effects.  
Includes functions to parse custom color codes in strings and print colored output.

###### Features

- Standard and bright text colors.
- Standard and bright background colors.
- Blink effect support.
- 256-color foreground and background support.
- Parse custom placeholders (e.g., `&r` for bright red, `}&lt;number&gt;` for 256-color).
- `print_color()` function for easy terminal output.

###### Installation

Place `colors.py` in your project directory or a folder in your Python PATH.  
Import the module in your scripts:

```python
from colors import Colors, parse_colors, print_color
```

###### Usage

Parse and print colored text:

```python
from colors import print_color

# Parse and print a string with custom codes
print_color("&rThis is bright red text&~")

# Use 256-color codes
print_color("This is }196 red text")
```

Directly use Colors constants:

```python
from colors import Colors

print(f"{Colors.brightGreen}This text is bright green{Colors.reset}")
print(f"{Colors.bgColor256(214)}This background is bright orange{Colors.reset}")
```

###### Examples

Basic usage:

```python
from colors import print_color

print_color("&BBlue text&~ and &Yyellow text&~")
print_color("Custom 256-color }42 greenish text&~")
```

Combining foreground and background:

```python
from colors import Colors

print(f"{Colors.brightWhite}{Colors.bgRed}White on red background{Colors.reset}")
```

#### dynamic_validator

###### Description

A flexible validation orchestrator that supports both synchronous and asynchronous rules.
It allows defining rules, managing them dynamically, and validating values using various strategies (all, any, one).

###### Features

- **Mixed Sync/Async Support**: Handle both synchronous and asynchronous validation checks transparently.
- **Dynamic Rule Management**: Add or remove rules at runtime.
- **Validation Strategies**:
  - `is_valid` / `all_of`: Ensure all rules pass.
  - `any_of`: Ensure at least one rule passes.
  - `one_of`: Ensure exactly one rule passes.
- **Detailed Errors**: Returns structured `ValidationError` objects with context.

###### Installation

Place the `dynamic_validator` folder in your project directory.
Import the `DynamicValidator` class:

```python
from dynamic_validator.dynamic_validator import DynamicValidator
```

###### Usage

Initialize the validator and add rules:

```python
from dynamic_validator.dynamic_validator import DynamicValidator

validator = DynamicValidator()

# Add a rule using a lambda
validator.add_rule(
    "PASSWORD_LENGTH",
    lambda p, **kwargs: len(p) >= 8,
    "Password must be at least 8 characters"
).add_rule(
    "PASSWORD_NO_EMAIL_USERNAME",
    lambda p, email=None, **kwargs: (
        email.split("@")[0].lower() not in p.lower() if email else True
    ),
    "Password must not contain your e-mail username"
)

# Add a rule using a function
def is_even(value, **kwargs):
    return value % 2 == 0

validator.add_rule("is_even", is_even, "Value must be even")
```

###### Examples

Validate a value:

```python
# Check if all rules pass
is_valid, errors = validator.is_valid(10)
if is_valid:
    print("Validation passed!")
else:
    for error in errors:
        print(f"Rule {error.rule} failed: {error.message}")
```

Async usage:

```python
import asyncio

async def check_db(value, **kwargs):
    # Simulate async DB check
    await asyncio.sleep(0.1)
    return True

validator.add_rule("db_check", check_db, "DB check failed")

# Must await if using async rules or in async context
is_valid, errors = await validator.is_valid(10)
```
