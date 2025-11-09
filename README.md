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
