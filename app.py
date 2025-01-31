# main.py
import sys
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout,
                             QMessageBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from sympy import symbols, sympify, solve, log, sqrt
import re

class MathPlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Solver & Plotter")
        self.setGeometry(100, 100, 1000, 800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create input section
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        # Function input fields
        func1_layout = QHBoxLayout()
        func1_label = QLabel("Function 1:")
        self.func1_input = QLineEdit()
        self.func1_input.setPlaceholderText("Enter function (e.g., 5*x^3 + 2*x)")
        func1_layout.addWidget(func1_label)
        func1_layout.addWidget(self.func1_input)
        
        func2_layout = QHBoxLayout()
        func2_label = QLabel("Function 2:")
        self.func2_input = QLineEdit()
        self.func2_input.setPlaceholderText("Enter function (e.g., 3*x^2 - 1)")
        func2_layout.addWidget(func2_label)
        func2_layout.addWidget(self.func2_input)
        
        # Expression buttons
        expr_layout = QGridLayout()
        expressions = [
            ('x', 'x'), ('^', '^'), ('√', 'sqrt('),
            ('+', '+'), ('-', '-'), ('*', '*'),
            ('/', '/'), ('(', '('), (')', ')'),
            ('log10', 'log10('), ('Clear', 'CLEAR')
        ]
        
        row, col = 0, 0
        for display_text, expr in expressions:
            button = QPushButton(display_text)
            button.clicked.connect(lambda checked=False, e=expr: self.add_expression(e))
            expr_layout.addWidget(button, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1
        
        # Solve and Plot button
        solve_button = QPushButton("Solve and Plot")
        solve_button.clicked.connect(self.solve_and_plot)
        
        # Add input widgets to input layout
        input_layout.addLayout(func1_layout)
        input_layout.addLayout(func2_layout)
        input_layout.addLayout(expr_layout)
        input_layout.addWidget(solve_button)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        
        # Create result label
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        
        # Add all widgets to main layout
        layout.addWidget(input_widget)
        layout.addWidget(self.canvas)
        layout.addWidget(self.result_label)
        
        # Track active input field
        self.active_input = self.func1_input
        self.func1_input.focusInEvent = lambda e: self.set_active_input(self.func1_input)
        self.func2_input.focusInEvent = lambda e: self.set_active_input(self.func2_input)
        
    def set_active_input(self, input_field):
        """Set the currently active input field."""
        self.active_input = input_field
        
    def add_expression(self, expr):
        """Add the selected expression to the active input field."""
        if expr == 'CLEAR':
            self.active_input.clear()
        else:
            cursor_pos = self.active_input.cursorPosition()
            current_text = self.active_input.text()
            new_text = current_text[:cursor_pos] + expr + current_text[cursor_pos:]
            self.active_input.setText(new_text)
            self.active_input.setFocus()
            self.active_input.setCursorPosition(cursor_pos + len(expr))
            
    def validate_expression(self, expr):
        """Validate the mathematical expression."""
        if not expr:
            return False, "Expression cannot be empty"
            
        # Check for valid operators and functions
        valid_chars = set('x0123456789+-*/^() ')
        valid_funcs = {'log10', 'sqrt'}
        
        # Remove valid functions from expression for checking
        temp_expr = expr
        for func in valid_funcs:
            temp_expr = temp_expr.replace(func, '')
            
        # Check remaining characters
        if not all(c in valid_chars for c in temp_expr):
            return False, "Invalid characters in expression"
            
        # Check balanced parentheses
        if expr.count('(') != expr.count(')'):
            return False, "Unbalanced parentheses"
            
        return True, ""
        
    def format_expression(self, expr):
        """Format the expression for sympy parsing."""
        # Replace ^ with **
        expr = expr.replace('^', '**')
        
        # Add multiplication symbols where needed
        expr = re.sub(r'(\d)x', r'\1*x', expr)
        expr = re.sub(r'\)(\w)', r')*\1', expr)
        expr = re.sub(r'(\d)\(', r'\1*(', expr)
        
        return expr
        
    def solve_and_plot(self):
        """Solve the equations and create the plot."""
        try:
            # Get and validate expressions
            func1_str = self.func1_input.text()
            func2_str = self.func2_input.text()
            
            valid1, msg1 = self.validate_expression(func1_str)
            valid2, msg2 = self.validate_expression(func2_str)
            
            if not valid1 or not valid2:
                QMessageBox.warning(self, "Invalid Input", 
                                  f"Function 1: {msg1}\nFunction 2: {msg2}")
                return
                
            # Format expressions
            func1_str = self.format_expression(func1_str)
            func2_str = self.format_expression(func2_str)
            
            # Create symbolic variable and expressions
            x = symbols('x')
            func1 = sympify(func1_str)
            func2 = sympify(func2_str)
            
            # Solve the equation
            equation = func1 - func2
            solutions = solve(equation, x)
            
            # Convert solutions to float for plotting
            solutions = [complex(sol).real for sol in solutions if complex(sol).imag == 0]
            
            if not solutions:
                self.result_label.setText("No real solutions found")
                return
                
            # Create x values for plotting
            x_min = min(solutions) - 2
            x_max = max(solutions) + 2
            x_vals = np.linspace(x_min, x_max, 1000)
            
            # Calculate y values
            y1_vals = [float(func1.subs(x, val)) for val in x_vals]
            y2_vals = [float(func2.subs(x, val)) for val in x_vals]
            
            # Clear the figure and create new plot
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # Plot functions
            ax.plot(x_vals, y1_vals, label=f'f1(x) = {func1_str}')
            ax.plot(x_vals, y2_vals, label=f'f2(x) = {func2_str}')
            
            # Plot and annotate solution points
            for sol in solutions:
                y_sol = float(func1.subs(x, sol))
                ax.plot(sol, y_sol, 'ro')
                ax.annotate(f'({sol:.2f}, {y_sol:.2f})',
                           (sol, y_sol),
                           xytext=(10, 10),
                           textcoords='offset points')
                           
            ax.grid(True)
            ax.legend()
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            
            self.canvas.draw()
            
            # Display solutions
            result_text = "Solutions:\n"
            for i, sol in enumerate(solutions, 1):
                result_text += f"x{i} = {sol:.4f}\n"
            self.result_label.setText(result_text)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MathPlotApp()
    window.show()
    sys.exit(app.exec_())