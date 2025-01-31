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
        # Get the function input field
        func1_input = input_panel.findChildren(QLineEdit)[0]

        # Ensure the input field is set as active
        input_panel._set_active_input(func1_input)

        # Set focus properly
        func1_input.setFocus()
        qtbot.wait(100)  

        # Define button tests (button text, expected output in input field)
        buttons_to_test = [
            ('x', 'x'),
            ('+', 'x+'),
            ('^', 'x+^'),
            ('(', 'x+^('),
        ]

        for button_text, expected_text in buttons_to_test:
            # Find the button safely
            button = next((btn for btn in input_panel.findChildren(QPushButton) 
                        if btn.text() == button_text), None)

            assert button is not None, f"Button '{button_text}' not found! Available: {[btn.text() for btn in input_panel.findChildren(QPushButton)]}"

            # Click the button
            qtbot.mouseClick(button, Qt.LeftButton)
            qtbot.wait(100)  # Ensure UI updates

            # Check if the expected text is in the input field
            assert func1_input.text() == expected_text, \
                f"Expected '{expected_text}', but got '{func1_input.text()}'"


    def test_clear_button(self, input_panel, qtbot):
        """Test clear button functionality"""
        func1_input = input_panel.func1_input.itemAt(1).widget()
        
        # Type some text
        func1_input.setText("x^2 + 1")

        # Find and click clear button
        clear_button = next((btn for btn in input_panel.findChildren(QPushButton) 
                            if btn.text() == 'Clear'), None)
        assert clear_button is not None, "Clear button not found"

        qtbot.mouseClick(clear_button, Qt.LeftButton)
        
        assert func1_input.text() == "", "Clear button did not reset input field"

    def test_solve_request(self, input_panel, qtbot):
        """Test solve button functionality"""
        func1_input = input_panel.func1_input.itemAt(1).widget()
        func2_input = input_panel.func2_input.itemAt(1).widget()
        
        # Set test equations
        func1_input.setText("x^2")
        func2_input.setText("4")
        
        # Create signal spy
        with qtbot.waitSignal(input_panel.solve_requested) as blocker:
            solve_button = next((btn for btn in input_panel.findChildren(QPushButton) 
                                 if "Solve" in btn.text()), None)
            assert solve_button is not None, "Solve button not found"
            qtbot.mouseClick(solve_button, Qt.LeftButton)
        
        # Verify signal was emitted with correct arguments
        assert blocker.args == ["x^2", "4"], \
            f"Expected ['x^2', '4'], but got {blocker.args}"

