from test.test_base import TestBase


class TestFunctional(TestBase):
    def test_try_catch(self):
        _test = self._assert_execute
        _test("(ㄱ 뜻밖ㅎㄴ ㄷㅈㅎㄴ) (ㄴㅎ) ㅅㄷㅎㄷ", "1")
        _test("(ㄱ 뜻밖ㅎㄴ ㄷㅈㅎㄴ) (ㄱ ㄱㅇㄱㅎㄴ ㅎ) ㅅㄷㅎㄷ", "0")
        _test("(ㄴ ㄷ 뜻밖ㅎㄷ ㄷㅈㅎㄴ) (ㄱㅇㄱ ㄴㅇㄱ ㄷㅎㄷㅎ)ㅁㅂㅎㄴ ㅅㄷㅎㄷ", "3")
