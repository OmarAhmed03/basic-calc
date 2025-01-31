from PySide2.QtWidgets import QWidget, QVBoxLayout
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create matplotlib figure with modern style
        self.figure = Figure(figsize=(8, 6), dpi=100, facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: white;")
        
        # Create navigation toolbar with modern styling
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: white;
                border: none;
                border-bottom: 1px solid #e0e0e0;
                padding: 5px;
            }
            QToolButton {
                background-color: white;
                border: none;
                border-radius: 4px;
                padding: 4px;
            }
            QToolButton:hover {
                background-color: #f5f5f5;
            }
        """)
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
    def plot_functions(self, x_vals, y1_vals, y2_vals, solutions, func1_str, func2_str):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Modern styling for the plot
        ax.set_facecolor('#f8f9fa')
        
        # Set modern grid style
        ax.grid(True, linestyle='--', alpha=0.3, color='gray')
        
        # Set modern spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#666666')
        ax.spines['bottom'].set_color('#666666')
        
        # Modern tick styling
        ax.tick_params(colors='#666666')
        
        # Plot with modern colors
        line1, = ax.plot(x_vals, y1_vals, label=f'f₁(x) = {func1_str}', 
                        color='#2196F3', linewidth=2)
        line2, = ax.plot(x_vals, y2_vals, label=f'f₂(x) = {func2_str}', 
                        color='#FF5722', linewidth=2)
        
        if solutions:
            for sol in solutions:
                idx = np.abs(x_vals - sol).argmin()
                y_sol = y1_vals[idx]
                ax.plot(sol, y_sol, 'o', color='#4CAF50', markersize=8, 
                       zorder=3)  # Ensure points are above grid
                
                # Modern annotation style
                bbox_props = dict(
                    boxstyle='round,pad=0.5',
                    fc='white',
                    ec='#4CAF50',
                    alpha=0.8
                )
                ax.annotate(
                    f'({sol:.2f}, {y_sol:.2f})',
                    (sol, y_sol),
                    xytext=(10, 10),
                    textcoords='offset points',
                    bbox=bbox_props,
                    fontsize=9,
                    color='#333333'
                )
        
        # Modern font styling for labels
        ax.set_xlabel('x', fontsize=11, color='#333333')
        ax.set_ylabel('y', fontsize=11, color='#333333')
        
        # Legend styling
        legend = ax.legend(
            frameon=True,
            facecolor='white',
            edgecolor='#e0e0e0',
            fontsize=10
        )
        legend.get_frame().set_alpha(0.9)
        for text in legend.get_texts():
            text.set_color('#333333')
        
        # Set margins
        ax.margins(x=0.1)
        
        # Adjust layout and display
        self.figure.tight_layout()
        self.canvas.draw()