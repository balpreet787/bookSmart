import sys

from ui.mainWindow import MainWindow
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()