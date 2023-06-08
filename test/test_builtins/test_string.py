from test.test_base import TestBase


class TestString(TestBase):
    def test_split_string(self):
        _test = self._assert_execute
        _test("ㅀㄱ ㄱㅇㄱ ㅂㅀㄴ ㄳㅎㄶ ㄱㅀㄷ", "['a', 'b', 'c']", "abc")
        _test("ㅀㄱ ㄱㅇㄱ ㅂㅀㄴ ㄳㅎㄶ ㄱㅀㄷ", "['가', 'a', '1', ' ']", "가a1 ")
        _test("ㅀㄱ ㅀㄱ ㄱㅇㄴ ㄱㅇㄱ ㅂㅀㄷ ㄳㅎㄶ ㄱㅀㄷㅎ ㄱㅀㄷ", "['a', 'b', 'c']", "a b c\n ")
        _test("ㅀㄱ ㅀㄱ ㄱㅇㄴ ㄱㅇㄱ ㅂㅀㄷ ㄳㅎㄶ ㄱㅀㄷㅎ ㄱㅀㄷ", "['평범한', '한글']", "평범한 한글\n ")
        _test(
            "ㅀㄱ ㅀㄱ ㄱㅇㄴ ㄱㅇㄱ ㅂㅀㄷ ㄳㅎㄶ ㄱㅀㄷㅎ ㄱㅀㄷ",
            "['평', '범', '한', '한', '글']",
            "평범한한글\n\n",
        )
        _test("ㅀㄱ ㅀㄱ ㄱㅇㄴ ㄱㅇㄱ ㅂㅀㄷ ㄳㅎㄶ ㄱㅀㄷㅎ ㄱㅀㄷ", "['']", "\n ")
        _test("ㅀㄱ ㅀㄱ ㄱㅇㄴ ㄱㅇㄱ ㅂㅀㄷ ㄳㅎㄶ ㄱㅀㄷㅎ ㄱㅀㄷ", "[' ']", " \n\n")
        _test("ㅀㄱ ㅀㄱ ㄱㅇㄴ ㄱㅇㄱ ㅂㅀㄷ ㄳㅎㄶ ㄱㅀㄷㅎ ㄱㅀㄷ", "['', '']", " \n ")

    def test_split_bytes(self):
        _test = self._assert_execute
        _test("ㄴㅁㄴㄴㅅㅅㄱㄺ ㄴ ㄹ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ ㅂㅀㄴ", "[b'\\x61', b'\\x62', b'\\x63']")
        _test(
            "(ㄴㅁㄴㄴㅅㅅㄱㄺ ㄴ ㄹ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ) (ㄷㅁㄴ ㄴ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ) ㅂㅀㄷ",
            "[b'\\x61', b'\\x63']",
        )
        _test(
            "(ㄴㅁㄴㄴㅅㅅㄱㄺ ㄴ ㄹ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ) (ㄱ ㄴ ㄱ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ) ㅂㅀㄷ",
            "[b'\\x61', b'\\x62', b'\\x63']",
        )
        _test(
            "(ㄱ ㄴ ㄱ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ) (ㄴㅁㄴㄴㅅㅅㄱㄺ ㄴ ㄹ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ) ㅂㅀㄷ",
            "[b'']",
        )
        _test(
            "(ㄴㅁㄴㄴㅅㅅㄱㄺ ㄴ ㄹ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ) (ㄴㅁㄴㄴㅅㅅㄱㄺ ㄴ ㄹ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ) ㅂㅀㄷ",
            "[b'', b'']",
        )

    def test_join_string(self):
        _test = self._assert_execute
        _test("ㅀㄱ ㄱㅇㄱ ㅂㅀㄴ ㄱㅁㅎㄴ ㄳㅎㄶ ㄱㅀㄷ", "'abc'", "abc")
        _test("ㅀㄱ ㅀㄱ ㄱㅇㄴ ㅂㅀㄴ ㄱㅇㄱ ㄱㅁㅎㄷ ㄳㅎㄶ ㄱㅀㄷㅎ ㄱㅀㄷ", "'a|b|c'", "abc\n|")
        _test(
            "ㅀㄱ ㅀㄱ ㄱㅇㄴ ㅂㅀㄴ ㄱㅇㄱ ㄱㅁㅎㄷ ㄳㅎㄶ ㄱㅀㄷㅎ ㄱㅀㄷ", "'산과 들과 강과 별'", "산들강별\n과 "
        )

    def test_join_bytes(self):
        _test = self._assert_execute
        _test("(ㄴㅁㄴㄴㅅㅅㄱㄺ ㄴ ㄹ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ) ㅂㅀㄴ ㄱㅁㅎㄴ", "b'\\x61\\x62\\x63'")
        _test(
            "(ㄴㅁㄴㄴㅅㅅㄱㄺ ㄴ ㄹ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ) ㅂㅀㄴ (ㄱㅁㄱ ㄴ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ) ㄱㅁㅎㄷ",
            "b'\\x61\\x20\\x62\\x20\\x63'",
        )
