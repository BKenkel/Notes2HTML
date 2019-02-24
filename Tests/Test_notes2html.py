import os
import unittest

import notes2html


class TestInitOutFile(unittest.TestCase):
    def setUp(self):
        self.expected_file_name = 'expected_init_file.html'
        with open(self.expected_file_name, 'r') as expected:
            self.expected_contents = expected.readlines()
        self.actual_output = 'test_init_out.html'

    def test_happy_case(self):
        notes2html.init_out_file('test_init', self.actual_output)

        with open(self.actual_output, 'r') as actual:
            self.actual_contents = actual.readlines()
        self.assertEqual(self.actual_contents, self.expected_contents)
        if self.actual_contents == self.expected_contents:
            os.remove(self.actual_output)
