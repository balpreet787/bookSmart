import os
import sys

from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, \
    QPushButton, QMessageBox
from functionalities.crud import get_books, add_book


def main_window_setup(main_window, app):
    main_window.setWindowTitle("BookSmart")
    main_window.resize(800, 600)
    main_window.show()
    app.exec()


def load_books(thumbnail_layout):
    books = get_books()
    for i in reversed(range(thumbnail_layout.count())):
        widget = thumbnail_layout.itemAt(i).widget()
        if widget is not None:
            widget.setParent(None)
    for book in books:
        book_name = os.path.basename(book)
        thumbnail_path = os.path.join('./thumbnails', book_name + ".png")
        thumbnail = QPixmap(thumbnail_path)
        thumbnail_label = QLabel()
        thumbnail_label.setPixmap(thumbnail)
        thumbnail_label.setAlignment(Qt.AlignCenter)

        book_name_label = QLabel(book_name.split(".")[0])
        book_name_label.setAlignment(Qt.AlignCenter)
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.addWidget(thumbnail_label)
        container_layout.addWidget(book_name_label)
        container_layout.setAlignment(Qt.AlignCenter)
        container.setLayout(container_layout)

        thumbnail_layout.addWidget(container)


def create_book(main_window, thumbnail_layout):
    book = QFileDialog.getOpenFileName(main_window, "Choose a book", "", "PDF Files (*.pdf)")
    add_book(book[0])
    load_books(thumbnail_layout)


def delete_book_confirmation(main_window, book_name):
    confirm = QMessageBox.question(main_window, "Confirm delete", "Are you sure you want to delete" + book_name + "?")


def delete_book(main_window, thumbnail_layout):
    for i in reversed(range(thumbnail_layout.count())):
        widget = thumbnail_layout.itemAt(i).widget()
        book_name = widget.children()[2].text()
        widget.children()[2] = QPushButton("Delete " + book_name)
        delete_button = widget.children()[2]
        delete_button.setStyleSheet(
            "color: red; background-color: white; font-size: 15px; padding: 10px; border-radius:5px")

        delete_button.clicked.connect(lambda: delete_book_confirmation(main_window, book_name))


def main_window_actions(main_window, thumbnail_layout):
    toolbar_bar = main_window.addToolBar("Options")
    toolbar_bar.setStyleSheet("font: 16px")
    add_book_option = toolbar_bar.addAction("Add book")
    delete_book_option = toolbar_bar.addAction("Delete book")
    add_book_option.triggered.connect(lambda: create_book(main_window, thumbnail_layout))
    delete_book_option.triggered.connect(lambda: delete_book(main_window, thumbnail_layout))


def main_window_handler():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    thumbnail_layout = QHBoxLayout()
    main_window_actions(main_window, thumbnail_layout)
    load_books(thumbnail_layout)
    central_widget.setLayout(thumbnail_layout)
    main_window_setup(main_window, app)
