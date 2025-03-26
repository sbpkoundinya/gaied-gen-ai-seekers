import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from unittest.mock import patch, mock_open, MagicMock
from Extract_Email_SavetoCSVFile import extract_text_from_image, extract_text_from_pdf, parse_email

class TestExtractEmailSaveToCSVFile(unittest.TestCase):
    @patch("Extract_Email_SavetoCSVFile.Image.open")
    @patch("Extract_Email_SavetoCSVFile.pytesseract.image_to_string")
    def test_extract_text_from_image(self, mock_image_to_string, mock_image_open):
        # Mock the behavior of Image.open and pytesseract.image_to_string
        mock_image_open.return_value = MagicMock()
        mock_image_to_string.return_value = "Mocked OCR Text"

        # Call the function
        result = extract_text_from_image("mock_image_path.png")

        # Assertions
        mock_image_open.assert_called_once_with("mock_image_path.png")
        mock_image_to_string.assert_called_once()
        self.assertEqual(result, "Mocked OCR Text")

if __name__ == "__main__":
    unittest.main()