from test.test_base import TestBase


class TestLogic(TestBase):
    def test_equals_basic(self):
        _test = self._assert_execute
        _test('ㄶㄱ', True)
        _test('ㄴ (ㄴㄱ ㄴㄱ ㄱㅎㄷ) (ㄴㄱ ㄷ ㅅㅎㄷ) ㄶㄹ', True)
        _test('ㅈㅈㅎㄱ (ㄱ ㄴ ㅈㅎㄷ) ㄶㄷ', True)
        _test('ㄱㅈㅎㄱ (ㄱ ㄴ ㅈㅎㄷ) ㄶㄷ', False)
        _test('ㅁㅈㅎㄱ ㅁㅈㅎㄱ ㄶㄷ', True)
        _test('ㄱ ㅁㅈㅎㄴ ㄱ (ㅈ ㄴㄱ ㅅㅎㄷ) ㄱㅎㄷ ㅁㅈㅎㄴ ㄶㄷ', True)

    def test_equals_list(self):
        _test = self._assert_execute
        _test('''(ㄴㄱ ㄱ ㄴ ㅁㅀㄹ) (ㄱㅇㄱ ㄱㅇㄱ ㄶㄷㅎ)ㅎㄴ''', True)
        _test('''(ㄴㄱ ㄱ ㄴ ㅁㅀㄹ) (
            ㄱㅇㄱ (ㄱㅇㄱ (ㄱㅇㄱㅎ) ㅁㄷㅎㄷ)
            ㄶㄷㅎ)ㅎㄴ''', True)
        _test('''(ㄴㄱ ㄱ ㄴ ㅁㅀㄹ) (
            ㄱㅇㄱ (ㄱㅇㄱ (ㄱㅇㄱ ㄹ ㅅㅎㄷㅎ) ㅁㄷㅎㄷ)
            ㄶㄷㅎ)ㅎㄴ''', True)
        _test('''(ㄴㄱ ㄱ ㄴ ㅁㅀㄹ) (
            ㄱㅇㄱ (ㄱㅇㄱ (ㄱㅇㄱ ㄹ ㅅㅎㄷㅎ) ㅁㄷㅎㄷ)
            ㄶㄷㅎ)ㅎㄴ''', True)
        _test('ㄱ ㄴ ㅁㅀㄷ ㄱ ㅁㅀㄴ ㄶㄷ', False)
        _test('ㄱ ㄴ ㅁㅀㄷ ㅂㄱㅎㄱ ㄶㄷ', False)

    def test_equals_other(self):
        _test = self._assert_execute
        _test('ㅂㄱㅎㄱ ㅂㄱㅎㄱ ㄶㄷ', True)
        _test('(ㄱ ㅁㅈㅎㄴ ㅈㅀㄴ) (ㄱㅇㄱ ㅂㄱㅎㄱ ㄶㄷㅎ) ㄱㅀㄷ', True, '', '0')
        _test('ㄶ (ㄱㅇㄱ ㄱㅇㄱ ㄶㄷㅎ)ㅎㄴ', True)
        _test('ㄶ (ㄱㅇㄱ ㄶ ㄶㄷㅎ)ㅎㄴ', False)
        _test('ㄶ ㄶ (ㄱㅇㄱ ㄴㅇㄱ ㄶㄷㅎ)ㅎㄷ', False)
        _test('ㄷ ㄳㅎㄴ (ㄱㅇㄱ ㄱㅇㄱ ㄶㄷㅎ)ㅎㄴ', True)
        _test('ㄷ ㄳㅎㄴ (ㄱㅇㄱ ㄷ ㄳㅎㄴ ㄶㄷㅎ)ㅎㄴ', True)
        _test('ㄷ ㄳㅎㄴ ㄷ ㄳㅎㄴ (ㄱㅇㄱ ㄴㅇㄱ ㄶㄷㅎ)ㅎㄷ', True)

    def test_negate(self):
        _test = self._assert_execute
        _test('ㅈㅈㅎㄱ ㅁㅎㄴ', False)
        _test('ㄱㅈㅎㄱ ㅁㅎㄴ', True)

    def test_less_than(self):
        _test = self._assert_execute
        _test('ㄴ ㄷ ㅈㅎㄷ', True)
        _test('ㄷ ㄷ ㅈㅎㄷ', False)
        _test('ㄹ ㄷ ㅈㅎㄷ', False)

    def test_true(self):
        _test = self._assert_execute
        _test('ㅈㅈㅎㄱ', True)
        _test('ㄱ ㄴ ㅈㅈㅎㄱㅎㄷ', 0)

    def test_false(self):
        _test = self._assert_execute
        _test('ㄱㅈㅎㄱ', False)
        _test('ㄱ ㄴ ㄱㅈㅎㄱㅎㄷ', 1)
