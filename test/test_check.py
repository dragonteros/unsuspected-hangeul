from test.test_base import TestBase
from pbhhg_py.abstract_syntax import *
from pbhhg_py.check import *
from pbhhg_py.check import _force_list, _matches


class TestCheck(TestBase):
    def test_force_list(self):
        self.assertEqual(_force_list([1, 2]), [1, 2])
        self.assertEqual(_force_list(3), [3])
        self.assertEqual(_force_list(Number), [Number])
        self.assertEqual(_force_list([Number, Boolean]), [Number, Boolean])

    def test_matches(self):
        self.assertTrue(_matches(Number(3), Number))
        self.assertFalse(_matches(Boolean(True), Number))
        self.assertTrue(_matches(Boolean(True), Boolean))

    def test_is_type(self):
        self.assertTrue(is_type(Number(3), Number))
        self.assertFalse(is_type(Boolean(True), Number))
        self.assertTrue(is_type(Boolean(True), Boolean))
        self.assertTrue(is_type(Number(3), [Number, Boolean]))
