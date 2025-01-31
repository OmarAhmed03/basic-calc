import pytest
import numpy as np
from PySide2.QtWidgets import QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib.pyplot as plt
from gui.plot_widget import PlotWidget

@pytest.mark.plot
class TestPlotWidget:
    def test_widget_creation(self, app, qtbot):
        """Test plot widget initialization"""
        widget = PlotWidget()
        qtbot.addWidget(widget)
        
        # Check widget structure
        assert isinstance(widget.layout(), QVBoxLayout)
        assert isinstance(widget.figure, Figure)
        assert isinstance(widget.canvas, FigureCanvasQTAgg)
        assert isinstance(widget.toolbar, NavigationToolbar2QT)

    def test_plot_functions(self, app, qtbot):
        """Test plotting functionality"""
        widget = PlotWidget()
        qtbot.addWidget(widget)
        
        # Create test data
        x_vals = np.linspace(-5, 5, 100)
        y1_vals = x_vals ** 2
        y2_vals = np.full_like(x_vals, 4)
        solutions = [-2.0, 2.0]
        
        # Plot the functions
        widget.plot_functions(x_vals, y1_vals, y2_vals, solutions, 
                            "x^2", "4")
        
        # Verify plot elements
        ax = widget.figure.axes[0]
        assert len(ax.lines) == 2  # Two function lines
        assert len([c for c in ax.collections 
                   if isinstance(c, plt.matplotlib.collections.PathCollection)]) == 2  # Solution points
        assert "x^2" in ax.get_legend().get_texts()[0].get_text()
        assert "4" in ax.get_legend().get_texts()[1].get_text()

    def test_plot_styling(self, app, qtbot):
        """Test plot styling elements"""
        widget = PlotWidget()
        qtbot.addWidget(widget)
        
        # Plot simple functions
        x_vals = np.linspace(-5, 5, 100)
        y1_vals = x_vals
        y2_vals = -x_vals
        solutions = [0.0]
        
        widget.plot_functions(x_vals, y1_vals, y2_vals, solutions,
                            "x", "-x")
        
        ax = widget.figure.axes[0]
        
        # Check styling elements
        assert ax.get_facecolor() == '#f8f9fa'
        assert not ax.spines['top'].get_visible()
        assert not ax.spines['right'].get_visible()
        assert ax.spines['left'].get_color() == '#666666'
        assert ax.spines['bottom'].get_color() == '#666666'
        
        # Check grid
        assert ax.xaxis._gridOnMajor
        assert ax.yaxis._gridOnMajor
        
        # Check solution point styling
        scatter_points = [c for c in ax.collections 
                         if isinstance(c, plt.matplotlib.collections.PathCollection)]
        assert len(scatter_points) == 1
        assert scatter_points[0].get_facecolor()[0][2] == 1.0  # Blue color
        assert scatter_points[0].get_zorder() == 3  # Above grid

    def test_no_solutions(self, app, qtbot):
        """Test plotting with no solutions"""
        widget = PlotWidget()
        qtbot.addWidget(widget)
        
        x_vals = np.linspace(-5, 5, 100)
        y1_vals = x_vals ** 2
        y2_vals = np.full_like(x_vals, -1)
        solutions = []
        
        widget.plot_functions(x_vals, y1_vals, y2_vals, solutions,
                            "x^2", "-1")
        
        ax = widget.figure.axes[0]
        scatter_points = [c for c in ax.collections 
                         if isinstance(c, plt.matplotlib.collections.PathCollection)]
        assert len(scatter_points) == 0

    def test_figure_update(self, app, qtbot):
        """Test figure updating with new plots"""
        widget = PlotWidget()
        qtbot.addWidget(widget)
        
        # Plot first set of functions
        x_vals = np.linspace(-5, 5, 100)
        y1_vals = x_vals ** 2
        y2_vals = np.full_like(x_vals, 4)
        
        widget.plot_functions(x_vals, y1_vals, y2_vals, [-2.0, 2.0],
                            "x^2", "4")
        
        # Plot second set of functions
        y1_vals_new = x_vals
        y2_vals_new = -x_vals
        
        widget.plot_functions(x_vals, y1_vals_new, y2_vals_new, [0.0],
                            "x", "-x")
        
        # Verify only the new plot exists
        assert len(widget.figure.axes) == 1
        ax = widget.figure.axes[0]
        assert len(ax.lines) == 2
        assert "x" in ax.get_legend().get_texts()[0].get_text()
        assert "-x" in ax.get_legend().get_texts()[1].get_text()