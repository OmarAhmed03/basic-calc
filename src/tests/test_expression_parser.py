import pytest
from core.expression_parser import ExpressionParser

@pytest.mark.parser
class TestExpressionParser:
    def test_validate_basic_expressions(self, parser):
        """Test validation of basic expressions"""
        valid_exprs = [
            "2*x + 1",
            "x^2 - 4*x + 4",
            "x + 1",
            "(x + 1)*(x - 1)",
        ]
        for expr in valid_exprs:
            is_valid, _ = parser.validate_expression(expr)
            assert is_valid

    def test_validate_invalid_expressions(self, parser):
        """Test validation of invalid expressions"""
        invalid_exprs = [
            "",  # Empty
            "2*x + @",  # Invalid character
            "(2*x + 1",  # Unbalanced parentheses
            "2**x",  # Invalid power notation
            "2x+",  # Incomplete expression
        ]
        for expr in invalid_exprs:
            is_valid, error_msg = parser.validate_expression(expr)
            assert not is_valid
            assert error_msg != ""

    def test_format_basic_expressions(self, parser):
        """Test formatting of basic expressions"""
        test_cases = [
            ("2x + 1", "2*x + 1"),
            ("x^2", "x**2"),
            ("2(x+1)", "2*(x+1)"),
            ("x+1", "x+1"),
        ]
        for input_expr, expected in test_cases:
            formatted = parser.format_expression(input_expr)
            assert formatted == expected

    def test_format_logarithms(self, parser):
        """Test formatting of logarithmic expressions"""
        test_cases = [
            ("log10(x)", "log(x, 10)"),
            ("2*log10(x+1)", "2*log(x+1, 10)"),
            ("log10(x^2)", "log(x**2, 10)"),
        ]
        for input_expr, expected in test_cases:
            formatted = parser.format_expression(input_expr)
            assert formatted == expected

    def test_implicit_multiplication(self, parser):
        """Test handling of implicit multiplication"""
        test_cases = [
            ("2x", "2*x"),
            ("(x+1)(x-1)", "(x+1)*(x-1)"),
            ("2(x+1)", "2*(x+1)"),
            ("x(x+1)", "x*(x+1)"),
        ]
        for input_expr, expected in test_cases:
            formatted = parser.format_expression(input_expr)
            assert formatted == expected