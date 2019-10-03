from test.test_base import TestBase


class TestInterpret(TestBase):
    def test_negative_index(self):
        _test = self._assert_execute
        _test('ㄴ [ㄷ (ㄱㅇㄴㄱ ㄱㅇㄷㄱ ㄷㅎㄷ ㅎ) ㅎㄴ ㅎ] ㅎㄴ', "3")
        _test('ㄴ ㄷㄱ [(ㄱㅇㄱ ㄴㄱ ㅅㅎㄷ ㅎ)(ㄱㅇㄱ ㄱㅇㄴㄱㅎㄴ ㄴㅇㄷㄱ ㄱㅇㄴㅎㄴ ㄷㅎㄷ ㅎ ㅎ) ㅎㄴ] ㅎㄷ', "0.5")
        _test('ㄹ [ㄴ: ㄱㅇㄱ ㄱㅇㄱ ㄴㄱ ㄷㅎㄷ ㄴㄱㅇㅎㄴ ㄱㅎㄷ?(ㄱㅇㄱ ㄷ ㅈㅎㄷ)ㅎㄷ ㅎ] ㅎㄴ', "6")
