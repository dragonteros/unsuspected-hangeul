from test_py.test_base import TestBase


class TestInterpret(TestBase):

    def test_negative_index(self):
        _test = self._assert_execute
        _test('ㄴ [ㄷ (ㄱㅇㄴㄱ ㄱㅇㄷㄱ ㄷㅎㄷ ㅎ) ㅎㄴ ㅎ] ㅎㄴ', 3)
        _test('ㄴ ㄷㄱ [(ㄱㅇㄱ ㄴㄱ ㅅㅎㄷ ㅎ)'
              '(ㄱㅇㄱ ㄱㅇㄴㄱㅎㄴ ㄴㅇㄷㄱ ㄱㅇㄴㅎㄴ ㄷㅎㄷ ㅎ ㅎ) ㅎㄴ] ㅎㄷ', 0.5)
        _test('ㄹ [ㄴ: ㄱㅇㄱ ㄱㅇㄱ ㄴㄱ ㄷㅎㄷ ㄴㄱㅇㅎㄴ ㄱㅎㄷ?'
              '(ㄱㅇㄱ ㄷ ㅈㅎㄷ)ㅎㄷ ㅎ] ㅎㄴ', 6)

    def test_list_basic(self):
        _test = self._assert_execute
        _test('ㅁㄹ ㅎㄱ', [])
        _test('ㄱ ㄴ ㄷ ㄹ ㅁㄹ ㅎㅁ', [0, 1, 2, 3])
        _test('ㄱ ([ㄱ ㄴ ㄷ] ㅁㄹ ㅎㄹ) ㅎㄴ', 0)
        _test('ㄴ ([ㄱ ㄴ ㄷ] ㅁㄹ ㅎㄹ) ㅎㄴ', 1)
        _test('(ㄷ ㄷㄱ ㅅㅎㄷ ㄹ ㄱㅎㄷ) ([ㄱ ㄴ ㄷ] ㅁㄹ ㅎㄹ) ㅎㄴ', 1)

    def test_string_basic(self):
        _test = self._assert_execute
        _test('ㅁㅈㅎㄱ', '')
        _test('ㄱ ㅁㅈㅎㄴ', '0')
        _test('ㄱㄴ ㅁㅈㅎㄴ', '-8')
        _test('ㄴㄱ ㅁㅈㅎㄴ', '-1')
        _test('(ㄷ ㄴㄱ ㅅㅎㄷ) ㅁㅈㅎㄴ', '0.5')
