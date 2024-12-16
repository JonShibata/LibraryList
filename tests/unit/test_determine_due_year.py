
import unittest
import os
import sys


from src.determine_due_year import determine_due_year


class TestDetermineDueYear(unittest.TestCase):

    def test_determine_due_year(self):
        self.assertEqual(determine_due_year(1, 12, 2024), 2025)
        self.assertEqual(determine_due_year(1, 1, 2025), 2025)
        self.assertEqual(determine_due_year(12, 11, 2025), 2025)
        self.assertEqual(determine_due_year(5, 7, 2025), 2026)
        self.assertEqual(determine_due_year(7, 5, 2025), 2025)


if __name__ == '__main__':
    unittest.main()
