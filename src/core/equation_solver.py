# src/core/equation_solver.py
import numpy as np
from sympy import symbols, sympify, solve, log
from .expression_parser import ExpressionParser

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
            expr_str = expr_str.replace('log10(', 'log(')
            
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
            
            # For logarithmic functions, use appropriate x range
            if 'log' in func1_str or 'log' in func2_str:
                x_min = 0.01
                x_max = 100.0
            else:
                x_min = -10.0
                x_max = 10.0
            
            # Create more points for better resolution
            x_vals = np.logspace(np.log10(x_min), np.log10(x_max), 1000) if 'log' in func1_str or 'log' in func2_str else np.linspace(x_min, x_max, 1000)
            
            # Calculate y values
            y1_vals = np.array([self.evaluate_function(func1_str, x_val) for x_val in x_vals])
            y2_vals = np.array([self.evaluate_function(func2_str, x_val) for x_val in x_vals])
            
            # Find intersections numerically
            valid_idx = ~(np.isnan(y1_vals) | np.isnan(y2_vals))
            y_diff = y1_vals[valid_idx] - y2_vals[valid_idx]
            x_valid = x_vals[valid_idx]
            
            print(f"Finding intersections in range: {x_min} to {x_max}")
            
            # Find where the difference changes sign
            solutions = []
            for i in range(len(y_diff)-1):
                if y_diff[i] * y_diff[i+1] <= 0:  # Sign change indicates solution
                    # Use linear interpolation to find more precise intersection
                    x1, x2 = x_valid[i], x_valid[i+1]
                    y1, y2 = y_diff[i], y_diff[i+1]
                    x_sol = x1 - y1 * (x2 - x1)/(y2 - y1)  # Linear interpolation
                    solutions.append(x_sol)
                    print(f"Found solution at x = {x_sol}")
            
            # Always return plot data even if no solutions found
            plot_data = (x_vals[valid_idx], y1_vals[valid_idx], y2_vals[valid_idx], 
                        solutions if solutions else [], func1_str, func2_str)
            
            return solutions if solutions else None, plot_data
            
        except Exception as e:
            print(f"Error in solve_functions: {str(e)}")
            raise ValueError(f"Error solving equations: {str(e)}")