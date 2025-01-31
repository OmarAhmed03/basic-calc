# src/core/expression_parser.py
import re
from sympy import sympify, log

class ExpressionParser:
    def __init__(self):
        self.valid_chars = set('x0123456789+-*/^() ')
        self.valid_funcs = {'log10', 'sqrt'}
        
    def validate_expression(self, expr):
        """
        Validate a mathematical expression.
        """
        if not expr:
            return False, "Expression cannot be empty"
            
        # Remove valid functions from expression for checking
        temp_expr = expr
        for func in self.valid_funcs:
            temp_expr = temp_expr.replace(func, '')
            
        # Check remaining characters
        if not all(c in self.valid_chars for c in temp_expr):
            return False, "Invalid characters in expression"
            
        # Check balanced parentheses
        if expr.count('(') != expr.count(')'):
            return False, "Unbalanced parentheses"
            
        return True, ""
        
    def validate_both_expressions(self, expr1, expr2):
        """Validate both expressions."""
        valid1, msg1 = self.validate_expression(expr1)
        valid2, msg2 = self.validate_expression(expr2)
        return valid1 and valid2
        
    def format_expression(self, expr):
        """Format expression for evaluation."""
        # Clean up the expression
        expr = expr.strip()
        
        # Handle logarithm
        if 'log10' in expr:
            # Convert log10(x) to log(x, 10)
            expr = expr.replace('log10', 'log')
        
        # Replace ^ with **
        expr = expr.replace('^', '**')
        
        # Add multiplication symbols
        expr = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expr)  # 15x -> 15*x
        expr = re.sub(r'(\))([a-zA-Z0-9])', r'\1*\2', expr)  # )x -> )*x
        expr = re.sub(r'(\d)(\()', r'\1*\2', expr)  # 5( -> 5*(
        
        
        return expr