from test.test_base import TestBase


class TestSequence(TestBase):
    def test_len(self):
        _test = self._assert_execute
        _test('ㅁㅀㄱ ㅈㄷㅎㄴ', 0)
        _test('ㄱ ㅁㅀㄴ ㅈㄷㅎㄴ', 1)
        _test('ㄱ ㄴ ㅁㅀㄷ ㅈㄷㅎㄴ', 2)
        _test('ㄱ ㅁㅀㄴ ㄴ ㅁㅀㄴ ㄷㅎㄷ ㅈㄷㅎㄴ', 2)

    def test_slice(self):
        _test = self._assert_execute
        _test('ㅁㅀㄱ ㄱ ㅂㅈㅎㄷ', [])
        _test('ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄱ ㅂㅈㅎㄷ', [0, 1, 2, 3, 4])
        _test('ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄴ ㅂㅈㅎㄷ', [1, 2, 3, 4])
        _test('ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄹ ㅂㅈㅎㄷ', [3, 4])
        _test('ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㅂ ㅂㅈㅎㄷ', [])
        _test('ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄴㄱ ㅂㅈㅎㄷ', [4])
        _test('ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄱ ㄷ ㅂㅈㅎㄹ', [0, 1])
        _test('ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄴ ㄴㄱ ㅂㅈㅎㄹ', [1, 2, 3])
        _test('ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄹ ㄹㄱ ㅂㅈㅎㄹ', [])
        _test('ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄹ ㅅ ㅂㅈㅎㄹ', [3, 4])
        _test('ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄱ ㄹ ㄷ ㅂㅈㅎㅁ', [0, 2])
        _test('ㄱ ㄴ ㄷ ㄹ ㅁ ㅁㅀㅂ ㄱ ㄴㄱ ㄹ ㅂㅈㅎㅁ', [0, 3])

    def test_map(self):
        _test = self._assert_execute
        _test('ㅁㅀㄱ ㄱㅇㄱ ㄷ ㅅㅎㄷㅎ ㅁㄷㅎㄷ', [])
        _test('ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁㅀㅂ ㄱㅇㄱ ㄷ ㅅㅎㄷㅎ ㅁㄷㅎㄷ', [1, 0, 1, 4, 9])
        _test('ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁㅀㅂ ㄱㅇㄱ ㅁㅀㄶ ㅁㄷㅎㄷ', [[-1], [0], [1], [2], [3]])

    def test_filter(self):
        _test = self._assert_execute
        _test('ㅁㅀㄱ ㄱ ㄱㅇㄱ ㅈㅎㄷㅎ ㅅㅂㅎㄷ', [])
        _test('ㄴㄱ ㄱ ㄴ ㄷㄱ ㄹ ㅁㅀㅂ ㄱ ㄱㅇㄱ ㅈㅎㄷㅎ ㅅㅂㅎㄷ', [1, 3])
        _test('ㄴㄱ ㄱ ㄴ ㄷㄱ ㄹ ㅁㅀㅂ ㄱㅇㄱ ㄱ ㅈㅎㄷㅎ ㅅㅂㅎㄷ', [-1, -2])
        _test('ㄴㄱ ㄱ ㄴ ㄷㄱ ㄹ ㅁㅀㅂ ㄱㅇㄱ ㄷㄱ ㅈㅎㄷㅎ ㅅㅂㅎㄷ', [])
