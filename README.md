# 🐍 Python Compiler Project

> **This project is still in development!** ⚠️

## 📋 Description

This Python-based compiler is built from scratch, focusing on the frontend of a compiler pipeline. The goal of this project is to provide an in-depth understanding of how a compiler works, from reading files and handling command-line arguments to performing lexical, syntactical, and semantic analysis.

## 📑 Table of Contents

- [🐍 Python Compiler Project](#-python-compiler-project)
  - [📋 Description](#-description)
  - [📑 Table of Contents](#-table-of-contents)
  - [📁 Project Structure](#-project-structure)
    - [📂 Folders and Files Description](#-folders-and-files-description)
  - [🛠️ Getting Started](#️-getting-started)
    - [📋 Requirements](#-requirements)
    - [⚙️ Installation](#️-installation)
    - [🖥️ Usage](#️-usage)
  - [🔄 Current Status](#-current-status)
  - [🤝 Contributing](#-contributing)
  - [📜 License](#-license)

## 📁 Project Structure

The project structure is organized as follows, considering future implementations of the other compiler stages:

```
.
├── README.md
├── docs
├── scripts
│   └── run_rpl.py
├── src
│   ├── codegen
│   ├── interpreter
│   │   ├── __pycache__
│   │   │   ├── repl.cpython-313.pyc
│   │   │   └── repl.cpython-38.pyc
│   │   └── repl.py
│   ├── lexer
│   │   ├── error_handler.py
│   │   ├── keywords.py
│   │   ├── scanner.py
│   │   ├── token.py
│   │   └── token_type.py
│   ├── optimization
│   ├── parser
│   ├── semantic
│   └── utils
│       ├── __pycache__
│       │   ├── file_handler.cpython-313.pyc
│       │   └── file_handler.cpython-38.pyc
│       └── file_handler.py
└── test
```

### 📂 Folders and Files Description

> 💡 The project follows a modular architecture where each component of the compiler pipeline has its own directory.

- **docs**: Project documentation.
- **scripts**: Scripts to run and test the project.
  - `run_rpl.py`: Script to run the REPL or read a file.
- **src**: Compiler source code.
  - **codegen**: Code generation (future implementation).
  - **interpreter**: Interpreter implementation.
    - `repl.py`: Module that implements the REPL (Read-Eval-Print Loop).
  - **lexer**: Lexical analysis.
    - `error_handler.py`: Lexical error handling.
    - `keywords.py`: Reserved words handling.
    - `scanner.py`: Lexical analyzer that converts source code into tokens.
    - `token.py`: Class that represents a token.
    - `token_type.py`: Enumeration of supported token types.
  - **optimization**: Code optimization (future implementation).
  - **parser**: Syntactic analysis (future implementation).
  - **semantic**: Semantic analysis (future implementation).
  - **utils**: General utilities.
    - `file_handler.py`: File handling and input/output.
- **test**: Project tests.

## 🛠️ Getting Started

### 📋 Requirements

- Python 3.8 or higher

### ⚙️ Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your_username/compyler.git
   cd compyler
   ```

2. Install dependencies (if any):
   ```sh
   pip install -r requirements.txt
   ```

### 🖥️ Usage

> ⚠️ **Note**: The project is currently in its early stages, focusing on lexical analysis.

To start the REPL:
```sh
python scripts/run_rpl.py
```

To read and process a file:
```sh
python scripts/run_rpl.py path/to/file.txt
```

## 🔄 Current Status

- ✅ Lexical Analysis (Scanner/Tokenizer)
- 🔄 Syntax Analysis (Parser) - In Progress
- ⏳ Semantic Analysis - Planned
- ⏳ Code Generation - Planned

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.