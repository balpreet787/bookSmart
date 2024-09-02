import json
import os

from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, \
    QPushButton, QMessageBox, QSpacerItem, QSizePolicy, QScrollArea
from PySide6.QtGui import QPixmap, Qt, QImage, QShortcut, QKeySequence
from PySide6.QtCore import QUrl
from functionalities.crud import get_books, add_book, delete_book
import fitz
from functionalities.sound import analyze_page, fetch_sounds


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


class BookSmartApp(QMainWindow):
    def __init__(self):
        """
        Initialize the BookSmartApp.

        :precondition: none
        :postcondition: BookSmartApp is initialized with its UI components and settings
        """
        super().__init__()
        self.setWindowTitle("BookSmart")
        self.resize(800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.thumbnail_layout = QHBoxLayout()
        self.central_widget.setLayout(self.thumbnail_layout)

        self.toolbar = self.addToolBar("Options")
        self.toolbar.setStyleSheet("font: 16px")

        self.add_book_option = self.toolbar.addAction("Add book")
        self.delete_book_option = self.toolbar.addAction("Delete book")

        self.add_book_option.triggered.connect(self.create_book)
        self.delete_book_option.triggered.connect(self.toggle_delete_buttons)

        self.current_book = None
        self.bookmarks = {}
        self.page_number_label = QLabel()
        self.book_name = None
        self.next_page_shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.next_page_shortcut.activated.connect(lambda: self.next_page(self.book_name))

        self.previous_page_shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.previous_page_shortcut.activated.connect(lambda: self.previous_page(self.book_name))

        self.audio_output = QAudioOutput()
        self.mood_player = QMediaPlayer()
        self.mood_player.setAudioOutput(self.audio_output)
        self.current_mood = None

        self.load_books()

    def play_sounds(self, sound, mood):
        """
        Play mood-specific sounds for the book.

        :param sound: the sound URL to play
        :param mood: the mood of the current page
        :precondition: sound must be a valid URL or None
        :postcondition: plays the sound if it is different from the current mood
        """
        if mood != self.current_mood:
            print(f"{mood} is not {self.current_mood}")
            self.current_mood = mood
            self.mood_player.stop()
            if sound is not None:
                self.mood_player.setSource(QUrl(sound))
                print(sound + " is playing")
                self.mood_player.play()

    def create_delete_button(self, book_name):
        """
        Create a QPushButton for deleting a book.

        :param book_name: the name of the book
        :precondition: book_name must be a non-empty string
        :postcondition: returns a QPushButton for deleting the book
        :return: QPushButton for deleting the book
        """
        delete_button = QPushButton(f"Delete {book_name}")
        delete_button.setStyleSheet(
            "color: red; background-color: white; font-size: 15px; padding: 10px; border-radius:5px")
        delete_button.clicked.connect(
            lambda checked, selected_book=book_name: self.delete_book_confirmation(selected_book))
        delete_button.setVisible(False)
        return delete_button

    def create_book_widget(self, book_name, thumbnail_path):
        """
        Create a QWidget containing the book's thumbnail, name, and action buttons.

        :param book_name: the name of the book
        :param thumbnail_path: the file path of the thumbnail image
        :precondition: book_name must be a non-empty string, thumbnail_path must be a valid path to an image file
        :postcondition: returns a QWidget containing the book's information and action buttons
        :return: QWidget with the book's information and action buttons
        """
        container = QWidget()
        container_layout = QVBoxLayout()

        thumbnail_label = create_thumbnail_label(thumbnail_path)
        book_name_label = create_book_name_label(book_name)
        delete_button = self.create_delete_button(book_name)
        start_book_fresh_button, continue_book_button = create_read_buttons()

        container_layout.addWidget(thumbnail_label)
        container_layout.addWidget(book_name_label)
        container_layout.addWidget(delete_button)
        container_layout.addWidget(continue_book_button)
        container_layout.addWidget(start_book_fresh_button)

        container_layout.setAlignment(Qt.AlignCenter)
        container.setLayout(container_layout)
        self.load_bookmark(book_name)
        continue_book_button.clicked.connect(lambda checked, selected_book=book_name,
                                                    start_page=self.bookmarks.get(book_name, 0):
                                             self.open_pdf(selected_book, start_page))
        start_book_fresh_button.clicked.connect(lambda checked, selected_book=book_name:
                                                self.open_pdf(selected_book, start_page=0))
        return container

    def load_books(self):
        """
        Load all books into the application.

        :precondition: none
        :postcondition: displays all books in the UI
        """
        books = get_books()
        self.reset_toolbar()
        for i in reversed(range(self.thumbnail_layout.count())):
            widget = self.thumbnail_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.showNormal()
        for book in books:
            book_name = os.path.basename(book).split(".")[0]
            thumbnail_path = os.path.join('./thumbnails', book_name + ".pdf.png")
            book_widget = self.create_book_widget(book_name, thumbnail_path)
            self.thumbnail_layout.addWidget(book_widget)

    def create_book(self):
        """
        Open a file dialog to add a new book.

        :precondition: none
        :postcondition: adds the selected book to the application and reloads the book list
        """
        book = QFileDialog.getOpenFileName(self, "Choose a book", "", "PDF Files (*.pdf)")
        if book[0]:
            add_book(book[0])
            self.load_books()

    def delete_book_confirmation(self, book_name):
        """
        Show a confirmation dialog to delete a book.

        :param book_name: the name of the book
        :precondition: book_name must be a non-empty string
        :postcondition: deletes the book if confirmed by the user
        """
        confirm = QMessageBox.question(self, "Confirm delete", f"Are you sure you want to delete {book_name}?")
        if confirm == QMessageBox.Yes:
            delete_book(book_name)
            self.load_books()
            self.toggle_delete_buttons()

    def toggle_delete_buttons(self):
        """
        Toggle the visibility of delete buttons for all books.

        :precondition: none
        :postcondition: shows or hides the delete buttons for all books
        """
        for i in range(self.thumbnail_layout.count()):
            container = self.thumbnail_layout.itemAt(i).widget()
            container_layout = container.layout()
            delete_button = container_layout.itemAt(2).widget()
            continue_button = container_layout.itemAt(3).widget()
            start_button = container_layout.itemAt(4).widget()
            if delete_button.isVisible():
                delete_button.setVisible(False)
                continue_button.setVisible(True)
                start_button.setVisible(True)
                self.delete_book_option.setText("Delete Book")
            else:
                delete_button.setVisible(True)
                continue_button.setVisible(False)
                start_button.setVisible(False)
                self.delete_book_option.setText("Hide Delete Book")

    def reset_toolbar(self):
        """
        Reset the toolbar to its default state.

        :precondition: none
        :postcondition: resets the toolbar actions to the default set of options
        """
        self.toolbar.clear()
        self.add_book_option = self.toolbar.addAction("Add book")
        self.delete_book_option = self.toolbar.addAction("Delete book")
        self.add_book_option.triggered.connect(self.create_book)
        self.delete_book_option.triggered.connect(self.toggle_delete_buttons)

    def load_bookmark(self, book_name):
        """
        Load the bookmark for a given book.

        :param book_name: the name of the book
        :precondition: book_name must be a non-empty string
        :postcondition: sets the current page to the bookmarked page, if any
        """
        bookmark_json_path = './bookmarks/bookmarks.json'
        try:
            if os.path.exists(bookmark_json_path):
                with open(bookmark_json_path, 'r') as file:
                    data = json.load(file)
                self.bookmarks[book_name] = data.get(book_name, 0)
            else:
                self.bookmarks[book_name] = 0
        except json.JSONDecodeError:
            self.bookmarks[book_name] = 0

    def save_bookmark(self, book_name):
        """
        Save the current page as a bookmark for a given book.

        :param book_name: the name of the book
        :precondition: book_name must be a non-empty string
        :postcondition: saves the current page number as the bookmark for the book
        """
        bookmark_json_path = './bookmarks/bookmarks.json'
        data = {}
        if os.path.exists(bookmark_json_path):
            try:
                with open(bookmark_json_path, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = {}
        data[book_name] = self.bookmarks.get(book_name, 0)
        with open(bookmark_json_path, 'w') as file:
            json.dump(data, file)

    def open_pdf(self, book_name, start_page=0):
        """
        Open a PDF book and display its content.

        :param book_name: the name of the book
        :param start_page: the page number to start from
        :precondition: book_name must be a non-empty string, start_page must be a valid page number
        :postcondition: displays the specified page of the book
        """
        self.toolbar.clear()
        back_button = self.toolbar.addAction("Back")
        back_button.triggered.connect(lambda: self.load_books())

        nav_widget = QWidget()
        nav_layout = QHBoxLayout()

        previous_page_button = QPushButton("Previous Page")
        previous_page_button.clicked.connect(lambda: self.previous_page(book_name))
        next_page_button = QPushButton("Next Page")
        next_page_button.clicked.connect(lambda: self.next_page(book_name))

        self.page_number_label.setText(f"Page {start_page + 1}")
        self.page_number_label.setAlignment(Qt.AlignCenter)

        nav_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        nav_layout.addWidget(previous_page_button)
        nav_layout.addWidget(self.page_number_label)
        nav_layout.addWidget(next_page_button)
        nav_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        nav_widget.setLayout(nav_layout)
        self.toolbar.addWidget(nav_widget)
        clear_layout(self.thumbnail_layout)

        self.current_book = fitz.open("./books/" + book_name + ".pdf")
        self.book_name = book_name
        self.showMaximized()
        if start_page == 0:
            self.show_page(start_from_beginning=True)
        else:
            self.show_page()

    def show_page(self, start_from_beginning=False):
        """
        Display the current page of the PDF book.

        :param start_from_beginning: whether to start from the beginning of the book
        :precondition: start_from_beginning must be a boolean
        :postcondition: displays the current page of the book
        """
        if start_from_beginning:
            self.bookmarks[self.book_name] = 0
        page_num = self.bookmarks[self.book_name]
        if page_num < 0 or page_num >= len(self.current_book):
            return
        clear_layout(self.thumbnail_layout)
        page = self.current_book.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        img_label = QLabel()
        img_label.setAlignment(Qt.AlignCenter)
        img_label.setPixmap(QPixmap.fromImage(img))

        scroll_area = QScrollArea()
        scroll_area.setWidget(img_label)
        scroll_area.setWidgetResizable(True)
        self.thumbnail_layout.addWidget(scroll_area)
        self.page_number_label.setText(f"Page {self.bookmarks[self.book_name] + 1}")
        page_text = page.get_text()
        page_theme = analyze_page(page_text)
        page_sounds = fetch_sounds(page_theme)
        self.play_sounds(page_sounds, page_theme)

    def next_page(self, book_name):
        """
        Navigate to the next page of the book.

        :param book_name: the name of the book
        :precondition: book_name must be a non-empty string
        :postcondition: moves to the next page of the book and updates the bookmark
        """
        if self.bookmarks[book_name] < len(self.current_book) - 1:
            self.bookmarks[book_name] += 1
            self.save_bookmark(book_name)
            self.show_page()

    def previous_page(self, book_name):
        """
        Navigate to the previous page of the book.

        :param book_name: the name of the book
        :precondition: book_name must be a non-empty string
        :postcondition: moves to the previous page of the book and updates the bookmark
        """
        if self.bookmarks[book_name] > 0:
            self.bookmarks[book_name] -= 1
            self.save_bookmark(book_name)
            self.show_page()
