# BookSmart

BookSmart is a PDF reading application
that provides a unique reading experience by playing background sounds based on the mood.
This project uses text analysis to determine the mood of the text
and fetches appropriate sounds from the Freesound API to enhance the reading experience.

## Features

- **PDF Reader**: Read PDF files with a clean and simple interface.
- **Mood-Based Background Sounds**: Plays background sounds based on the mood of the text being read.
- **Bookmarks**: Save your reading progress and continue from where you left off.
- **Keyboard Shortcuts**: Navigate through the book using keyboard shortcuts.

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (optional but recommended)

### Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/balpreet787/bookSmart.git
    cd bookSmart
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the Freesound API key:

    - Create a `.env` file in the root directory of the project.
    - Add your Freesound API key to the `.env` file:

        ```sh
        FREESOUND_API_KEY=your_freesound_api_key
        ```
## Usage

Run the application:

```sh
python main.py
```

### Keyboard Shortcuts

- **Right Arrow**: Next page
- **Left Arrow**: Previous page

### Project Structure

- `main.py`: The main entry point of the application.
- `ui/mainWindow.py`: Contains the main window class and GUI logic.
- `functionalities/crud.py`: Handles file operations such as adding, deleting, and fetching books.
- `functionalities/sound.py`: Contains functions for analyzing text and fetching sounds from the Freesound API.
- `requirements.txt`: Lists all the dependencies required to run the project.

### Dependencies

The project dependencies are listed in the `requirements.txt` file. Here are some of the key dependencies:

- `PySide6`: Used for the graphical user interface.
- `requests`: For making HTTP requests to the Freesound API.
- `textblob`: For text analysis.
- `python-dotenv`: For loading environment variables from a `.env` file.
- `pdf2image`: For converting PDF pages to images.
- `PyMuPDF`: For working with PDF files.
