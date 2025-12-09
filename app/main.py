"""Main entry point for the math game application.

This module initializes the PyQt5 application and creates the main window.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from gui import MainWindow

def main():
    """Initialize and run the math game application.
    
    Creates the QApplication instance, initializes the main window,
    and starts the Qt event loop.
    """

    app = QApplication(sys.argv)
    apply_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

def apply_stylesheet(app, filename="style.qss"):
    """Apply QSS stylesheet to the application.
    
    Args:
        app (QApplication): The application instance
        filename (str): Name of the stylesheet file
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))

    style_path = os.path.join(script_dir, filename)
    
    try:
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Warning: Could not find stylesheet at {style_path}")


if __name__ == "__main__":
    main()
