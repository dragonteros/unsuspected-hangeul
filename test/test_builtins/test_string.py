from test.test_base import TestBase


class TestString(TestBase):
    def test_split(self):
        _test = self._assert_execute
        _test('ㅀㄱ ㄱㅇㄱ ㅂㅀㄴ ㄳㅎㄶ ㄱㅀㄷ', "['a', 'b', 'c']", 'abc')
        _test('ㅀㄱ ㄱㅇㄱ ㅂㅀㄴ ㄳㅎㄶ ㄱㅀㄷ', "['가', 'a', '1', ' ']", '가a1 ')
        _test('ㅀㄱ ㅀㄱ ㄱㅇㄱ ㄴㅇㄱ ㅂㅀㄷ ㄳㅎㄶ ㄱㅀㄹ', "['a', 'b', 'c']", 'a b c\n ')
        _test('ㅀㄱ ㅀㄱ ㄱㅇㄱ ㄴㅇㄱ ㅂㅀㄷ ㄳㅎㄶ ㄱㅀㄹ', "['평범한', '한글']", '평범한 한글\n ')
        _test('ㅀㄱ ㅀㄱ ㄱㅇㄱ ㄴㅇㄱ ㅂㅀㄷ ㄳㅎㄶ ㄱㅀㄹ', "['평', '범', '한', '한', '글']", '평범한한글\n\n')
        _test('ㅀㄱ ㅀㄱ ㄱㅇㄱ ㄴㅇㄱ ㅂㅀㄷ ㄳㅎㄶ ㄱㅀㄹ', "['']", '\n ')
        _test('ㅀㄱ ㅀㄱ ㄱㅇㄱ ㄴㅇㄱ ㅂㅀㄷ ㄳㅎㄶ ㄱㅀㄹ', "[' ']", ' \n\n')
        _test('ㅀㄱ ㅀㄱ ㄱㅇㄱ ㄴㅇㄱ ㅂㅀㄷ ㄳㅎㄶ ㄱㅀㄹ', "['', '']", ' \n ')

    def test_join(self):
        _test = self._assert_execute
        _test('ㅀㄱ ㅀㄱ ㄱㅇㄱ ㅂㅀㄴ ㄴㅇㄱ ㄱㅁㅎㄷ ㄳㅎㄶ ㄱㅀㄹ', "'a|b|c'", 'abc\n|')
        _test('ㅀㄱ ㅀㄱ ㄱㅇㄱ ㅂㅀㄴ ㄴㅇㄱ ㄱㅁㅎㄷ ㄳㅎㄶ ㄱㅀㄹ', "'산과 들과 강과 별'", '산들강별\n과 ')
