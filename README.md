# 📁 Directory Structure Analyzer & Builder

This Python tool provides a minimal GUI (via Tkinter) for **analyzing** and **rebuilding** directory structures based on `.txt` files. It supports two main operations:

- **Analyze**: Generate `.txt` representations (tree and flat) from an existing directory.
- **Build**: Create a directory and file structure from a `structure.txt` file (tree-style).

---

## ✨ Features

- Tree-style parsing and creation (using `├──`, `└──`, and indentation)
- Flat path output (for scripting or logs)
- Cross-platform support (uses only Python standard library)
- GUI-based file/folder selection
- Avoids overwriting existing files

---

## 🔧 Requirements

- Python 3.6+
- Tkinter (usually included with Python)

---

## 🚀 How to Use

### Run the Tool

```bash
python main.py
```

You will be prompted to choose a mode:
1 - Create structure
2 - Analyze folder

## Mode 1: Create Structure
Select a structure.txt file (tree-style format).

Choose a destination folder.

The tool creates all folders and empty files based on the tree structure.

Example of a valid structure.txt:
```bash
├── src/
│   ├── main.py
│   └── utils/
│       └── helpers.py
├── README.md
└── requirements.txt
```

## Mode 2: Analyze Folder
Select the folder you want to analyze.

Choose where to save:

A tree-style .txt file.

A flat list .txt file (relative paths).

The tool generates two output files.

Output Example
Tree Structure (tree_output.txt)
```bash
├── src/
│   ├── main.py
│   └── utils/
│       └── helpers.py
├── README.md
└── requirements.txt
```
Flat Structure (flat_output.txt)
```bash
project/src/
project/src/main.py
project/src/utils/
project/src/utils/helpers.py
project/README.md
project/requirements.txt
```

## Purpose
This application is designed to facilitate the maintenance, visualization, and restructuring of project directory hierarchies. By enabling bidirectional conversion between actual filesystem layouts and their text-based representations, it serves as a practical tool for:

Quickly visualizing complex directory structures in a human-readable format (tree or flat),

Easily reorganizing or reconstructing project layouts from editable .txt files,

Extracting file and folder paths for integration with scripts, documentation, or automation workflows.

It is particularly suited for development environments where project organization, consistency, and reproducibility are critical. Through a lightweight GUI, users can abstract and manage file structures without directly interacting with the filesystem, supporting a more controlled and modular approach to structural maintenance.