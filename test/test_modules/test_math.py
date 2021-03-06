from test.test_base import TestBase


class TestMath(TestBase):
    def test_isclose(self):
        _test = self._assert_execute
        _test('ㄹ (ㄱㅇㄱ ㄱㅇㄱ ㄴㄱ ㅅㅎㄷ ㄱㅎㄷ ㄴ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ)ㅎㄴ', 'True')
        _test('ㅂ ㅅ ㅂ ㅂㅎㄹ (ㄱㅇㄱ ㄱㅇㄱ ㄴㄱ ㅅㅎㄷ ㄱㅎㄷ ㄴ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ)ㅎㄴ', 'True')
        _test('ㅂ ㅅ ㅈ ㅂㅎㄹ (ㄱㅇㄱ ㄱㅇㄱ ㄴㄱ ㅅㅎㄷ ㄱㅎㄷ ㄴ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ)ㅎㄴ', 'True')
        _test('ㅈㅈㅈ ㄴㄱ ㅅㅎㄷ ㅅㅈㅈ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷ', 'False')
        _test('ㅈㅈㅈㅈㅈㅈㅈ ㄴㄱ ㅅㅎㄷ ㅅㅈㅈㅈㅈㅈㅈ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷ', 'False')
        _test('ㅅㄷㄱ ㅈ ㄴㄱ ㅅㅎㄷ ㄱㅎㄷ (ㅂ ㅅ ㅂ ㅂㅎㄹ) (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷ', 'False')
        _test('ㄴㅈㄱㄹㄴㄹㄱ ㅅㄴㅂㄱㄱㄴㄱ ㄴㄱ ㅅㅎㄷ ㄱㅎㄷ (ㅂ ㅅ ㅂ ㅂㅎㄹ) (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷ', 'True')
        _test('(ㅂ ㅅ ㅈ ㅂㅎㄹ) (ㄱ ㅂ ㅅ ㅂ ㅂㅎㄹ ㅄㅎㄷ) ㅅㅎㄷ, ㄴㄱ, (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷ', 'True')
        _test('ㄱㄴ ㄷ (ㄱㅇㄱ ㄴㅇㄱ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ ㄴㅇㄱ ㅅㅎㄷ, ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ)ㅎㄷ', 'True')
        _test('ㄱㄴ ㄹ (ㄱㅇㄱ ㄴㅇㄱ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ ㄴㅇㄱ ㅅㅎㄷ, ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ)ㅎㄷ', 'True')
        _test('ㄱㄴ ㅁ (ㄱㅇㄱ ㄴㅇㄱ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ ㄴㅇㄱ ㅅㅎㄷ, ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ)ㅎㄷ', 'True')
        _test('ㄴㄱ ㄷ (ㄱㅇㄱ ㄴㅇㄱ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ ㄴㅇㄱ ㅅㅎㄷ, ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ)ㅎㄷ', 'True')
        _test('ㄴㄱ ㄹ (ㄱㅇㄱ ㄴㅇㄱ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ ㄴㅇㄱ ㅅㅎㄷ, ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ)ㅎㄷ', 'True')
        _test('ㄴㄱ ㅁ (ㄱㅇㄱ ㄴㅇㄱ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ ㄴㅇㄱ ㅅㅎㄷ, ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ)ㅎㄷ', 'True')

    def test_isnan(self):
        _test = self._assert_execute
        _test('(ㅂ ㅅ ㄴ ㅂㅎㄹ) (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('(ㅂ ㅅ ㅁ ㅂㅎㄹ) (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('ㄱ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('ㄴ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('(ㅂ ㅅ ㄴ ㅂㅎㄹ) ㄴ ㅄㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('ㄱ (ㅂ ㅅ ㄴ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('ㄴ (ㅂ ㅅ ㄴ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('(ㅂ ㅅ ㄴ ㅂㅎㄹ) (ㅂ ㅅ ㄴ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('(ㅂ ㅅ ㅁ ㅂㅎㄹ) (ㅂ ㅅ ㄴ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('(ㅂ ㅅ ㄴ ㅂㅎㄹ) (ㅂ ㅅ ㅁ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('ㅂ ㅅ ㅁ ㅂㅎㄹ ㄴㄱ ㄱㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('(ㅂ ㅅ ㅁ ㅂㅎㄹ) ㄴ ㅄㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('ㄱ (ㅂ ㅅ ㅁ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('ㄴ (ㅂ ㅅ ㅁ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('(ㅂ ㅅ ㅁ ㅂㅎㄹ) (ㅂ ㅅ ㅁ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('ㄱ (ㅂ ㅅ ㅁ ㅂㅎㄹ ㄴㄱ ㄱㅎㄷ) ㅄㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('ㄱ (ㅂ ㅅ ㅁ ㅂㅎㄹ ㄴㄱ ㄱㅎㄷ) ㅄㅎㄷ (ㅂ ㅅ ㄴㄴ ㅂㅎㄹ)ㅎㄴ', 'False')

    def test_isinf(self):
        _test = self._assert_execute
        _test('(ㅂ ㅅ ㅁ ㅂㅎㄹ) (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('(ㅂ ㅅ ㄴ ㅂㅎㄹ) (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('ㄱ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('ㄴ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('ㅂ ㅅ ㅁ ㅂㅎㄹ ㄴㄱ ㄱㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('(ㅂ ㅅ ㅁ ㅂㅎㄹ) ㄴ ㅄㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('(ㅂ ㅅ ㅁ ㅂㅎㄹ ㄴㄱ ㄱㅎㄷ) ㄴ ㅄㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('(ㅂ ㅅ ㅁ ㅂㅎㄹ) (ㅂ ㅅ ㄴ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('ㄱ (ㅂ ㅅ ㅁ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('ㄴ (ㅂ ㅅ ㅁ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('(ㅂ ㅅ ㄴ ㅂㅎㄹ) (ㅂ ㅅ ㅁ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('(ㅂ ㅅ ㅁ ㅂㅎㄹ) (ㅂ ㅅ ㅁ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('ㄱ (ㅂ ㅅ ㅁ ㅂㅎㄹ ㄴㄱ ㄱㅎㄷ) ㅄㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'True')
        _test('(ㅂ ㅅ ㄴ ㅂㅎㄹ) ㄴ ㅄㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('ㄱ (ㅂ ㅅ ㄴ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('ㄴ (ㅂ ㅅ ㄴ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'False')
        _test('(ㅂ ㅅ ㄴ ㅂㅎㄹ) (ㅂ ㅅ ㄴ ㅂㅎㄹ) ㅄㅎㄷ (ㅂ ㅅ ㅁㄴ ㅂㅎㄹ)ㅎㄴ', 'False')

    def test_abs(self):
        _test = self._assert_execute
        _test('ㄱ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '0')
        _test('ㄱ ㄷ ㄴㄱ ㅅㅎㄷ ㄱㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '0.0')
        _test('ㄱ ㅄㅎㄴ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '0.0')
        _test('ㄴ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '1')
        _test('ㄴㄱ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '1')
        _test('ㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '2')
        _test('ㄷㄱ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '2')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '0.5')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '0.5')
        _test('ㅁ ㄴㄱ ㅅㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '0.25')
        _test('ㅁㄱ ㄴㄱ ㅅㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '0.25')
        _test('ㄴ ㅄㅎㄴ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '1.0')
        _test('ㄴㄱ ㅄㅎㄴ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '1.0')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ ㅄㅎㄴ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '0.5')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ ㅄㅎㄴ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '0.5')
        _test('ㄱ ㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '1.0')
        _test('ㄱ ㄴㄱ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '1.0')
        _test('ㄱ ㄷ ㄴㄱ ㅅㅎㄷ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '0.5')
        _test('ㄱ ㄷㄱ ㄴㄱ ㅅㅎㄷ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ', '0.5')
        _test('ㄹ ㅁ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㅂ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㄹㄱ ㅁ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㅂ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㄹ ㅁㄱ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㅂ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㄹㄱ ㅁㄱ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㅂ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㅂ ㅁㄴㄱ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㅂㄴㄱ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㅂㄱ ㅁㄴㄱ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㅂㄴㄱ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㅂ ㅁㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㅂㄴㄱ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㅂㄱ ㅁㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㅂㄴㄱ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㄴㄱ ㄷ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㄴ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㄴㄱ ㄹ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㄴ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㄴㄱ ㅁ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㄴ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㅁㄱ ㄷ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㄷ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㄱㄴ ㄹ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㄷ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')
        _test('ㄱㄷ ㅁ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㄷ ㅂ ㅅ ㄱ ㅂㅎㅀㄷ', 'True')

    def test_log(self):
        _test = self._assert_execute
        _test('ㄴ [((ㅂ ㅅ ㅈ ㅂㅎㄹ) (ㄱㅇㄱ ㅂ ㅅ ㄺ ㅂㅎㅀㄴ) ㅅㅎㄷ) ㄱㅇㄱ ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴㄱ [(ㅂ ㅅ ㅈ ㅂㅎㄹ (ㄱㅇㄱ ㅂ ㅅ ㄺ ㅂㅎㅀㄴ) ㅅㅎㄷ) ㄱㅇㄱ ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄷㄱ [(ㅂ ㅅ ㅈ ㅂㅎㄹ (ㄱㅇㄱ ㅂ ㅅ ㄺ ㅂㅎㅀㄴ) ㅅㅎㄷ) ㄱㅇㄱ ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄷ [(ㅂ ㅅ ㅈ ㅂㅎㄹ (ㄱㅇㄱ ㅂ ㅅ ㄺ ㅂㅎㅀㄴ) ㅅㅎㄷ) ㄱㅇㄱ ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴㄱ ㄹ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ [(ㅂ ㅅ ㅈ ㅂㅎㄹ (ㄱㅇㄱ ㅂ ㅅ ㄺ ㅂㅎㅀㄴ) ㅅㅎㄷ) ㄱㅇㄱ ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')

    def test_trig(self):
        _test = self._assert_execute
        _test('ㄱ (ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ) ㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷ', 'True')
        _test('[ㅈㄱ ㅅㄱ ㅂㄱ ㅁㄱ ㄺ ㄷㄱ ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ ㅈ] ㅁㅀㅈㄴㄱ [ㅂ ㅅ ㅂ ㅂㅎㄹ (ㄱㅇㄱ ㄷ ㄱㅎㄷ ㄷ ㄴㄱ ㅅㅎㄷ ㄷㅎㄷ) ㄱㅎㄷ (ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ) ㄴ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ] ㅁㄷㅎㄷ (ㄱ ㅁㅂㅎㄴ)ㅎㄴ', 'True')
        _test('[ㅈㄱ ㅅㄱ ㅂㄱ ㅁㄱ ㄺ ㄷㄱ ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ ㅈ] ㅁㅀㅈㄴㄱ [ㅂ ㅅ ㅂ ㅂㅎㄹ (ㄱㅇㄱ ㄷ ㄱㅎㄷ ㄷㄱ ㄴㄱ ㅅㅎㄷ ㄷㅎㄷ) ㄱㅎㄷ (ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ) ㄴㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ] ㅁㄷㅎㄷ (ㄱ ㅁㅂㅎㄴ)ㅎㄴ', 'True')
        _test('ㄱ (ㅂ ㅅ ㄳ ㅂㅎㅀㄴ) ㄴ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷ', 'True')
        _test('[ㅈㄱ ㅅㄱ ㅂㄱ ㅁㄱ ㄺ ㄷㄱ ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ ㅈ] ㅁㅀㅈㄴㄱ [ㅂ ㅅ ㅂ ㅂㅎㄹ (ㄱㅇㄱ ㄷ ㄱㅎㄷ) ㄱㅎㄷ (ㅂ ㅅ ㄳ ㅂㅎㅀㄴ) ㄴ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ] ㅁㄷㅎㄷ (ㄱ ㅁㅂㅎㄴ)ㅎㄴ', 'True')
        _test('[ㅈㄱ ㅅㄱ ㅂㄱ ㅁㄱ ㄺ ㄷㄱ ㄴㄱ ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ ㅈ] ㅁㅀㅈㄴㄱ [ㅂ ㅅ ㅂ ㅂㅎㄹ (ㄱㅇㄱ ㄷ ㄱㅎㄷ ㄴ ㄷㅎㄷ) ㄱㅎㄷ (ㅂ ㅅ ㄳ ㅂㅎㅀㄴ) ㄴㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ] ㅁㄷㅎㄷ (ㄱ ㅁㅂㅎㄴ)ㅎㄴ', 'True')
        _test('ㄱ (ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ) ㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷ', 'True')
        _test('(ㅂ ㅅ ㅂ ㅂㅎㄹ ㅁ ㄴㄱ ㅅㅎㄷ ㄱㅎㄷ) (ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ) ㄴ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷ', 'True')
        _test('(ㅂ ㅅ ㅂ ㅂㅎㄹ ㅁㄱ ㄴㄱ ㅅㅎㄷ ㄱㅎㄷ) (ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ) ㄴㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷ', 'True')
        _test('(ㅂ ㅅ ㅂ ㅂㅎㄹ ㄹ ㄴㄱ ㅅㅎㄷ ㄱㅎㄷ) (ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ) (ㄹ ㄷ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ) (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷ', 'True')
        _test('(ㅂ ㅅ ㅂ ㅂㅎㄹ ㅅ ㄴㄱ ㅅㅎㄷ ㄱㅎㄷ) (ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ) (ㄹ ㄷㄱ ㄴㄱ ㅅㅎㄷ ㅅㅎㄷ) (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷ', 'True')
        _test('ㄱ [(ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㄱㅇㄱ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ) ㄴ ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ [(ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㄱㅇㄱ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ) ㄴ ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴㄱ [(ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㄱㅇㄱ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ) ㄴ ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄷ [(ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㄱㅇㄱ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ) ㄴ ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄷㄱ [(ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㄱㅇㄱ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ) ㄴ ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㅂ ㅅ ㅂ ㅂㅎㄹ [(ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㄱㅇㄱ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ) ㄴ ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄱ [(ㄱㅇㄱ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ ㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㄷ ㅅㅎㄷ) (ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㄷㄱ ㅅㅎㄷ) ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ [(ㄱㅇㄱ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ ㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㄷ ㅅㅎㄷ) (ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㄷㄱ ㅅㅎㄷ) ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴㄱ [(ㄱㅇㄱ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ ㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㄷ ㅅㅎㄷ) (ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㄷㄱ ㅅㅎㄷ) ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄷ [(ㄱㅇㄱ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ ㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㄷ ㅅㅎㄷ) (ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㄷㄱ ㅅㅎㄷ) ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㄷㄱ [(ㄱㅇㄱ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ ㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㄷ ㅅㅎㄷ) (ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㄷㄱ ㅅㅎㄷ) ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')
        _test('ㅂ ㅅ ㅂ ㅂㅎㄹ [(ㄱㅇㄱ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ ㄴ ㅄㅎㄷ ㅂ ㅅ ㅈㄷ ㅂㅎㅀㄴ ㄷ ㅅㅎㄷ) (ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㄷㄱ ㅅㅎㄷ) ㅂ ㅅ ㄱ ㅂㅎㅀㄷㅎ]ㅎㄴ', 'True')

    def test_asin(self):
        _test = self._assert_execute
        _test('ㄱ [(ㄱㅇㄱ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ ㅂ ㅅ ㄴㅅ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ [(ㄱㅇㄱ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ ㅂ ㅅ ㄴㅅ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴㄱ [(ㄱㅇㄱ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ ㅂ ㅅ ㄴㅅ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄱ ㄴ ㅄㅎㄷ [(ㄱㅇㄱ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ ㅂ ㅅ ㄴㅅ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ ㄴ ㅄㅎㄷ [(ㄱㅇㄱ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ ㅂ ㅅ ㄴㅅ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄱ [(ㄱㅇㄱ ㅂ ㅅ ㄴㅅ ㅂㅎㅀㄴ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ[(ㄱㅇㄱ ㅂ ㅅ ㄴㅅ ㅂㅎㅀㄴ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴㄱ[(ㄱㅇㄱ ㅂ ㅅ ㄴㅅ ㅂㅎㅀㄴ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄱ ㄴ ㅄㅎㄷ[(ㄱㅇㄱ ㅂ ㅅ ㄴㅅ ㅂㅎㅀㄴ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ ㄴ ㅄㅎㄷ[(ㄱㅇㄱ ㅂ ㅅ ㄴㅅ ㅂㅎㅀㄴ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')

    def test_acos(self):
        _test = self._assert_execute
        _test('ㄱ [(ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㅂ ㅅ ㅅㄱ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ [(ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㅂ ㅅ ㅅㄱ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄱ ㄴ ㅄㅎㄷ [(ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㅂ ㅅ ㅅㄱ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ ㄴ ㅄㅎㄷ [(ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ ㅂ ㅅ ㅅㄱ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ[(ㄱㅇㄱ ㅂ ㅅ ㅅㄱ ㅂㅎㅀㄴ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴㄱ[(ㄱㅇㄱ ㅂ ㅅ ㅅㄱ ㅂㅎㅀㄴ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄱ ㄴ ㅄㅎㄷ[(ㄱㅇㄱ ㅂ ㅅ ㅅㄱ ㅂㅎㅀㄴ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ ㄴ ㅄㅎㄷ[(ㄱㅇㄱ ㅂ ㅅ ㅅㄱ ㅂㅎㅀㄴ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')

    def test_atan(self):
        _test = self._assert_execute
        _test('ㄱ [(ㄱㅇㄱ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ ㅂ ㅅ ㄴㄷ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ [(ㄱㅇㄱ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ ㅂ ㅅ ㄴㄷ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴㄱ [(ㄱㅇㄱ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ ㅂ ㅅ ㄴㄷ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄱ ㄴ ㅄㅎㄷ [(ㄱㅇㄱ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ ㅂ ㅅ ㄴㄷ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ ㄴ ㅄㅎㄷ [(ㄱㅇㄱ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ ㅂ ㅅ ㄴㄷ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄱ [(ㄱㅇㄱ ㅂ ㅅ ㄴㄷ ㅂㅎㅀㄴ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴ[(ㄱㅇㄱ ㅂ ㅅ ㄴㄷ ㅂㅎㅀㄴ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')
        _test('ㄴㄱ[(ㄱㅇㄱ ㅂ ㅅ ㄴㄷ ㅂㅎㅀㄴ ㅂ ㅅ ㄷㄴ ㅂㅎㅀㄴ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ]ㅎㄴ', 'True')

    def test_atan2(self):
        _test = self._assert_execute
        _test('ㄱ ㄴ ㅂ ㅅ ㄴㄷ ㅂㅎㄹ ㅎㄷ', '0.0')
        _test('ㄱ ㄴㄱ ㅂ ㅅ ㄴㄷ ㅂㅎㄹ ㅎㄷ (ㅂ ㅅ ㅂ ㅂㅎㄹ)ㄶㄷ', 'True')
        _test('(ㄴ ㄱ ㅂ ㅅ ㄴㄷ ㅂㅎㄹ ㅎㄷ) ㄷ ㄱㅎㄷ (ㅂ ㅅ ㅂ ㅂㅎㄹ)ㄶㄷ', 'True')
        _test('(ㄴㄱ ㄱ ㅂ ㅅ ㄴㄷ ㅂㅎㄹ ㅎㄷ) ㄷㄱ ㄱㅎㄷ (ㅂ ㅅ ㅂ ㅂㅎㄹ)ㄶㄷ', 'True')
        _test('[ㄴ ㄴㄱ ㄷ ㄷㄱ ㄹ ㄺ ㅁㅀㅅ] [(ㄱㅇㄱ ㅂ ㅅ ㅅㄴ ㅂㅎㅀㄴ, ㄱㅇㄱ ㅂ ㅅ ㄳ ㅂㅎㅀㄴ, ㅂ ㅅ ㄴㄷ ㅂㅎㅀㄷ) ㄱㅇㄱ (ㅂ ㅅ ㄱ ㅂㅎㄹ)ㅎㄷㅎ] ㅁㄷㅎㄷ (ㄱ ㅁㅂㅎㄴ)ㅎㄴ', 'True')

    def test_trunc(self):
        _test = self._assert_execute
        _test('ㄱ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㅁ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㅁㄱ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㄴ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '1')
        _test('ㄴㄱ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '-1')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ ㄹ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '1')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ ㄹ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '-1')
        _test('ㄷ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '2')
        _test('ㄷㄱ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '-2')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ ㅂ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '2')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ ㅂ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄱ ㅂㅎㅁ)ㅎㄴ', '-2')

    def test_floor(self):
        _test = self._assert_execute
        _test('ㄱ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㅁ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㅁㄱ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '-1')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '-1')
        _test('ㄴ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '1')
        _test('ㄴㄱ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '-1')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ ㄹ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '1')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ ㄹ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '-2')
        _test('ㄷ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '2')
        _test('ㄷㄱ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '-2')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ ㅂ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '2')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ ㅂ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄴ ㅂㅎㅁ)ㅎㄴ', '-3')

    def test_round(self):
        _test = self._assert_execute
        _test('ㄱ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㅁ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㅁㄱ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㄴ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '1')
        _test('ㄴㄱ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '-1')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ ㄹ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '2')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ ㄹ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '-2')
        _test('ㄷ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '2')
        _test('ㄷㄱ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '-2')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ ㅂ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '2')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ ㅂ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄷ ㅂㅎㅁ)ㅎㄴ', '-2')

    def test_ceil(self):
        _test = self._assert_execute
        _test('ㄱ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㅁ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '1')
        _test('ㅁㄱ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '1')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㄴ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '1')
        _test('ㄴㄱ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '-1')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ ㄹ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '2')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ ㄹ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '-1')
        _test('ㄷ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '2')
        _test('ㄷㄱ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '-2')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ ㅂ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '3')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ ㅂ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㄹ ㅂㅎㅁ)ㅎㄴ', '-2')

    def test_round_to_inf(self):
        _test = self._assert_execute
        _test('ㄱ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '0')
        _test('ㅁ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '1')
        _test('ㅁㄱ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '-1')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '1')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '-1')
        _test('ㄴ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '1')
        _test('ㄴㄱ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '-1')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ ㄹ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '2')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ ㄹ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '-2')
        _test('ㄷ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '2')
        _test('ㄷㄱ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '-2')
        _test('ㄷ ㄴㄱ ㅅㅎㄷ ㅂ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '3')
        _test('ㄷㄱ ㄴㄱ ㅅㅎㄷ ㅂ ㄱㅎㄷ (ㅂ ㅅ ㅂㄹ ㅁ ㅂㅎㅁ)ㅎㄴ', '-3')
