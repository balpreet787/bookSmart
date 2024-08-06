import json
import os
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, \
    QPushButton, QMessageBox, QSpacerItem, QSizePolicy, QScrollArea
from PySide6.QtGui import QPixmap, Qt, QImage
from functionalities.crud import get_books, add_book, delete_book
import fitz  # PyMuPDF


def clear_layout(layout):
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widget.setParent(None)


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


def create_read_buttons():
    start_book_fresh_button = QPushButton("Read from beginning")
    continue_book_button = QPushButton("Continue")
    start_book_fresh_button.setStyleSheet(
        "color: black; background-color: white; font-size: 15px; padding: 10px; border-radius:5px")
    continue_book_button.setStyleSheet(
        "color: green; background-color: white; font-size: 15px; padding: 10px; border-radius:5px")
    return start_book_fresh_button, continue_book_button


class BookSmartApp(QMainWindow):
    def __init__(self):
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
        self.current_page = 0
        self.page_number_label = QLabel()

        self.load_books()

    def create_delete_button(self, book_name):
        delete_button = QPushButton(f"Delete {book_name}")
        delete_button.setStyleSheet(
            "color: red; background-color: white; font-size: 15px; padding: 10px; border-radius:5px")
        delete_button.clicked.connect(
            lambda checked, selected_book=book_name: self.delete_book_confirmation(selected_book))
        delete_button.setVisible(False)
        return delete_button

    def create_book_widget(self, book_name, thumbnail_path):
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
        continue_book_button.clicked.connect(lambda checked, selected_book=book_name, start_page=self.current_page:
                                             self.open_pdf(selected_book, start_page))
        start_book_fresh_button.clicked.connect(lambda checked, selected_book=book_name:
                                                self.open_pdf(selected_book, start_page=0))
        return container

    def load_books(self):
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
        book = QFileDialog.getOpenFileName(self, "Choose a book", "", "PDF Files (*.pdf)")
        if book[0]:
            add_book(book[0])
            self.load_books()

    def delete_book_confirmation(self, book_name):
        confirm = QMessageBox.question(self, "Confirm delete", f"Are you sure you want to delete {book_name}?")
        if confirm == QMessageBox.Yes:
            delete_book(book_name)
            self.load_books()

    def toggle_delete_buttons(self):
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
        self.toolbar.clear()
        self.add_book_option = self.toolbar.addAction("Add book")
        self.delete_book_option = self.toolbar.addAction("Delete book")
        self.add_book_option.triggered.connect(self.create_book)
        self.delete_book_option.triggered.connect(self.toggle_delete_buttons)

    def load_bookmark(self, book_name):
        bookmark_json_path = './bookmarks/bookmarks.json'
        try:
            if os.path.exists(bookmark_json_path):
                with open(bookmark_json_path, 'r') as file:
                    data = json.load(file)
                self.current_page = data.get(book_name, 0)
            else:
                self.current_page = 0
        except json.JSONDecodeError:
            self.current_page = 0

    def save_bookmark(self, book_name):
        bookmark_json_path = './bookmarks/bookmarks.json'
        data = {}
        if os.path.exists(bookmark_json_path):
            try:
                with open(bookmark_json_path, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = {}
        data[book_name] = self.current_page
        with open(bookmark_json_path, 'w') as file:
            json.dump(data, file)

    def open_pdf(self, book_name, start_page=0):
        self.toolbar.clear()
        back_button = self.toolbar.addAction("Back")
        back_button.triggered.connect(lambda: self.load_books())

        # Create a custom layout for navigation buttons and page number
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
        self.showMaximized()
        if start_page == 0:
            self.show_page(start_from_beginning=True)
        else:
            self.show_page()

    def show_page(self, start_from_beginning=False):
        if start_from_beginning:
            self.current_page = 0
        page_num = self.current_page
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
        self.page_number_label.setText(f"Page {self.current_page + 1}")

    def next_page(self, book_name):
        if self.current_page < len(self.current_book) - 1:
            self.current_page += 1
            self.save_bookmark(book_name)
            self.show_page()

    def previous_page(self, book_name):
        if self.current_page > 0:
            self.current_page -= 1
            self.save_bookmark(book_name)
            self.show_page()
