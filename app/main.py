"""Main entry point for the math game application.

This module initializes the PyQt5 application and creates the main window.
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow

def main():
    """Initialize and run the math game application.
    
    Creates the QApplication instance, initializes the main window,
    and starts the Qt event loop.
    """
    # Skapa applikationsobjektet (måste finnas i varje PyQt app)
    app = QApplication(sys.argv)

    # Skapa ditt huvudfönster
    window = MainWindow()
    window.show()

    # Starta event-loopen
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
