from test.test_base import TestBase


class TestIO(TestBase):
    def test_input(self):
        _test = self._assert_execute
        _test('ㅀㄱ', '', '\n')
        _test('ㅀㄱ', '하늘', '하늘')
        _test('ㅀㄱ ㄱㅇㄱ ㅅㅅㅎㄴ ㄳㅎㄶ ㄱㅀㄷ', 3.141592, '3.141592')

    def test_print(self):
        _test = self._assert_execute
        _test('ㅀㄱ ㄱㅇㄱ ㅈㅀㄶ ㄱㅀㄷ', None, '\n', '')
        _test('ㅀㄱ ㄱㅇㄱ ㅈㅀㄶ ㄱㅀㄷ', None, '하늘', '하늘')
        _test('ㅀㄱ ㄱㅇㄱ ㅅㅅㅎㄴ ㄴㄱ ㅅㅎㄷ ㅁㅈㅎㄴ ㅈㅀㄶ ㄱㅀㄷ', None, '5', '0.2')
        _test('ㅀㄱ ㄱㅇㄱ ㅅㅅㅎㄴ ㄴㄱ ㅅㅎㄷ ㅁㅈㅎㄴ ㅈㅀㄶ ㄱㅀㄷ', None, '-1', '-1')

    def test_return(self):
        _test = self._assert_execute
        _test('ㄴ ㄳㅎㄴ', 1)
        _test('ㄴ ㄱㅇㄱㅎㅎㄴ ㄳㅎㄴ', 1)

    def test_bind(self):
        _test = self._assert_execute
        _test('ㄴ ㄳㅎㄴ (ㄱㅇㄱ ㄴ ㄷㅎㄷㅎ)ㄱㅀㄷ', 2)
        _test('ㄴ ㄳㅎㄴ ㄷ ㄳㅎㄴ (ㄱㅇㄱ ㄴㅇㄱ ㄷㅎㄷㅎ)ㄱㅀㄹ', 3)
