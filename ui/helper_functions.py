from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtGui import QPixmap, Qt

def clear_layout(layout):
    """
    Clear all widgets from a given layout.

    :param layout: a QLayout instance
    :precondition: layout must be a valid QLayout instance
    :postcondition: all widgets in the layout will be removed
    """
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widget.setParent(None)


def create_thumbnail_label(thumbnail_path):
    """
    Create a QLabel for displaying a book thumbnail.

    :param thumbnail_path: the file path of the thumbnail image
    :precondition: thumbnail_path must be a valid path to an image file
    :postcondition: returns a QLabel containing the image
    :return: QLabel with the thumbnail image
    """
    thumbnail = QPixmap(thumbnail_path)
    thumbnail_label = QLabel()
    thumbnail_label.setPixmap(thumbnail)
    thumbnail_label.setAlignment(Qt.AlignCenter)
    return thumbnail_label


def create_book_name_label(book_name):
    """
    Create a QLabel for displaying a book name.

    :param book_name: the name of the book
    :precondition: book_name must be a non-empty string
    :postcondition: returns a QLabel with the book name
    :return: QLabel with the book name
    """
    book_name_label = QLabel(book_name)
    book_name_label.setAlignment(Qt.AlignCenter)
    return book_name_label


def create_read_buttons():
    """
    Create QPushButton widgets for reading a book.

    :precondition: none
    :postcondition: returns two QPushButton widgets
    :return: tuple containing 'start book fresh' and 'continue book' QPushButton widgets
    """
    start_book_fresh_button = QPushButton("Read from beginning")
    continue_book_button = QPushButton("Continue")
    start_book_fresh_button.setStyleSheet(
        "color: black; background-color: white; font-size: 15px; padding: 10px; border-radius:5px")
    continue_book_button.setStyleSheet(
        "color: green; background-color: white; font-size: 15px; padding: 10px; border-radius:5px")
    return start_book_fresh_button, continue_book_button