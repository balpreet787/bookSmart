from unittest import TestCase
from unittest.mock import patch, MagicMock
import os

from functionalities.crud import directory_exists


class TestDirectoryExists(TestCase):

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_directory_created(self, mock_makedirs, mock_exists):
        mock_exists.return_value = False
        path = 'new_directory'

        result = directory_exists(path)

        mock_makedirs.assert_called_once_with(path)
        self.assertTrue(result)

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_directory_exists(self, mock_makedirs, mock_exists):
        mock_exists.return_value = True  #

        result = directory_exists('existing_directory')

        mock_makedirs.assert_not_called()
        self.assertTrue(result)

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_directory_creation_failure(self, mock_makedirs, mock_exists):
        mock_exists.return_value = False
        mock_makedirs.side_effect = OSError("Error creating directory")

        with self.assertRaises(OSError):
            directory_exists('fail_directory')

        mock_makedirs.assert_called_once()
