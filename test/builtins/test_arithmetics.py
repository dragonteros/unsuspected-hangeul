from test.test_base import TestBase


class TestArithmetics(TestBase):
    def test_multiply(self):
        _test = self._assert_execute
        _test('ㄱ ㄴ ㄷ ㄹ ㄱㅎㅁ', 0)
        _test('ㄴㄱ ㄴ ㄷ ㄹ ㄱㅎㅁ', -6)
        _test('(ㄱ ㄱ ㅈㅎㄷ) (ㄱ ㄴ ㄴㅎㄷ) ㄱㅎㄷ', False)
        _test('(ㄱ ㄱ ㅈㅎㄷ) (ㄱ ㄴ ㅈㅎㄷ) ㄱㅎㄷ', False)
        _test('(ㄱ ㄱ ㄴㅎㄷ) (ㄱ ㄴ ㅈㅎㄷ) (ㅈㅈㅎㄱ) ㄱㅎㄹ', True)

    def test_add(self):
        _test = self._assert_execute
        _test('ㄱ ㄴ ㄷ ㄹ ㄷㅎㅁ', 6)
        _test('ㄴㄱ ㄴ ㄷ ㄹㄱ ㄷㅎㅁ', -1)
        _test('(ㄱ ㄱ ㅈㅎㄷ) (ㄱ ㄴ ㄴㅎㄷ) ㄷㅎㄷ', False)
        _test('(ㄱ ㄱ ㅈㅎㄷ) (ㄱ ㄴ ㅈㅎㄷ) ㄷㅎㄷ', True)
        _test('(ㄱ ㄱ ㄴㅎㄷ) (ㄱ ㄴ ㅈㅎㄷ) (ㅈㅈㅎㄱ) ㄷㅎㄹ', True)
        _test('ㅁㅀㄱ ㅁㅀㄱ ㄷㅎㄷ', [])
        _test('ㄱ ㅁㅀㄴ ㅁㅀㄱ ㄷㅎㄷ', [0])
        _test('ㄱ ㅁㅀㄴ ㄴ ㄷ ㅁㅀㄷ ㄷㅎㄷ', [0, 1, 2])
        _test('ㄱ ㅁㅀㄴ ㄷㅎㄴ', [0])
        _test('ㅀㄱ ㅀㄱ ㄱㅇㄱ ㄴㅇㄱ ㄷㅎㄷ ㄳㅎㄶ ㄱㅀㄹ', '', '\n\n')
        _test('ㅀㄱ ㅀㄱ ㄱㅇㄱ ㄴㅇㄱ ㄷㅎㄷ ㄳㅎㄶ ㄱㅀㄹ', '불꽃', '불\n꽃')

    def test_exponentiate(self):
        _test = self._assert_execute
        _test('ㄱ ㄴ ㅅㅎㄷ', 0)
        _test('ㄴㄱ ㄴ ㅅㅎㄷ', -1)
        _test('ㄷ ㄴㄱ ㅅㅎㄷ', 0.5)
        _test('ㄴㄱ ㄴㄱ ㅅㅎㄷ', -1)
