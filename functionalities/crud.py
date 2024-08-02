from PySide6.QtWidgets import QFileDialog
import shutil
import os
from pdf2image import convert_from_path
BOOKS_DIR = './books'
THUMB_DIR = './thumbnails'


def directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    else:
        return True


def add_thumbnail(file):
    directory_exists(THUMB_DIR)
    images = convert_from_path(file, first_page=1, last_page=2, size=(256, 256))
    base_name = os.path.basename(file)
    thumb_path = os.path.join(THUMB_DIR, base_name + ".png")
    images[0].save(thumb_path, 'PNG')


def add_book(file):
    directory_exists(BOOKS_DIR)
    file_name = os.path.basename(file)
    destination = os.path.join(BOOKS_DIR, file_name)

    if not os.path.exists(destination):
        shutil.copy2(file, destination)
        add_thumbnail(destination)
        return True
    else:
        return False





def get_books():
    all_books = []
    for path in os.listdir(BOOKS_DIR):
        absolute_path = os.path.abspath(os.path.join(BOOKS_DIR, path))
        all_books.append(absolute_path)

    return all_books
