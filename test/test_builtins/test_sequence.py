from test.test_base import TestBase


class TestSequence(TestBase):
    def test_len(self):
        _test = self._assert_execute
        _test("ㅁㅀㄱ ㅈㄷㅎㄴ", "0")
        _test("ㄱ ㅁㅀㄴ ㅈㄷㅎㄴ", "1")
        _test("ㄱ ㄴ ㅁㅀㄷ ㅈㄷㅎㄴ", "2")
        _test("ㄱ ㅁㅀㄴ ㄴ ㅁㅀㄴ ㄷㅎㄷ ㅈㄷㅎㄴ", "2")
        _test("ㅁㅈㅎㄱ ㅈㄷㅎㄴ", "0")
        _test("ㄷㄴㄱ ㅁㅈㅎㄴ ㅈㄷㅎㄴ", "2")
        _test("ㅁㅈㅎㄱ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㅈㄷㅎㄴ", "0")
        _test("ㄷㄴㄱ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㅈㄷㅎㄴ", "2")
        _test("ㄷㄴㄱ ㅁㅈㅎㄴ (ㄱ ㄷ ㄱㅈㅎㄱ ㅂ ㅂ ㅂㅎㄷㅎㄹ)ㅎㄴ ㅈㄷㅎㄴ", "4")
        _test("뜻밖ㅎㄱ ㅈㄷㅎㄴ", "0")
        _test("ㄱ 뜻밖ㅎㄴ ㅈㄷㅎㄴ", "1")
        _test("ㄱ ㄴ 뜻밖ㅎㄷ ㅈㄷㅎㄴ", "2")

    def test_slice(self):
        _test = self._assert_execute
        _test("ㅁㅀㄱ ㄱ ㅂㅈㅎㄷ", "[]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄱ ㅂㅈㅎㄷ", "[0, 1, 2, 3, 4]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄴ ㅂㅈㅎㄷ", "[1, 2, 3, 4]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄹ ㅂㅈㅎㄷ", "[3, 4]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㅂ ㅂㅈㅎㄷ", "[]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄴㄱ ㅂㅈㅎㄷ", "[4]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄱ ㄷ ㅂㅈㅎㄹ", "[0, 1]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄴ ㄴㄱ ㅂㅈㅎㄹ", "[1, 2, 3]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄹ ㄹㄱ ㅂㅈㅎㄹ", "[]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄹ ㅅ ㅂㅈㅎㄹ", "[3, 4]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄱ ㄹ ㄷ ㅂㅈㅎㅁ", "[0, 2]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄱ ㄴㄱ ㄹ ㅂㅈㅎㅁ", "[0, 3]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄴㄱ ㅅㄱ ㄴㄱ ㅂㅈㅎㅁ", "[4, 3, 2, 1, 0]")
        _test("ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㅂ ㄴ ㄴㄱ ㅂㅈㅎㅁ", "[4, 3, 2]")
        _test("ㅁㅈㅎㄱ ㄱ ㅂㅈㅎㄷ", "''")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ ㄱ ㅂㅈㅎㄷ", "'12345'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ ㄴ ㅂㅈㅎㄷ", "'2345'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ ㄹ ㅂㅈㅎㄷ", "'45'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ ㅂ ㅂㅈㅎㄷ", "''")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ ㄴㄱ ㅂㅈㅎㄷ", "'5'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ ㄱ ㄷ ㅂㅈㅎㄹ", "'12'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ ㄴ ㄴㄱ ㅂㅈㅎㄹ", "'234'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ ㄹ ㄹㄱ ㅂㅈㅎㄹ", "''")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ ㄹ ㅅ ㅂㅈㅎㄹ", "'45'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ ㄱ ㄹ ㄷ ㅂㅈㅎㅁ", "'13'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ ㄱ ㄴㄱ ㄹ ㅂㅈㅎㅁ", "'14'")
        _test("ㅁㅈㅎㄱ ㄱ ㅂㅈㅎㄷ", "''")
        _test(
            "ㄵㄱㄱㄹ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㄱ ㅂㅈㅎㄷ",
            "b'\\x31\\x32\\x33\\x34\\x35'",
        )
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㄴ ㅂㅈㅎㄷ", "b'\\x32\\x33\\x34\\x35'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㄹ ㅂㅈㅎㄷ", "b'\\x34\\x35'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㅂ ㅂㅈㅎㄷ", "b''")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㄴㄱ ㅂㅈㅎㄷ", "b'\\x35'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㄱ ㄷ ㅂㅈㅎㄹ", "b'\\x31\\x32'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㄴ ㄴㄱ ㅂㅈㅎㄹ", "b'\\x32\\x33\\x34'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㄹ ㄹㄱ ㅂㅈㅎㄹ", "b''")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㄹ ㅅ ㅂㅈㅎㄹ", "b'\\x34\\x35'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㄱ ㄹ ㄷ ㅂㅈㅎㅁ", "b'\\x31\\x33'")
        _test("ㄵㄱㄱㄹ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㄱ ㄴㄱ ㄹ ㅂㅈㅎㅁ", "b'\\x31\\x34'")

    def test_map(self):
        _test = self._assert_execute
        _test("ㅁㅀㄱ ㄱㅇㄱ ㄷ ㅅㅎㄷㅎ ㅁㄷㅎㄷ", "[]")
        _test("ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁㅀㅂ ㄱㅇㄱ ㄷ ㅅㅎㄷㅎ ㅁㄷㅎㄷ", "[1, 0, 1, 4, 9]")
        _test("ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁㅀㅂ ㄱㅇㄱ ㅁㅀㄶ ㅁㄷㅎㄷ", "[[-1], [0], [1], [2], [3]]")
        _test("ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁㅀㅂ ㅁㄹ ㅁㄷㅎㄷ", "[[-1], [0], [1], [2], [3]]")
        _test("ㅁㅀㄱ ㅁㄹ ㅁㄷㅎㄷ", "[]")
        _test("ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁㅀㅂ ㅁㅈ ㅁㄷㅎㄷ", "['-1', '0', '1', '2', '3']")

    def test_filter(self):
        _test = self._assert_execute
        _test("ㅁㅀㄱ ㄱ ㄱㅇㄱ ㅈㅎㄷㅎ ㅅㅂㅎㄷ", "[]")
        _test("ㄴㄱ ㄱ ㄴ ㄷㄱ ㄹ ㅁㅀㅂ ㄱ ㄱㅇㄱ ㅈㅎㄷㅎ ㅅㅂㅎㄷ", "[1, 3]")
        _test("ㄴㄱ ㄱ ㄴ ㄷㄱ ㄹ ㅁㅀㅂ ㄱㅇㄱ ㄱ ㅈㅎㄷㅎ ㅅㅂㅎㄷ", "[-1, -2]")
        _test("ㄴㄱ ㄱ ㄴ ㄷㄱ ㄹ ㅁㅀㅂ ㄱㅇㄱ ㄷㄱ ㅈㅎㄷㅎ ㅅㅂㅎㄷ", "[]")

    def test_fold(self):
        _test = self._assert_execute
        _test("ㅁㅀㄱ ㄱ ㅀ ㅅㅀㄹ", "0")
        _test("ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁㅀㅂ ㄷ ㅅㅀㄷ", "5")
        _test("ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁㅀㅂ ㄱㅇㄱ ㄴㅇㄱ ㄷㅎㄷㅎ ㅅㅀㄷ", "5")
        _test("ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁㅀㅂ ㅂ ㄱㅇㄱ ㄴㅇㄱ ㄷㅎㄷㅎ ㅅㅀㄹ", "10")
        _test("ㄱㅇㄱ ㄴㅇㄱ ㄷㅎㄷㅎ ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁㅀㅂ ㅅㅀㄷ", "5")
        _test("ㄱㅇㄱ ㄴㅇㄱ ㄷㅎㄷㅎ ㅂ ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁㅀㅂ ㅅㅀㄹ", "10")
        _test("ㅁ ㄷ ㄴㄱ ㅁㅀㄹ ㄱㅇㄱ ㄴㅇㄱ ㅅㅎㄷㅎ ㅅㅀㄷ", "2.0")
        _test("ㄱㅇㄱ ㄴㅇㄱ ㅅㅎㄷㅎ ㄷㄱ ㄷ ㄴㄱ ㅁㅀㄹ ㅅㅀㄷ", "0.25")
        _test("ㅁ ㄷ ㄴㄱ ㅁㅀㄹ (ㅁㅈ ㄴㄱㅎㄴ) ㅁㄷㅎㄷ (ㄱㅇㄱ ㄴㅇㄱ ㄷㅎㄷㅎ) ㅅㅀㄷ", "'42-1'")
        _test("(ㄱㅇㄱ ㄴㅇㄱ ㄷㅎㄷㅎ) ㅁ ㄷ ㄴㄱ ㅁㅀㄹ (ㅁㅈ ㄴㄱㅎㄴ) ㅁㄷㅎㄷ ㅅㅀㄷ", "'42-1'")
