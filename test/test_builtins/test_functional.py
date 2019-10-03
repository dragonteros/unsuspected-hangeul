from test.test_base import TestBase


class TestFunctional(TestBase):
    def test_pipe(self):
        _test = self._assert_execute
        _test('ㄱ ㄴㄱㅎㄱ ㅎㄴ', "0")
        _test('ㄱ ㄴ ㄷ ㅁㅀㄹ ㄴㄱㅎㄱ ㅎㄴ', "[0, 1, 2]")
        _test('ㄱ ㄴ ㅁㅀㄷ ㄱㅈㅎㄱ ㅁㅂㅎㄴ ㅁㅈ ㄴㄱㅎㄷ ㅎㄴ', "'1'")
        _test('ㄷ ㅁㅈ (ㄱㅇㄱ ㄱㅇㄱ ㄷㅎㄷㅎ) ㅅㅅ ㄴㄱㅎㄹ ㅎㄴ', "22")

    def test_spread(self):
        _test = self._assert_execute
        _test('ㄱㅇㄱ ㅈㄷㅎㄶ ㅂㅂㅎㄴ ㅎㄱ', "0")
        _test('ㅁ ㄱㅇㄱ ㅈㄷㅎㄶ ㅂㅂㅎㄴ ㅎㄴ', "1")
        _test('ㅁ ㅁ ㄱㅇㄱ ㅈㄷㅎㄶ ㅂㅂㅎㄴ ㅎㄷ', "2")
        _test('ㄴ ㄴㄱ [ㄱㅇㄱ (ㄱㅇㄱ ㄷ ㄷㅎㄷㅎ) ㅁㄷㅎㄷㅎ] ㅂㅂㅎㄴ ㅎㄷ', "[3, 1]")

    def test_collect(self):
        _test = self._assert_execute
        _test('ㄱ ㄴ ㄷ ㄹ ㅁㅀㅁ ㄷ ㅁㅂㅎㄴ ㅎㄴ', "6")
        _test('ㄱ ㄴ ㄷ ㄹ ㅁㅀㅁ ㄷ ㅁㅂㅎㄴ ㅁㅈ ㄴㄱㅎㄷ ㅎㄴ', "'6'")
        _test('ㄴㄱ ㄴ ㄷ ㄹ ㅁㅀㅁ ㄱ ㅁㅂㅎㄴ ㅁㅈ ㄴㄱㅎㄷ ㅎㄴ', "'-6'")
        _test('ㄱ ㄴ ㄷ ㄹ ㅁㅀㅁ ㅁㅈ ㅁㄷㅎㄷ ㄷ ㅁㅂㅎㄴ ㅎㄴ', "'0123'")
        _test('ㄱ ㄴ ㄷ ㄹ ㅁㅀㅁ ㅁㅈ ㄴㄱㅎㄴ ㅁㄷㅎㄷ ㄷ ㅁㅂㅎㄴ ㅎㄴ', "'0123'")
