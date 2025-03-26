import unittest
import pandas as pd
import sys
import os

# Add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from update_email_classification import process_with_openai

class TestEmailClassification(unittest.TestCase):
    
    def test_single_request_classification(self):
        """Test classification of a single request type."""
        subject = "Fee Payment Request"
        body = "Please process the ongoing fee payment."
        attachment_text = ""
        response = process_with_openai(subject, body, attachment_text, "")
        self.assertIn("Fee Payment", response)
    
    def test_multiple_request_classification(self):
        """Test classification of an email containing multiple requests."""
        subject = "Money Movement and Commitment Change"
        body = "We need to process an inbound principal payment and increase commitment."
        attachment_text = ""
        response = process_with_openai(subject, body, attachment_text, "")
        self.assertIn("Money Movement - Inbound", response)
        self.assertIn("Commitment Change", response)
    
    def test_email_with_attachment_priority(self):
        """Test prioritization of attachment content for specific request types."""
        subject = "Closing Notice - Reallocation Fees"
        body = "See attached document for fee details."
        attachment_text = "Reallocation Fees: $5000"
        response = process_with_openai(subject, body, attachment_text, "")
        self.assertIn("Closing Notice", response)
        self.assertIn("Reallocation Fees", response)
    
    def test_duplicate_email_detection(self):
        """Test that duplicate emails are not reprocessed."""
        subject = "Adjustment Request"
        body = "Please adjust the account balance."
        attachment_text = ""
        response1 = process_with_openai(subject, body, attachment_text, "")
        response2 = process_with_openai(subject, body, attachment_text, "")
        self.assertIsNotNone(response1)
        self.assertIsNone(response2)
    
    def test_various_attachment_types(self):
        """Test processing with different attachment types (PDF, Image, TXT)."""
        subject = "Money Movement - Outbound Request"
        body = "Please process this timebound transfer."
        attachment_text = "Timebound Transfer Details"
        response = process_with_openai(subject, body, attachment_text, "")
        self.assertIn("Money Movement - Outbound", response)
        self.assertIn("Timebound", response)
    
if __name__ == "__main__":
    unittest.main()