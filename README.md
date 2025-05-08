<!-- omit from toc -->
# 🐍 Python Compiler Project

> **This project is currently in development!** ⚠️

<!-- omit from toc -->
## 📋 Description

This Python-based compiler is built from scratch, focusing on the frontend of a compiler pipeline. The goal is to provide an in-depth understanding of how compilers work.

<!-- omit from toc -->
## 📑 Table of Contents

- [📁 Project Structure](#-project-structure)
- [🛠️ Getting Started](#️-getting-started)
  - [📋 Requirements](#-requirements)
  - [⚙️ Installation](#️-installation)
  - [🖥️ Usage](#️-usage)
- [🔄 Current Status](#-current-status)

## 📁 Project Structure
The project structure is organized as follows:
```
.
├── README.md
├── main.py                # Main entry point
├── setup.py               # Environment setup
├── src
│   ├── interpreter        # Interpreter
│   │   └── repl.py        # REPL implementation
│   ├── lexer              # Lexical analysis
│   │   ├── error_handler.py  # Lexical error handling
│   │   ├── keywords.py    # Reserved keywords
│   │   ├── scanner.py     # Lexical analyzer
│   │   ├── token.py       # Token class
│   │   └── token_type.py  # Token types
│   ├── parser             # Syntactic analysis
│   │   └── parser.py      # Parser implementation
│   ├── semantic           # Semantic analysis (planned)
│   └── utils              # Utilities
│       └── file_handler.py # File handling
└── test                   # Tests
    ├── lexer              # Lexical analyzer tests
    └── parser             # Parser tests
```

## 🛠️ Getting Started

### 📋 Requirements

- Python 3.8 or higher

### ⚙️ Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your_username/compyler.git
   cd compyler
   ```

2. Set up a virtual environment (recommended):
   ```sh
   python -m venv env
   ```

3. ⚠️ **Important! Before proceeding, ensure the environment is properly initialized. Run this command in the powershell terminal** ⚠️
   ```sh
   .\env\Scripts\activate # (THIS COMMAND IS FOR WINDOWS)
   ```

4. Then, install the project in development mode:
   ```sh
   pip install -e .
   ```

### 🖥️ Usage

- **Start the REPL (interactive mode)**:
  ```sh
  python main.py
  ```

- **Process a source file**:
  ```sh
  python main.py path/to/file.txt
  ```

## 🔄 Current Status

- ✅ Lexical Analysis (Scanner/Tokenizer)
- ✅ Syntax Analysis (Parser)
- ⏳ Semantic Analysis - In progress