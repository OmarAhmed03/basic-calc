# Basic-calc
## Overview

Basic-calc is a GUI application for solving and plotting mathematical functions. It provides a user-friendly interface to input mathematical expressions, solve equations, and visualize the results using plots.

## Features

- Solve linear, quadratic, and logarithmic equations.
- Plot functions and their solutions.
- Modern and intuitive GUI built with PySide2.
- Expression validation and formatting.
- Interactive input panel with expression buttons.

## Installation

To install the required dependencies, run:
```sh
pip install -r requirements.txt
```

## Usage

To start the application, run:
```sh
python src/main.py
```

## Project Structure

- `src/`: Contains the source code for the application.
    - `core/`: Core logic for equation solving and expression parsing.
    - `gui/`: GUI components including the main window, input panel, and plot widget.
    - `utils/`: Utility constants and theme management.
    - `tests/`: Unit tests for the application.
- `requirements.txt`: List of dependencies.
- `readme.md`: Project documentation.

## Running Tests

To run the tests, use:
```sh
pytest
```
## Snapshots

![image](https://github.com/user-attachments/assets/3c781877-1637-4be1-af98-1912b7aa9c21)

![image](https://github.com/user-attachments/assets/612df8ae-a2c3-4538-ae8b-1875bdd800ab)


## License

This project is licensed under the MIT License.
