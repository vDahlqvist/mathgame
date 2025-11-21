import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow

def main():
    # Skapa applikationsobjektet (måste finnas i varje PyQt app)
    app = QApplication(sys.argv)

    # Skapa ditt huvudfönster
    window = MainWindow()
    window.show()

    # Starta event-loopen
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
