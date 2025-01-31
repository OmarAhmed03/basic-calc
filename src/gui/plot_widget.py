# src/gui/plot_widget.py
from PySide2.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the plot widget UI."""
        layout = QVBoxLayout(self)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
    def plot_functions(self, x_vals, y1_vals, y2_vals, solutions, func1_str, func2_str):
        """
        Plot the functions and their intersection points.
        Will always plot the functions even if no solutions exist.
        """
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # Determine if we should use log scale
            use_log_scale = 'log' in func1_str or 'log' in func2_str
            
            if use_log_scale:
                ax.set_xscale('log')
            
            # Plot functions
            ax.plot(x_vals, y1_vals, label=f'f1(x) = {func1_str}')
            ax.plot(x_vals, y2_vals, label=f'f2(x) = {func2_str}')
            
            # Plot and annotate solution points if they exist
            if solutions:
                for sol in solutions:
                    # Find y value at solution point
                    idx = np.abs(x_vals - sol).argmin()
                    y_sol = y1_vals[idx]
                    
                    ax.plot(sol, y_sol, 'ro')
                    ax.annotate(f'({sol:.2f}, {y_sol:.2f})',
                               (sol, y_sol),
                               xytext=(10, 10),
                               textcoords='offset points')
            
            ax.grid(True)
            ax.legend()
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            
            # Adjust the view
            if use_log_scale:
                ax.set_xlim(min(x_vals), max(x_vals))
            else:
                margin = 0.1 * (max(x_vals) - min(x_vals))
                ax.set_xlim(min(x_vals) - margin, max(x_vals) + margin)
            
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error in plot_functions: {str(e)}")
            raise