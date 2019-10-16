from io import StringIO
import sys
import unittest

from pbhhg_py.main import main


class TestBase(unittest.TestCase):
    def _assert_execute(self, program, py_value, stdin='', stdout=''):
        sys.stdin, sys.stdout = StringIO(stdin), StringIO()
        result = main(program, False)
        self.assertEqual(len(result), 1, 'Number of Parsed Exprs')
        self.assertEqual(result[0], py_value, 'Evaluated Value')
        self.assertEqual(sys.stdout.getvalue().strip(), stdout.strip())
        sys.stdin, sys.stdout = sys.__stdin__, sys.__stdout__
