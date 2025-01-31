# src/gui/main_window.py
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from .input_panel import InputPanel
from .plot_widget import PlotWidget
from utils.constants import WINDOW_TITLE, WINDOW_GEOMETRY

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(*WINDOW_GEOMETRY)
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Initialize components
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize and setup all UI components."""
        # Create input panel
        self.input_panel = InputPanel()
        
        # Create plot widget
        self.plot_widget = PlotWidget()
        
        # Connect signals
        self.input_panel.solve_requested.connect(self.solve_and_plot)
        
        # Add widgets to layout
        self.layout.addWidget(self.input_panel)
        self.layout.addWidget(self.plot_widget)
        
    def solve_and_plot(self, func1_str, func2_str):
        """Handle solve and plot request from input panel."""
        try:
            print(f"Main window received solve request for: {func1_str} and {func2_str}")  # Debug log
            
            # Get solutions and plot data from input panel
            solutions, plot_data = self.input_panel.get_solutions()
            print(f"Got solutions: {solutions}")  # Debug log
            
            # Update plot
            if solutions and plot_data:
                print("Updating plot")  # Debug log
                self.plot_widget.plot_functions(*plot_data)
                
            else:
                print("No solutions or plot data available")  # Debug log
                
        except Exception as e:
            print(f"Error in solve_and_plot: {str(e)}")  # Debug log
            self.input_panel.show_error(str(e))