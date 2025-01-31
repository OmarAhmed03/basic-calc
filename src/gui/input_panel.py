from PySide2.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QGridLayout, QMessageBox)
from PySide2.QtCore import Signal, Qt
from PySide2.QtGui import QFont, QPalette, QColor
from core.equation_solver import EquationSolver
from core.expression_parser import ExpressionParser

class InputPanel(QWidget):
    solve_requested = Signal(str, str)
    
    def __init__(self):
        super().__init__()
        self.solver = EquationSolver()
        self.parser = ExpressionParser()
        self.active_input = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Style for input fields
        input_style = """
            QLineEdit {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
                font-family: 'Consolas';
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """
        
        # Function input fields with modern styling
        self.func1_input = self._create_function_input("Function 1:", input_style)
        self.func2_input = self._create_function_input("Function 2:", input_style)
        
        # Expression buttons with grid layout
        button_grid = self._create_expression_buttons()
        
        # Solve button with modern styling
        solve_button = QPushButton("Solve and Plot")
        solve_button.setFixedHeight(40)
        solve_button.setFont(QFont("Segoe UI", 11))
        solve_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        solve_button.clicked.connect(self._on_solve_clicked)
        
        # Result label with modern styling
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                background-color: #f5f5f5;
                border-radius: 6px;
                font-family: 'Segoe UI';
                font-size: 13px;
            }
        """)
        
        # Add widgets to layout
        layout.addLayout(self.func1_input)
        layout.addLayout(self.func2_input)
        layout.addLayout(button_grid)
        layout.addWidget(solve_button)
        layout.addWidget(self.result_label)
        layout.addStretch()
        
    def _create_function_input(self, label_text, style):
        layout = QVBoxLayout()
        
        # Label with modern font
        label = QLabel(label_text)
        label.setFont(QFont("Segoe UI", 11))
        
        # Input field with modern styling
        input_field = QLineEdit()
        input_field.setFixedHeight(36)
        input_field.setPlaceholderText("Enter function (e.g., 5*x^3 + 2*x)")
        input_field.setStyleSheet(style)
        
        # Use focusInEvent properly
        def focus_in_handler(event):
            self._set_active_input(input_field)
            QLineEdit.focusInEvent(input_field, event)
            
        input_field.focusInEvent = focus_in_handler
        
        layout.addWidget(label)
        layout.addWidget(input_field)
        return layout
        
    def _create_expression_buttons(self):
        layout = QGridLayout()
        layout.setSpacing(8)
        
        buttons = [
            ('x', 0, 0), ('^', 0, 1), ('√', 0, 2), ('+', 0, 3), ('-', 0, 4),
            ('*', 1, 0), ('/', 1, 1), ('(', 1, 2), (')', 1, 3), ('log₁₀', 1, 4)
        ]
        
        button_style = """
            QPushButton {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #2196F3;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """
        
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedHeight(36)
            button.setStyleSheet(button_style)
            expr = 'log10(' if text == 'log₁₀' else 'sqrt(' if text == '√' else text
            # Create a closure to capture the expression value
            def create_click_handler(expression):
                return lambda _: self._add_expression(expression)
            button.clicked.connect(create_click_handler(expr))
            layout.addWidget(button, row, col)
            
        # Add clear button spanning all columns
        clear_button = QPushButton("Clear")
        clear_button.setFixedHeight(36)
        clear_button.setStyleSheet(button_style)
        clear_button.clicked.connect(lambda _: self._clear_input())
        layout.addWidget(clear_button, 2, 0, 1, 5)
        
        return layout

    def _set_active_input(self, input_field):
        """Set the currently active input field."""
        self.active_input = input_field

    def _add_expression(self, expr):
        """Add the selected expression to the active input field."""
        if not self.active_input:
            return
            
        cursor_pos = self.active_input.cursorPosition()
        current_text = self.active_input.text()
        new_text = current_text[:cursor_pos] + expr + current_text[cursor_pos:]
        self.active_input.setText(new_text)
        self.active_input.setFocus()
        self.active_input.setCursorPosition(cursor_pos + len(expr))

    def _clear_input(self):
        """Clear the active input field."""
        if self.active_input:
            self.active_input.clear()
            
    def _on_solve_clicked(self):
        """Handle solve button click."""
        func1_str = self.func1_input.itemAt(1).widget().text()
        func2_str = self.func2_input.itemAt(1).widget().text()
        
        # Validate input
        if not self.parser.validate_both_expressions(func1_str, func2_str):
            self.show_error("Invalid input expressions")
            return
            
        self.solve_requested.emit(func1_str, func2_str)
        
    def get_solutions(self):
        """Get solutions and plot data for the current functions."""
        func1_str = self.func1_input.itemAt(1).widget().text()
        func2_str = self.func2_input.itemAt(1).widget().text()
        
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