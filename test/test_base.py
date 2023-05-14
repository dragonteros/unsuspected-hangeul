import io
import sys
import unittest

from pbhhg_py.main import main


class TestBase(unittest.TestCase):
    def _assert_execute(
        self,
        program: str,
        py_value: str,
        stdin: str = "",
        stdout: str = "",
    ):
        reader = io.BytesIO(stdin.encode("utf-8"))
        sys.stdin = io.TextIOWrapper(reader, encoding="utf-8")

        writer = io.BytesIO()
        sys.stdout = io.TextIOWrapper(writer, encoding="utf-8")

        result = main("<test file>", program, False)
        self.assertEqual(len(result), 1, "Number of Parsed Exprs")
        self.assertEqual(result[0], py_value, "Evaluated Value")
        self.assertEqual(
            writer.getvalue().decode("utf-8").strip(), stdout.strip()
        )
        sys.stdin, sys.stdout = sys.__stdin__, sys.__stdout__
