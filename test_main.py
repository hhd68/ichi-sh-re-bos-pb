#!/usr/bin/env python3
"""
Tests for ichi+sh+re+bos+pb implementation
"""

import unittest
import sys
from io import StringIO
from main import main


class TestIchiShReBosPb(unittest.TestCase):
    """Test cases for ichi+sh+re+bos+pb implementation"""

    def test_main_output(self):
        """Test that main() outputs the correct string"""
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        result = main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify output
        self.assertEqual(result, "ichi+sh+re+bos+pb")
        self.assertEqual(captured_output.getvalue().strip(), "ichi+sh+re+bos+pb")

    def test_result_format(self):
        """Test that the result has the correct format"""
        result = main()
        self.assertIn("+", result)
        components = result.split("+")
        self.assertEqual(len(components), 5)
        self.assertEqual(components, ["ichi", "sh", "re", "bos", "pb"])


if __name__ == "__main__":
    # Suppress main() output during import
    sys.stdout = StringIO()
    unittest.main()
