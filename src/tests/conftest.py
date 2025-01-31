import pytest
from PySide2.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.input_panel import InputPanel
from core.equation_solver import EquationSolver
from core.expression_parser import ExpressionParser
from PySide2.QtCore import Qt

@pytest.fixture(scope="session")
def app():
    """Create the QApplication instance"""
    return QApplication.instance() or QApplication([])

@pytest.fixture
def main_window(app, qtbot):
    """Create the main window instance"""
    window = MainWindow()
    qtbot.addWidget(window)
    return window

@pytest.fixture
def input_panel(app, qtbot):
    """Create the input panel instance"""
    panel = InputPanel()
    qtbot.addWidget(panel)
    return panel

@pytest.fixture
def solver():
    """Create equation solver instance"""
    return EquationSolver()

@pytest.fixture
def parser():
    """Create expression parser instance"""
    return ExpressionParser()

@pytest.fixture
def qtbot_click(qtbot):
    """Helper fixture for clicking buttons"""
    def _click_button(widget):
        qtbot.mouseClick(widget, Qt.LeftButton)
    return _click_button