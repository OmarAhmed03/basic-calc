from PySide2.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel)
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QPalette, QColor
from .input_panel import InputPanel
from .plot_widget import PlotWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Function Solver & Plotter")
        self.setGeometry(100, 100, 1200, 800)
        self.setup_ui()
        self.setup_styling()
        
    def setup_ui(self):
        # Create central widget with dark background
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout with margins for padding
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left panel for inputs (1/3 width)
        left_panel = QWidget()
        left_panel.setFixedWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)
        
        # Add title
        title = QLabel("Function Solver & Plotter")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        left_layout.addWidget(title)
        
        # Add input panel
        self.input_panel = InputPanel()
        left_layout.addWidget(self.input_panel)
        
        # Right panel for plot (2/3 width)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Add plot widget
        self.plot_widget = PlotWidget()
        right_layout.addWidget(self.plot_widget)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, stretch=2)
        
        # Connect signals
        self.input_panel.solve_requested.connect(self.solve_and_plot)
        
    def setup_styling(self):
        # Set modern color scheme
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f0f2f5"))
        palette.setColor(QPalette.WindowText, QColor("#1a1a1a"))
        palette.setColor(QPalette.Base, QColor("#ffffff"))
        palette.setColor(QPalette.AlternateBase, QColor("#f9f9f9"))
        palette.setColor(QPalette.Button, QColor("#ffffff"))
        self.setPalette(palette)
        
    def solve_and_plot(self, func1_str, func2_str):
        try:
            solutions, plot_data = self.input_panel.get_solutions()
            if plot_data:
                self.plot_widget.plot_functions(*plot_data)
            self.input_panel.display_results(solutions)
        except Exception as e:
            self.input_panel.show_error(str(e))