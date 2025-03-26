import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from unittest.mock import patch, MagicMock
from ReadFromCSVAndCallOpenAI import process_with_openai

class TestReadFromCSVAndCallOpenAI(unittest.TestCase):
    @patch("ReadFromCSVAndCallOpenAI.client.chat.completions.create")
    def test_process_with_openai(self, mock_openai_create):
        # Mock OpenAI API response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content='{"Category": [{"Request Type": "Adjustment", "Sub Request Type": "Reallocation Fees"}], "Deal Name": "Deal123", "Amount": "1000", "Expiration Date": "2025-12-31", "Reasoning": "Example reasoning"}'))
        ]
        mock_openai_create.return_value = mock_response

        # Test data
        subject = "Test Subject"
        body = "Test Body"
        attachment_text = "Test Attachment"
        image_text = "Test Image"

        # Call the function
        result = process_with_openai(subject, body, attachment_text, image_text)

        # Assertions
        self.assertIn("Category", result)
        self.assertIn("Adjustment", result)
        self.assertIn("Deal123", result)
        self.assertIn("1000", result)
        self.assertIn("2025-12-31", result)

        # Verify OpenAI API was called
        mock_openai_create.assert_called_once()

if __name__ == "__main__":
    unittest.main()