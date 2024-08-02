import os
import sys

from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, \
    QPushButton, QMessageBox
from functionalities.crud import get_books, add_book, delete_book


def main_window_setup(main_window, app):
    main_window.setWindowTitle("BookSmart")
    main_window.resize(800, 600)
    main_window.show()
    app.exec()


def create_thumbnail_label(thumbnail_path):
    thumbnail = QPixmap(thumbnail_path)
    thumbnail_label = QLabel()
    thumbnail_label.setPixmap(thumbnail)
    thumbnail_label.setAlignment(Qt.AlignCenter)
    return thumbnail_label


def create_book_name_label(book_name):
    book_name_label = QLabel(book_name)
    book_name_label.setAlignment(Qt.AlignCenter)
    return book_name_label


def create_delete_button(main_window, thumbnail_layout, book_name):
    delete_button = QPushButton(f"Delete {book_name}")
    delete_button.setStyleSheet(
        "color: red; background-color: white; font-size: 15px; padding: 10px; border-radius:5px")
    delete_button.clicked.connect(lambda checked, selected_book=book_name: delete_book_confirmation(main_window,
                                                                                                    thumbnail_layout,
                                                                                                    selected_book))
    delete_button.setVisible(False)
    return delete_button


def create_read_buttons():
    start_book_fresh_button = QPushButton("Read from beginning")
    continue_book_button = QPushButton("Continue")
    start_book_fresh_button.setStyleSheet("color: black; background-color: white; font-size: 15px; padding: 10px; "
                                          "border-radius:5px")
    continue_book_button.setStyleSheet("color: green; background-color: white; font-size: 15px; padding: 10px; "
                                       "border-radius:5px")
    return start_book_fresh_button, continue_book_button


def create_book_widget(main_window, thumbnail_layout, book_name, thumbnail_path):
    container = QWidget()
    container_layout = QVBoxLayout()

    thumbnail_label = create_thumbnail_label(thumbnail_path)
    book_name_label = create_book_name_label(book_name)
    delete_button = create_delete_button(main_window, thumbnail_layout, book_name)
    start_book_fresh_button, continue_book_button = create_read_buttons()

    container_layout.addWidget(thumbnail_label)
    container_layout.addWidget(book_name_label)
    container_layout.addWidget(delete_button)
    container_layout.addWidget(continue_book_button)
    container_layout.addWidget(start_book_fresh_button)

    container_layout.setAlignment(Qt.AlignCenter)
    container.setLayout(container_layout)

    return container


def load_books(main_window, thumbnail_layout):
    books = get_books()
    for i in reversed(range(thumbnail_layout.count())):
        widget = thumbnail_layout.itemAt(i).widget()
        if widget is not None:
            widget.setParent(None)
    for book in books:
        book_name = os.path.basename(book).split(".")[0]
        thumbnail_path = os.path.join('./thumbnails', book_name + ".pdf.png")
        book_widget = create_book_widget(main_window, thumbnail_layout, book_name, thumbnail_path)
        thumbnail_layout.addWidget(book_widget)


def create_book(main_window, thumbnail_layout):
    book = QFileDialog.getOpenFileName(main_window, "Choose a book", "", "PDF Files (*.pdf)")
    add_book(book[0])
    load_books(main_window, thumbnail_layout)


def delete_book_confirmation(main_window, thumbnail_layout, book_name):
    confirm = QMessageBox.question(main_window, "Confirm delete", "Are you sure you want to delete" + book_name + "?")
    if confirm == QMessageBox.Yes:
        print("Deleting " + book_name + "...")
        delete_book(book_name)
        load_books(main_window, thumbnail_layout)


def delete_book_action(thumbnail_layout, delete_book_option):
    for i in range(thumbnail_layout.count()):
        container = thumbnail_layout.itemAt(i).widget()
        container_layout = container.layout()
        delete_button = container_layout.itemAt(2).widget()
        continue_button = container_layout.itemAt(3).widget()
        start_button = container_layout.itemAt(4).widget()
        if delete_button.isVisible():
            delete_button.setVisible(False)
            continue_button.setVisible(True)
            start_button.setVisible(True)
            delete_book_option.setText("Delete Book")
        else:
            delete_button.setVisible(True)
            continue_button.setVisible(False)
            start_button.setVisible(False)
            delete_book_option.setText("Hide Delete Book")


def main_window_actions(main_window, thumbnail_layout):
    toolbar_bar = main_window.addToolBar("Options")
    toolbar_bar.setStyleSheet("font: 16px")
    add_book_option = toolbar_bar.addAction("Add book")
    delete_book_option = toolbar_bar.addAction("Delete book")
    add_book_option.triggered.connect(lambda: create_book(main_window, thumbnail_layout))
    delete_book_option.triggered.connect(lambda: delete_book_action(thumbnail_layout, delete_book_option))


def main_window_handler():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    thumbnail_layout = QHBoxLayout()
    main_window_actions(main_window, thumbnail_layout)
    load_books(main_window, thumbnail_layout)
    central_widget.setLayout(thumbnail_layout)
    main_window_setup(main_window, app)
