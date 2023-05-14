from test.test_base import TestBase

from pbhhg_py.abstract_syntax import *
from pbhhg_py.utils import *


class TestUtils(TestBase):
    def test_all_equal(self):
        self.assertTrue(all_equal([]))
        self.assertTrue(all_equal([1]))
        self.assertTrue(all_equal([1, 1]))
        self.assertTrue(all_equal([1, 1.0]))
        self.assertTrue(all_equal([1, 1.0, 1 + 0j]))
        self.assertFalse(all_equal([1, 2]))
        self.assertFalse(all_equal([1, "1"]))

    def test_is_type(self):
        self.assertTrue(is_type([], Number))
        self.assertTrue(is_type([Integer(3)], Number))
        self.assertFalse(is_type([Boolean(True)], Number))
        self.assertTrue(is_type([Boolean(True)], Boolean))
        self.assertTrue(is_type([Integer(3)], Number | Boolean))
        self.assertTrue(is_type([Integer(3)], StrictValue))
        self.assertTrue(is_type([Integer(3), Float(1.0)], Number))
        self.assertTrue(is_type([Integer(3), Complex(1j)], Number))
        self.assertFalse(is_type([Integer(3), Complex(1j)], Real))

    def test_is_same_type(self):
        self.assertTrue(is_same_type([]))
        self.assertTrue(is_same_type([Integer(3)]))
        self.assertTrue(is_same_type([Integer(3), Integer(4)]))
        self.assertFalse(is_same_type([Integer(3), Float(4.0)]))

    def test_match_defaults(self):
        metadata = Metadata("<test file>", 0, 0, 0, "")
        self.assertEqual(match_defaults(metadata, [], 0), [])
        self.assertEqual(match_defaults(metadata, [], 1, [1]), [1])
        self.assertEqual(match_defaults(metadata, [0], 1, [1]), [0])
        self.assertEqual(match_defaults(metadata, [], 2, [1, 2]), [1, 2])
        self.assertEqual(match_defaults(metadata, [0], 3, [1, 2]), [0, 1, 2])
        self.assertEqual(match_defaults(metadata, [0], 2, [1, 2]), [0, 2])
        self.assertEqual(match_defaults(metadata, [0, 1], 2, [1, 2]), [0, 1])

    def test_guessed_wrap(self):
        self.assertEqual(guessed_wrap(0), Integer(0))
        self.assertEqual(guessed_wrap(0.0), Float(0.0))
        self.assertEqual(guessed_wrap(0j), Complex(0j))
        self.assertEqual(guessed_wrap(True), Boolean(True))
        self.assertEqual(guessed_wrap(()), List(()))
        self.assertEqual(guessed_wrap(""), String(""))
        self.assertEqual(guessed_wrap(b""), Bytes(b""))
        self.assertEqual(guessed_wrap({}), Dict({}))
