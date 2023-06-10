from test.test_base import TestBase


class TestIO(TestBase):
    def test_input(self):
        _test = self._assert_execute
        _test("ㅀㄱ", "Nil", "")
        _test("ㅀㄱ", "''", "\n")
        _test("ㅀㄱ", "'하늘'", "하늘")
        _test("ㅀㄱ ㄱㅇㄱ ㅅㅅㅎㄴ ㄳㅎㄶ ㄱㅀㄷ", "3.141592", "3.141592")
        _test("ㅀㄱ ㅅㅅ ㄳ ㄴㄱㅎㄷ ㄱㅀㄷ", "3.141592", "3.141592")
        _test("ㅀㄱ ㅀㄱ ㄱㅇㄴ ㄱㅇㄱ 목록ㅎㄷ ㄳㅎㄶ ㄱㅀㄷㅎ ㄱㅀㄷ", "['', Nil]", "\n")

    def test_print(self):
        _test = self._assert_execute
        _test("ㅀㄱ ㄱㅇㄱ ㅈㅀㄶ ㄱㅀㄷ", "Nil", "\n", "")
        _test("ㅀㄱ ㄱㅇㄱ ㅈㅀㄶ ㄱㅀㄷ", "Nil", "하늘", "하늘")
        _test("ㅀㄱ ㅈㄹ ㄱㅀㄷ", "Nil", "\n", "")
        _test("ㅀㄱ ㅈㄹ ㄱㅀㄷ", "Nil", "하늘", "하늘")
        _test("ㅀㄱ ㄱㅇㄱ ㅅㅅㅎㄴ ㄴㄱ ㅅㅎㄷ ㅁㅈㅎㄴ ㅈㅀㄶ ㄱㅀㄷ", "Nil", "5", "0.2")
        _test("ㅀㄱ ㄱㅇㄱ ㅅㅅㅎㄴ ㄴㄱ ㅅㅎㄷ ㅁㅈㅎㄴ ㅈㅀㄶ ㄱㅀㄷ", "Nil", "-1", "-1.0")

    def test_return(self):
        _test = self._assert_execute
        _test("ㄴ ㄳㅎㄴ", "1")
        _test("ㄴ ㄱㅇㄱㅎㅎㄴ ㄳㅎㄴ", "1")

    def test_bind(self):
        _test = self._assert_execute
        _test("ㄴ ㄳㅎㄴ (ㄱㅇㄱ ㄴ ㄷㅎㄷ ㄳㅎㄶ)ㄱㅀㄷ", "2")
        _test(
            "ㄹㅎㄱ (ㄱㅇㄱ ㅅㅅㅎㄴ ㄴㄱ ㅅㅎㄷ ㄱㅅㅎㄴㅎ) ㄱㄹㅎㄷ (ㄱㅇㄱ ㄱㅅㅎㄴㅎ) (ㄱ ㄱㅅㅎㄴㅎ)ㄱㄹㅎㄹ",
            "0.5",
            "2",
        )
        _test(
            "ㄹㅎㄱ (ㄱㅇㄱ ㅅㅅㅎㄴ ㄴㄱ ㅅㅎㄷ ㄱㅅㅎㄴㅎ) ㄱㄹㅎㄷ (ㄱㅇㄱ ㄱㅅㅎㄴㅎ) (ㄱ ㄱㅅㅎㄴㅎ)ㄱㄹㅎㄹ",
            "0",
            "0",
        )

    def test_file_descriptor(self):
        _test = self._assert_execute
        _test("ㄱ ㄹ ㄱㄴㅎㄷ (ㄴ ㄹ ㄱㅇㄱㅎㄷㅎ)ㄱㅀㄷ", "b'\\x61'", "a")
        _test("ㄴ ㅈㄹ ㄱㄴㅎㄷ (b'ㄴㅁㄴ ㄴ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷㅎㄴ' ㅈㄹ ㄱㅇㄱㅎㄷㅎ)ㄱㅀㄷ", "1", "", "a")

    def test_file_read_write(self):
        _test = self._assert_execute
        _test(
            "ㄹㅎㄱ {ㄱㅇㄱ ㅈㄹ ㄱㄴㅎㄷ (ㄱ ㅁㅈ <ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ> ㄴㄱㅎㄷㅎㄴ ㅈㄹ ㄱㅇㄱㅎㄷ {ㄷ ㄱㅇㄴㅎㄴ (ㄱㅇㄴ ㄳㅎㄶ)ㄱㅀㄷㅎ}ㄱㅀㄷㅎ)ㄱㅀㄷㅎ}ㄱㅀㄷ",
            "1",
            "test/test_builtins/testdata/test.txt",
        )
        _test(
            "ㄹㅎㄱ {ㄱㅇㄱ ㄹ ㄱㄴㅎㄷ (ㄴㄱ ㄹ ㄱㅇㄱㅎㄷ {ㄷ ㄱㅇㄴㅎㄴ (ㄱㅇㄴ ㄳㅎㄶ)ㄱㅀㄷㅎ}ㄱㅀㄷㅎ)ㄱㅀㄷㅎ}ㄱㅀㄷ",
            "b'\\x30'",
            "test/test_builtins/testdata/test.txt",
        )
        _test(
            "ㄹㅎㄱ {ㄱㅇㄱ ㄹ ㄱㄴㅎㄷ (ㄴ ㄹ ㄱㅇㄱㅎㄷ {ㄷ ㄱㅇㄴㅎㄴ (ㄱㅇㄴ ㄳㅎㄶ)ㄱㅀㄷㅎ}ㄱㅀㄷㅎ)ㄱㅀㄷㅎ}ㄱㅀㄷ",
            "b'\\x30'",
            "test/test_builtins/testdata/test.txt",
        )

    def test_file_seek(self):
        _test = self._assert_execute
        _test(
            "ㄹㅎㄱ {ㄱㅇㄱ ㄹ ㄱㄴㅎㄷ (ㄴ ㄹ ㄱㅇㄱㅎㄷ [ㄱ ㅈ ㄱㅇㄴㅎㄷ {ㄴ ㄹ ㄱㅇㄷㅎㄷ (ㄱㅇㄱ ㄱㅇㄷ ㄷㅎㄷ ㄱㅅㅎㄴㅎ)ㄱㅀㄷㅎ}ㄱㅀㄷㅎ]ㄱㅀㄷ {ㄷ ㄱㅇㄴㅎㄴ (ㄱㅇㄴ ㄳㅎㄶ)ㄱㅀㄷㅎ}ㄱㅀㄷㅎ)ㄱㅀㄷㅎ}ㄱㅀㄷ",
            "b'\\x30\\x30'",
            "test/test_builtins/testdata/test.txt",
        )

    def test_file_tell(self):
        _test = self._assert_execute
        _test(
            "ㄹㅎㄱ {ㄱㅇㄱ ㄹ ㄱㄴㅎㄷ (ㅈ ㄱㅇㄱㅎㄴ {ㄷ ㄱㅇㄴㅎㄴ (ㄱㅇㄴ ㄳㅎㄶ)ㄱㅀㄷㅎ}ㄱㅀㄷㅎ)ㄱㅀㄷㅎ}ㄱㅀㄷ",
            "0",
            "test/test_builtins/testdata/test.txt",
        )
        _test(
            "ㄹㅎㄱ {ㄱㅇㄱ ㄹ ㄱㄴㅎㄷ (ㄴ ㄹ ㄱㅇㄱㅎㄷ (ㅈ ㄱㅇㄴㅎㄴㅎ)ㄱㄹㅎㄷ {ㄷ ㄱㅇㄴㅎㄴ (ㄱㅇㄴ ㄳㅎㄶ)ㄱㅀㄷㅎ}ㄱㅀㄷㅎ)ㄱㅀㄷㅎ}ㄱㅀㄷ",
            "1",
            "test/test_builtins/testdata/test.txt",
        )
        _test(
            "ㄹㅎㄱ {ㄱㅇㄱ ㄹ ㄱㄴㅎㄷ (ㅈ ㄱㅇㄱㅎㄴ, ㄴ ㄹ ㄱㅇㄱㅎㄷ [ㄴㅇㄱ ㄱㅇㄴㅎ ㄱㄹㅎㄷㅎ]ㅎㄷ {ㄷ ㄱㅇㄴㅎㄴ (ㄱㅇㄴ ㄳㅎㄶ)ㄱㅀㄷㅎ}ㄱㅀㄷㅎ)ㄱㅀㄷㅎ}ㄱㅀㄷ",
            "1",
            "test/test_builtins/testdata/test.txt",
        )
