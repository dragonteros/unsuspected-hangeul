from test.test_base import TestBase


class TestInterpret(TestBase):
    def test_negative_index(self):
        _test = self._assert_execute
        _test("ㄴ [ㄷ (ㄱㅇㄴㄱ ㄱㅇㄷㄱ ㄷㅎㄷ ㅎ) ㅎㄴ ㅎ] ㅎㄴ", "3")
        _test(
            "ㄴ ㄷㄱ [(ㄱㅇㄱ ㄴㄱ ㅅㅎㄷ ㅎ)(ㄱㅇㄱ ㄱㅇㄴㄱㅎㄴ ㄴㅇㄷㄱ ㄱㅇㄴㅎㄴ ㄷㅎㄷ ㅎ ㅎ) ㅎㄴ] ㅎㄷ", "0.5"
        )
        _test("ㄹ [ㄴ: ㄱㅇㄱ ㄱㅇㄱ ㄴㄱ ㄷㅎㄷ ㄴㄱㅇㅎㄴ ㄱㅎㄷ?(ㄱㅇㄱ ㄷ ㅈㅎㄷ)ㅎㄷ ㅎ] ㅎㄴ", "6")

    def test_seq_index(self):
        _test = self._assert_execute
        _test("ㄱ ㄴ ㄷ ㅁㅀㄷ ㅎㄴ", "1")
        _test("ㄴ ㄴ ㄷ ㅁㅀㄷ ㅎㄴ", "2")
        _test("ㄴㄱ ㄴ ㄷ ㅁㅀㄷ ㅎㄴ", "2")
        _test("ㄷㄱ ㄴ ㄷ ㅁㅀㄷ ㅎㄴ", "1")
        _test("ㄱ ㄷㄴㄱ ㅁㅈㅎㄴ ㅎㄴ", "'1'")
        _test("ㄴ ㄷㄴㄱ ㅁㅈㅎㄴ ㅎㄴ", "'0'")
        _test("ㄴㄱ ㄷㄴㄱ ㅁㅈㅎㄴ ㅎㄴ", "'0'")
        _test("ㄷㄱ ㄷㄴㄱ ㅁㅈㅎㄴ ㅎㄴ", "'1'")
        _test("ㄱ ㄷㄴㄱ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㅎㄴ", "b'\\x31'")
        _test("ㄴ ㄷㄴㄱ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㅎㄴ", "b'\\x30'")
        _test("ㄴㄱ ㄷㄴㄱ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㅎㄴ", "b'\\x30'")
        _test("ㄷㄱ ㄷㄴㄱ ㅁㅈㅎㄴ (ㄱ ㄴ ㅂ ㅂ ㅂㅎㄷㅎㄷ)ㅎㄴ ㅎㄴ", "b'\\x31'")
