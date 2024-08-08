import json

from PySide6.QtWidgets import QFileDialog
import shutil
import os
from pdf2image import convert_from_path

BOOKS_DIR = './books'
THUMB_DIR = './thumbnails'


def directory_exists(directory):
    """
    Check if a directory exists, and create it if it does not.

    :param directory: the path to the directory
    :precondition: directory must be a valid directory path as a string
    :postcondition: the directory will be created if it does not exist
    :return: True if the directory exists or was created successfully
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    else:
        return True


def add_thumbnail(file):
    """
    Create and save a thumbnail image for the given PDF file.

    :param file: the path to the PDF file
    :precondition: file must be a valid path to a PDF file
    :postcondition: a thumbnail image will be created and saved in the thumbnails directory
    """
    directory_exists(THUMB_DIR)
    images = convert_from_path(file, first_page=1, last_page=2, size=(256, 256))
    base_name = os.path.basename(file)
    thumb_path = os.path.join(THUMB_DIR, base_name + ".png")
    images[0].save(thumb_path, 'PNG')


def add_book(file):
    """
    Add a book to the books directory and create its thumbnail.

    :param file: the path to the PDF file
    :precondition: file must be a valid path to a PDF file
    :postcondition: the PDF file will be copied to the books directory and a thumbnail will be created
    :return: True if the book was successfully added, False if it already exists
    """
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
    """
    Retrieve a list of all books in the books directory.

    :precondition: none
    :postcondition: returns a list of absolute paths to the books
    :return: a list of absolute paths to the books in the books directory
    """
    all_books = []
    for path in os.listdir(BOOKS_DIR):
        absolute_path = os.path.abspath(os.path.join(BOOKS_DIR, path))
        all_books.append(absolute_path)

    return all_books


def delete_book(book_name):
    """
    Delete a book and its associated thumbnail and bookmark.

    :param book_name: the name of the book
    :precondition: book_name must be a non-empty string
    :postcondition: the book, its thumbnail, and its bookmark will be deleted if they exist
    """
    print("Deleting book " + book_name)
    if os.path.exists(f"{BOOKS_DIR}/{book_name}.pdf"):
        os.remove(f"{BOOKS_DIR}/{book_name}.pdf")
        os.remove(f"{THUMB_DIR}/{book_name}.pdf.png")

    bookmark_json_path = './bookmarks/bookmarks.json'
    data = {}
    if os.path.exists(bookmark_json_path):
        try:
            with open(bookmark_json_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = {}
    if book_name in data:
        del data[book_name]
    with open(bookmark_json_path, 'w') as file:
        json.dump(data, file)

