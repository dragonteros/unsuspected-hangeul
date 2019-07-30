from io import StringIO
import sys
import unittest

from pbhhg_py.main import main
from pbhhg_py.interpret import interpret
from pbhhg_py.abstract_syntax import Env
from pbhhg_py.builtins.logic import _all_equal


class TestBase(unittest.TestCase):
    def _assert_execute(self, program, py_value, stdin='', stdout=''):
        sys.stdin, sys.stdout = StringIO(stdin), StringIO()
        self.assertEqual(main(program), py_value)
        self.assertEqual(sys.stdout.getvalue().strip(), stdout.strip())
        sys.stdin, sys.stdout = sys.__stdin__, sys.__stdout__

    def _assert_interpret(self, *programs):
        if len(programs) >= 2:
            values = [
                interpret(program, Env([], [])) for program in programs
            ]
            self.assertTrue(_all_equal(values))
