import sys

from ui.mainWindow import BookSmartApp
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    main_window = BookSmartApp()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
