# src/gui/input_panel.py
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QGridLayout, QMessageBox)
from PySide2.QtCore import Signal
from core.equation_solver import EquationSolver
from core.expression_parser import ExpressionParser
from utils.constants import EXPRESSION_BUTTONS

class InputPanel(QWidget):
    solve_requested = Signal(str, str)  # Signal for when solve button is clicked
    
    def __init__(self):
        super().__init__()
        self.solver = EquationSolver()
        self.parser = ExpressionParser()
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize and setup the input panel UI."""
        layout = QVBoxLayout(self)
        
        # Function input fields
        self.func1_input = self._create_function_input("Function 1:")
        self.func2_input = self._create_function_input("Function 2:")
        
        # Expression buttons
        button_grid = self._create_expression_buttons()
        
        # Solve button
        solve_button = QPushButton("Solve and Plot")
        solve_button.clicked.connect(self._on_solve_clicked)
        
        # Result label
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        
        # Add widgets to layout
        layout.addLayout(self.func1_input)
        layout.addLayout(self.func2_input)
        layout.addLayout(button_grid)
        layout.addWidget(solve_button)
        layout.addWidget(self.result_label)
        
        # Track active input
        self.active_input = None
        
    def _create_function_input(self, label_text):
        """Create a function input row with label and text field."""
        layout = QHBoxLayout()
        label = QLabel(label_text)
        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter function (e.g., 5*x^3 + 2*x)")
        input_field.focusInEvent = lambda e, field=input_field: self._set_active_input(field)
        layout.addWidget(label)
        layout.addWidget(input_field)
        return layout
        
    def _create_expression_buttons(self):
        """Create the grid of expression buttons."""
        layout = QGridLayout()
        row, col = 0, 0
        
        for display_text, expr in EXPRESSION_BUTTONS:
            button = QPushButton(display_text)
            button.clicked.connect(lambda checked=False, e=expr: self._add_expression(e))
            layout.addWidget(button, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1
                
        return layout
        
    def _set_active_input(self, input_field):
        """Set the currently active input field."""
        self.active_input = input_field
        
    def _add_expression(self, expr):
        """Add the selected expression to the active input field."""
        if not self.active_input:
            return
            
        if expr == 'CLEAR':
            self.active_input.clear()
        else:
            cursor_pos = self.active_input.cursorPosition()
            current_text = self.active_input.text()
            new_text = current_text[:cursor_pos] + expr + current_text[cursor_pos:]
            self.active_input.setText(new_text)
            self.active_input.setFocus()
            self.active_input.setCursorPosition(cursor_pos + len(expr))
            
    def _on_solve_clicked(self):
        """Handle solve button click."""
        func1_str = self.func1_input.layout().itemAt(1).widget().text()
        func2_str = self.func2_input.layout().itemAt(1).widget().text()
        
        # Validate input
        if not self.parser.validate_both_expressions(func1_str, func2_str):
            self.show_error("Invalid input expressions")
            return
            
        self.solve_requested.emit(func1_str, func2_str)
        
    def get_solutions(self):
        """Get solutions and plot data for the current functions."""
        func1_str = self.func1_input.layout().itemAt(1).widget().text()
        func2_str = self.func2_input.layout().itemAt(1).widget().text()
        
        return self.solver.solve_functions(func1_str, func2_str)
        
    def display_results(self, solutions):
        """Display the solutions in the result label."""
        if not solutions:
            self.result_label.setText("No real solutions found")
            return
            
        result_text = "Solutions:\n"
        for i, sol in enumerate(solutions, 1):
            result_text += f"x{i} = {sol:.4f}\n"
        self.result_label.setText(result_text)
        
    def show_error(self, message):
        """Show error message to user."""
        QMessageBox.warning(self, "Error", message)