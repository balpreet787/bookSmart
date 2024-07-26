from PySide6.QtWidgets import QApplication, QMainWindow
from functionalities.crud import add_book


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("BookSmart")

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        add_book_option = file_menu.addAction("Add Book")
        file_menu.addAction("Delete Book")
        add_book_option.triggered.connect(add_book)
