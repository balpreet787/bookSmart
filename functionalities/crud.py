from PySide6.QtWidgets import QFileDialog
import shutil


def add_book():
    book = QFileDialog.getOpenFileName()
    shutil.copy(book[0], './books')
