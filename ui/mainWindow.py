import os
import sys

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from functionalities.crud import create_book, get_books


def main_window_actions(main_window):
    menu_bar = main_window.menuBar()
    file_menu = menu_bar.addMenu("&File")
    add_book_option = file_menu.addAction("Add book")
    add_book_option.triggered.connect(lambda: create_book(main_window))


def main_window_setup(main_window, app):
    main_window.setWindowTitle("BookSmart")
    main_window.resize(800, 600)
    main_window.show()
    app.exec()


def load_books():
    books = get_books()
    thumbnail_layout = QHBoxLayout()
    for book in books:
        book_name = os.path.basename(book)
        thumbnail_path = os.path.join('./thumbnails', book_name + ".png")
        thumbnail = QPixmap(thumbnail_path)
        thumbnail_label = QLabel()
        thumbnail_label.setPixmap(thumbnail)

        book_name_label = QLabel(book_name.split(".")[0])

        # Create a container widget for each book's thumbnail and label
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.addWidget(thumbnail_label)
        container_layout.addWidget(book_name_label)
        container.setLayout(container_layout)

        # Add the container widget to the main horizontal layout
        thumbnail_layout.addWidget(container)
    return thumbnail_layout


def main_window_handler():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window_actions(main_window)
    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    thumbnail_layout = load_books()
    central_widget.setLayout(thumbnail_layout)
    main_window_setup(main_window, app)
