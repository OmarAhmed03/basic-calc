import pytest
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QPushButton, QLineEdit, QApplication
from gui.input_panel import InputPanel

@pytest.mark.gui
class TestInputPanel:
    def test_initial_state(self, input_panel):
        """Test initial state of input panel"""
        assert input_panel.active_input is None
        func1_input = input_panel.func1_input.itemAt(1).widget()
        func2_input = input_panel.func2_input.itemAt(1).widget()
        assert isinstance(func1_input, QLineEdit)
        assert isinstance(func2_input, QLineEdit)
        assert func1_input.text() == ""
        assert func2_input.text() == ""

    def test_button_clicks(self, input_panel, qtbot):
        """Test button click functionality"""
        # Set focus to first function input
        func1_input = input_panel.func1_input.itemAt(1).widget()
        qtbot.mouseClick(func1_input, Qt.LeftButton)
        
        # Test clicking various buttons
        buttons_to_test = [
            ('x', 'x'),
            ('+', 'x+'),
            ('2', 'x+2'),
            ('^', 'x+2^'),
            ('(', 'x+2^('),
        ]
        
        for button_text, expected_text in buttons_to_test:
            button = [btn for btn in input_panel.findChildren(QPushButton) 
                     if btn.text() == button_text][0]
            qtbot.mouseClick(button, Qt.LeftButton)
            assert func1_input.text() == expected_text

    def test_clear_button(self, input_panel, qtbot):
        """Test clear button functionality"""
        func1_input = input_panel.func1_input.itemAt(1).widget()
        qtbot.mouseClick(func1_input, Qt.LeftButton)
        
        # Type some text
        func1_input.setText("x^2 + 1")
        
        # Find and click clear button
        clear_button = [btn for btn in input_panel.findChildren(QPushButton) 
                       if btn.text() == 'Clear'][0]
        qtbot.mouseClick(clear_button, Qt.LeftButton)
        
        assert func1_input.text() == ""

    def test_solve_request(self, input_panel, qtbot):
        """Test solve button functionality"""
        func1_input = input_panel.func1_input.itemAt(1).widget()
        func2_input = input_panel.func2_input.itemAt(1).widget()
        
        # Set test equations
        func1_input.setText("x^2")
        func2_input.setText("4")
        
        # Create signal spy
        with qtbot.waitSignal(input_panel.solve_requested) as blocker:
            solve_button = [btn for btn in input_panel.findChildren(QPushButton) 
                          if "Solve" in btn.text()][0]
            qtbot.mouseClick(solve_button, Qt.LeftButton)
        
        # Verify signal was emitted with correct arguments
        assert blocker.args == ["x^2", "4"]

    def test_error_handling(self, input_panel, qtbot):
        """Test error handling in input panel"""
        func1_input = input_panel.func1_input.itemAt(1).widget()
        func2_input = input_panel.func2_input.itemAt(1).widget()
        
        # Set invalid expression
        func1_input.setText("x^2 + @")
        func2_input.setText("4")
        
        # Try to solve
        solve_button = [btn for btn in input_panel.findChildren(QPushButton) 
                       if "Solve" in btn.text()][0]
        qtbot.mouseClick(solve_button, Qt.LeftButton)
        
        # Verify error message
        # Note: Implementation might vary based on how you show errors
        error_widgets = [w for w in QApplication.topLevelWidgets() 
                        if w.windowTitle() == "Error"]
        assert len(error_widgets) > 0