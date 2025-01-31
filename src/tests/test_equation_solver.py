import pytest
import numpy as np
from core.equation_solver import EquationSolver

@pytest.mark.solver
class TestEquationSolver:
    def test_linear_equation(self, solver):
        """Test solving linear equations"""
        solutions, _ = solver.solve_functions("2*x + 1", "x - 1")
        assert len(solutions) == 1
        assert abs(solutions[0] - (-2)) < 1e-6

    def test_quadratic_equation(self, solver):
        """Test solving quadratic equations"""
        solutions, _ = solver.solve_functions("x^2", "4")
        assert len(solutions) == 2
        solutions = sorted(solutions)
        assert abs(solutions[0] + 2) < 1e-6
        assert abs(solutions[1] - 2) < 1e-6

    def test_no_real_solutions(self, solver):
        """Test equations with no real solutions"""
        solutions, _ = solver.solve_functions("x^2 + 1", "0")
        assert solutions is None

    def test_logarithmic_equations(self, solver):
        """Test equations with logarithms"""
        solutions, _ = solver.solve_functions("log10(x)", "1")
        assert len(solutions) == 1
        assert abs(solutions[0] - 10) < 1e-6



    def test_plot_data_generation(self, solver):
        """Test plot data generation"""
        _, plot_data = solver.solve_functions("x^2", "4")
        x_vals, y1_vals, y2_vals, solutions, func1_str, func2_str = plot_data
        
        assert len(x_vals) == len(y1_vals) == len(y2_vals)
        assert isinstance(solutions, list)
        assert func1_str == "x**2"
        assert func2_str == "4"