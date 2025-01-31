# src/core/equation_solver.py
import numpy as np
from sympy import symbols, sympify, solve, log
from .expression_parser import ExpressionParser
import re
class EquationSolver:
    def __init__(self):
        self.parser = ExpressionParser()
        
    def evaluate_function(self, expr_str, x_val):
        """
        Safely evaluate function for a given x value.
        """
        try:
            if x_val <= 0 and 'log' in expr_str:
                return np.nan
                
            # Convert log10 to log base 10
            x = symbols('x')
            expr = sympify(expr_str)
            result = float(expr.subs(x, x_val))
            
            if np.isnan(result) or np.isinf(result):
                return np.nan
            return result
        except (ValueError, TypeError, ZeroDivisionError) as e:
            print(f"Error evaluating {expr_str} at x={x_val}: {str(e)}")
            return np.nan

    def solve_functions(self, func1_str, func2_str):
        """
        Solve the system of equations and prepare plot data.
        """
        try:
            print(f"Solving equations: {func1_str} = {func2_str}")
            
            # Parse expressions
            func1_str = self.parser.format_expression(func1_str)
            func2_str = self.parser.format_expression(func2_str)
            
            x = symbols('x')
            func1 = sympify(func1_str)
            func2 = sympify(func2_str)
            
            # Solve the equations using sympy
            solutions = solve(func1 - func2, x)
            # Filter out complex solutions
            solutions = [sol.evalf() for sol in solutions if sol.is_real]
            solutions = [float(sol) for sol in solutions]
            
            print(f"Found solutions: {solutions}")
            
            # Prepare plot data
            x_min = min(solutions) - (np.abs(3*min(solutions)) if min(solutions)==0 else 3) if solutions else -10.0
            x_max = max(solutions) + (np.abs(3*min(solutions)) if min(solutions)==0 else 3) if solutions else 10.0
            
            x_vals = np.linspace(x_min, x_max, 1000)
            y1_vals = np.array([self.evaluate_function(func1_str, x_val) for x_val in x_vals])
            y2_vals = np.array([self.evaluate_function(func2_str, x_val) for x_val in x_vals])
            
            plot_data = (x_vals, y1_vals, y2_vals, solutions, func1_str, func2_str)
            
            return solutions if solutions else None, plot_data
            
        except Exception as e:
            print(f"Error in solve_functions: {str(e)}")
            raise ValueError(f"Error solving equations: {str(e)}")