from test.test_base import TestBase


class TestFunctional(TestBase):
    def test_try_catch(self):
        _test = self._assert_execute
        _test('(ㄱ ㄷㅈㅎㄴ) (ㄴㅎ) ㅅㄷㅎㄷ', "1")
        _test('(ㄱ ㄷㅈㅎㄴ) (ㄱㅇㄱ ㅎ) ㅅㄷㅎㄷ', "0")
        _test('(ㄴ ㄷ ㄷㅈㅎㄷ) (ㄱㅇㄱ ㄴㅇㄱ ㄷㅎㄷㅎ) ㅅㄷㅎㄷ', "3")
