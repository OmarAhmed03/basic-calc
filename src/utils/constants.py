WINDOW_TITLE = "Function Solver & Plotter"
WINDOW_GEOMETRY = (100, 100, 1000, 800)  # x, y, width, height

# Expression buttons configuration
EXPRESSION_BUTTONS = [
    ('x', 'x'),
    ('^', '^'),
    ('√', 'sqrt('),
    ('+', '+'),
    ('-', '-'),
    ('*', '*'),
    ('/', '/'),
    ('(', '('),
    (')', ')'),
    ('log10', 'log10('),
    ('Clear', 'CLEAR')
]

# Plot settings
FIGURE_SIZE = (10, 6)
PLOT_DPI = 100
SOLUTION_POINT_COLOR = 'ro'
SOLUTION_POINT_SIZE = 10
GRID_ALPHA = 0.3

# Mathematical constants
X_RANGE_PADDING = 2  # Extra space around solutions in plot
NUM_PLOT_POINTS = 1000  # Number of points to plot