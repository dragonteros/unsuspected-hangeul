from test.test_base import TestBase


class TestModule(TestBase):
    def test_load_from_path(self):
        _test = self._assert_execute
        _test('(ㅂ ㅂ ㅂㅎㄷ) ㅁㅂㅈㄱㄷㄴㅁㅂㄷㅂㄹㄱㄹㄹㄱㅁㄷㅂㄹㅁㄹㄴㄱㅁㅈㅂㅁㅅㅅㄹㅁㅁㅁㄹㄷㅈㄷㄱㅂㄹㄱㅈㄴㄷㅈ (ㄴ ㄴㄷㄱ ㄱㅇㄱㅎㄷ)ㅎㄴ (ㄱ ㄴ ㄱㅇㄱㅎㄷ)ㅎㄴ ㅎㅎㄴ ㅂㅎㄴ', "'ㄱㄴㄷㄹㅁㅂㅅㅈ'")
        _test('(ㅂ ㅂ ㅂㅎㄷ) ㅅㅂㅁㅈㄷㄱㄹㅈㄴㅁㄷㄱㄹㅂㄷㅈㄱㅅㅅㄱㄱㅂㄷㅈㄱㅈㄷㄱㄱㅈㄹㄴㅂㅂㅈㅈㄱㄹㄷㅁㄹㅂㄹㄴㄹㄴㅂㅁㅁㅂㄹㅁㄱㅈㄷㅂㅁㅂㄹㅈㄴㄴㅁㅁㅅㅂㄱㄷㅈㄱㅅㄹㅁㅅㄴ (ㄴ ㅁㄹㄱ ㄱㅇㄱㅎㄷ)ㅎㄴ (ㄱ ㄴ ㄱㅇㄱㅎㄷ)ㅎㄴ ㅎㅎㄴ ㅂㅎㄴ (ㅂ ㅂ ㅂㅎㄷ) ㅁㅂㅈㄱㄷㄴㅁㅂㄷㅂㄹㄱㄹㄹㄱㅁㄷㅂㄹㅁㄹㄴㄱㅁㅈㅂㅁㅅㅅㅈㄹㅁㄴㄴㅅㅂㅅㅂㅁㅂㅁㄷㄷㅅㅅㄴㄷㅁㄹㅂㄷㅅㅅㅂㅈㅁㄱㄷㄷㅈㄷㄱㅂㄹㄱㅈㄴㄷㅈ (ㄴ ㄷㄹㄱ ㄱㅇㄱㅎㄷ)ㅎㄴ (ㄱ ㄴ ㄱㅇㄱㅎㄷ)ㅎㄴ ㅎㅎㄴ ㅂㅎㄴ ㄶㄷ', "True")

    def test_load_from_literal(self):
        _test = self._assert_execute
        _test('조각글 표 ㅂㅎㄷ', "'ㄱㄴㄷㄹㅁㅂㅅㅈ'")
        _test('ㄱ 조각글 팔로나눈몫 ㅂㅎㄷ ㅎㄴ', "0")
        _test('ㄷㄴㄱ 조각글 팔로나눈몫 ㅂㅎㄷ ㅎㄴ', "1")
        _test('ㄱ 조각글 팔로나눈나머지 ㅂㅎㄷ ㅎㄴ', "0")
        _test('ㄷㄴㄱ 조각글 팔로나눈나머지 ㅂㅎㄷ ㅎㄴ', "2")
        _test('ㄱ 조각글 평범숫자 ㅂㅎㄷ ㅎㄴ', "'ㄱ'")
        _test('ㄴ 조각글 평범숫자 ㅂㅎㄷ ㅎㄴ', "'ㄴ'")
        _test('ㄴㄱ 조각글 평범숫자 ㅂㅎㄷ ㅎㄴ', "'ㄴㄱ'")
        _test('ㄴㄴ 조각글 평범숫자 ㅂㅎㄷ ㅎㄴ', "'ㄴㄴ'")
        _test('ㄱㄴㄷㄻ 조각글 평범숫자 ㅂㅎㄷ ㅎㄴ', "'ㄱㄴㄷㄹㅁ'")
        _test('조각글 평범숫자 ㅂㅎㄷ 조각글 평범숫자 ㅂㅎㄷ ㄶㄷ', "True")
        _test('조각글 문자만드는평범코드드립니다 ㅂㅎㄷ', "Nil", '유구한 역사와 전통에 빛나는 우리 대한국민은 3·1운동으로 건립된 대한민국임시정부의 법통과 불의에 항거한 4·19민주이념을 계승하고, 조국의 민주개혁과 평화적 통일의 사명에 입각하여 정의·인도와 동포애로써 민족의 단결을 공고히 하고, 모든 사회적 폐습과 불의를 타파하며, 자율과 조화를 바탕으로 자유민주적 기본질서를 더욱 확고히 하여 정치·경제·사회·문화의 모든 영역에 있어서 각인의 기회를 균등히 하고, 능력을 최고도로 발휘하게 하며, 자유와 권리에 따르는 책임과 의무를 완수하게 하여, 안으로는 국민생활의 균등한 향상을 기하고 밖으로는 항구적인 세계평화와 인류공영에 이바지함으로써 우리들과 우리들의 자손의 안전과 자유와 행복을 영원히 확보할 것을 다짐하면서 1948년 7월 12일에 제정되고 8차에 걸쳐 개정된 헌법을 이제 국회의 의결을 거쳐 국민투표에 의하여 개정한다.', '(ㅂ ㅂ ㅂㅎㄷ) ㅁㅂㄹㅅㄴㄴㄱㅂㄷㅂㅈㄷㄹㄴㄹㅂㅂㅂㅈㄷㄴㄴㅈㅁㄱㅁㄱㅅㅅㅈㅂㅁㅂㅂㄷㅅㅅㅂㄱㅁㅁㅂㄷㅅㅅㄹㅅㅁㄱㄱㄷㄱㄷㄱㄹㅈㄱㅁㄷㄷㄱㄹㄹㅈㅅㄱㅅㄷㄹㄴㄹㅈㅈㄷㄷㄱㄴㄴㄱㄴㄹㅂㅈㅁㄹㅈㅅㅁㄹㅂㄹㄴㄱㄴㅅㅁㄹㅂㄹㅂㄱㄴㅂㅁㄱㅁㄱㅅㅅㅂㅅㅁㄱㅅㅅㅂㅅㅂㄴㅂㅁㅂㄷㄱㄷㅅㄷㅈㅁㄴㄷㄱㄱㄹㄹㅈㅂㄷㄷㅅㄴㅂㄷㅈㅂㅅㅅㅅㄷㅈㄷㅈㅈㅂㄷㅅㄹㄴㄹㅈㅂㄹㄷㄱㄱㄴㄱㄴㄹㅅㄱㄴㅁㅈㅂㅂㄴㅅㄱㅅㅅㅂㅅㅁㅁㅅㅅㅂㅅㅈㄹㅁㄴㄹㄷㅅㅅㄴㅈㅁㅁㅈㅅㅂㅅㄹㄱㅂㅁㄹㄷㄱㄷㅁㄷㅈㄴㅅㄷㄷㄹㅈㄷㅈㅅㅁㅅㅅㄹㅈㄷㅈㄱㄷㄷㅅㄴㄴㄱㄴㄹㅂㄹㅅㄱㄴㄱㅁㅂㅂㅈㄷㄴㄴㅈㅁㄹㅂㅈㅈㄷㄴㅈㅂㄷㅂㅈㄷㄹㄹㄹㅂㅁㅂㄹㅈㄴㄴㄴㅁㅁㅂㅈㅂㄱㄴㅈㅁㅁㅂㄹㄱㄷㄹㅂㅁㄹㅂㄹㄹㄹㄴㄱㅁㅁㅂㅈㅅㄴㄴㅅㅁㄱㅁㅁㅂㅅㅂㅁㅂㅂㄷㅅㅅㅅㅂㄴㅁㅂㅅㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㅅㄷㅈㅅㅅㄷㅁㄱㄴㄹㅈㅂㄹㄷㅁㄴㄴㄹㅈㅈㄷㄷㄱㄴㄴㄱㄴㅂㅂㅈㄷㄴㄹㄹㅂㄷㅂㅈㄱㄹㄴㅁㅂㅂㅂㅈㄷㄴㄴㅈㅁㄱㅁㄱㄷㄹㅁㄱㅅㅈㅅㅅㄱㄹㄷㅅㄴㄹㅂㅈㅈㄷㄴㅈㅂㅁㅂㅈㄴㄷㄴㅈㅂㅁㅂㅈㅅㄴㄴㅂㅂㄹㅂㅈㄷㄱㄴㅁㅁㅁㅂㅈㅅㄴㄴㄴㅁㄱㅁㄱㅂㅅㅈㅁㅂㅁㄱㄷㅅㅅㅂㄷㅁㄴㅈㅅㅅㅅㄹㅂㅁㄱㄹㄷㅂㅅㅈㅁㅂㄱㅁㄷㅅㄷㄱㄱㄴㅁㅂㅈㄱㄷㄴㅁㅂㄷㅂㅈㄷㄹㄹㄹㅂㅁㅂㅈㅅㄴㄴㅅㅁㄱㅁㅁㅂㅅㅈㄹㅂㅁㅈㄷㅅㅅㅈㄱㅂㅁㅈㄷㅂㅅㄴㅁㅂㅁㄹㅅㅅㅅㄴㅅㅁㄴㄱㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㄷㄹㅈㅈㄴㅅㅁㄱㄹㄹㅈㄴㄹㄷㄷㄴㄴㄹㅈㄱㅁㅅㄱㄱㄴㄱㄴㅂㅂㄹㄹㄱㄹㅂㅂㅁㅂㅈㅅㄴㄴㅈㅂㅁㅂㅈㅅㄴㄴㅅㅁㄱㅁㄱㅅㅅㅂㄱㅁㅁㅂㅅㅂㅅㅂㄷㅂㅂㄱㄷㅅㅅㅈㅂㅁㄱㄷㄷㄱㄷㄱㄹㅈㅅㄹㅅㄷㄱㅂㄷㅈㄱㅅㅅㄱㄱㄹㄹㅈㅂㄷㄷㅁㄴㄴㄹㅈㅈㄷㄷㅅㄷㄴㄱㄴㅁㅂㄹㄱㄷㄹㅂㅁㅁㅂㅈㅅㄴㄴㅅㅁㄷㄱㅈㄹㄹㄴㄹㅈㅂㄹㄷㅁㄹㅈㄷㅈㅈㄴㄷㄷㄱㄴㄹㅈㄴㄹㄷㄱㄱㄴㄱㄴㄹㅂㅈㅈㄱㄹㅅㅁㅂㅂㅈㅈㄱㄴㄹㅂㅁㅂㅈㄷㄴㄴㄱㅂㄹㅂㅈㄱㄷㄴㅈㅁㅁㅂㅈㅅㄱㄴㄷㅂㄱㅁㅁㅂㅅㅈㄹㅂㅁㅈㄷㅅㅅㄹㄱㅂㄴㅅㄷㅅㅅㄹㅈㅁㄱㄹㄷㄱㄷㅅㄷㅈㄹㄴㄷㅁㄷㅂㄷㅈㄷㅅㄷㄱㄹㄴㄹㅈㅂㄹㄷㄷㄱㄴㄱㄴㄷㅂㅈㄴㄹㄹㅂㅂㄷㅂㅈㄴㄹㄴㄱㅂㅂㅂㄹㅈㄴㄴㄷㅁㄱㅁㅁㅅㅅㄹㅂㅁㄱㄹㄷㅂㅅㅈㅁㅂㄱㅁㄷㅅㄷㄱㄱㄴㄹㅂㄹㅂㄷㄴㄷㅂㄹㅂㅈㄴㄴㄴㄱㅂㄱㅁㄱㅅㅅㅂㄱㅁㅁㅂㅅㅅㅅㅂㅅㅁㅁㄴㄷㅅㅅㄴㄱㅂㄴㄱㄷㄱㄷㄷㄹㅈㅈㄴㄷㄱㄴㄴㄹㅈㄷㄴㅅㄷㄹㅂㄷㅈㄹㅅㄷㅅㄹㄴㄱㄴㄹㅂㄹㄹㄹㄴㄷㅁㅁㅂㅈㅅㄴㄴㅅㅁㄹㅂㅈㄷㄷㄴㅈㅂㄱㅁㅁㅅㅅㅈㄱㅁㄱㄱㅅㅅㅅㄴㄹㅁㅁㄴㅅㅅㅅㄹㅂㅁㄱㄹㅅㅂㅅㄹㄷㅂㄱㅅㄷㅅㄷㄱㄱㄴㅁㅂㄹㅈㄴㄴㅁㅁㅁㅂㄹㅅㄴㄴㄷㅂㄷㅂㅈㄴㄹㄴㅈㅂㄱㅁㄱㅅㅅㄹㄱㅂㄱㅅㅅㅅㅅㄹㅅㅁㅁㄷㅅㅂㅅㄹㄴㅂㅁㅈㄷㄱㄷㅅㄷㅈㄱㅅㄷㄷㄴㄹㄹㅈㄹㄱㅅㄷㄴㄴㄹㅈㅁㄹㄷㅅㄹㅈㄷㅈㄴㅁㄷㅅㄴㄴㄱㄴㅁㅂㄹㅈㄴㄴㅁㅁㅁㅂㄹㅅㄴㄴㄱㅂㄹㅂㅈㅈㄷㄴㅈㅂㅁㅂㅈㄴㄷㄴㅈㅂㅁㅂㄹㄱㄷㄹㄱㅁㄱㅁㄱㅂㅅㄴㅅㅂㄱㅅㅅㅂㅅㅈㅁㅂㄱㅈㄷㅅㅅㅈㄴㅂㄱㄴㄷㅅㅅㄴㄴㅁㅁㄹㅅㅂㅅㄹㄴㅂㅁㅈㄷㄱㄷㅅㄷㅈㅂㄴㄷㄷㄴㄴㄹㅈㄷㄹㅅㄱㄹㄴㄱㄴㅂㅂㅈㅁㄴㄹㅂㅁㄷㅂㅈㄴㄹㄴㄱㅂㅂㅂㄹㅈㄴㄴㄷㅁㄱㅁㅁㅅㅅㄹㅂㅁㄱㄹㄷㅅㅅㅈㅂㅁㅁㅂㄷㄱㄷㄱㄹㅈㄱㅁㅅㄷㄴㄴㄹㅈㄴㅈㄷㅁㄴㅂㄱㅅㅈㅅㄷㅂㅅㅂㅁㅂㅂㅈㄷㅅㅅㄴㄱㅂㅁㄹㄷㄴㅁㅈㅂㅂㅁㅂㄹㄴㄱㄴㄹㅂㅂㅂㄹㅂㄴㄴㄹㅁㄷㄱㅈㄹㄹㅈㄷㅈㅁㅂㄷㅁㄹㄹㄹㅈㄴㄹㄷㄷㄴㄴㄹㅈㅂㄹㄷㅁㄴㄴㄱㄴㄹㅂㄹㅂㄷㄴㄷㅂㄹㅂㅈㄴㄴㄴㄱㅂㄱㅁㄱㅅㅅㄴㅅㅁㄴㄱㄷㅅㅅㅈㅂㅁㅂㅂㄷㅅㅅㅈㅂㅁㄱㄷㄷㄱㄷㄱㄹㅈㅅㄹㄷㅁㄱㄴㄹㅈㅅㄷㄷㄷㄹㄴㄹㅈㅁㄱㄷㅅㄴㄴㄱㄴㄷㅂㄹㄱㄹㄹㄱㅁㅁㅂㅈㅅㄴㄴㅅㅂㅁㅂㅈㅅㄴㄴㅅㅁㄱㅁㄱㅂㅅㄴㅅㅂㄱㅅㅅㅅㅅㅂㅅㅁㅁㄴㅅㅂㅅㄹㄴㅂㅁㅈㄷㄱㄷㅁㄷㅈㅈㅅㄷㄱㄷㅈㄷㅈㄹㄷㅅㄱㄹㄹㄹㅈㅅㄹㄷㅁㄱㄴㄱㄴㅂㅂㅈㄷㄴㄴㅅㅁㄷㅂㅈㄴㄹㄴㄱㅂㅁㅂㄱㄱㄷㅅㄷㅈㄷㄴㅅㄷㄷㅈㄷㅈㄱㅁㅅㄷㄷㄴㄹㅈㅂㄹㄷㄷㄱㄴㄱㄴㅁㅂㅈㄷㄹㄴㅈㅁㄷㅂㅈㄴㄹㄴㄱㅂㄹㅂㅈㅈㄱㄴㄴㅁㄹㅂㅈㄱㄷㄴㅈㅁㄱㅁㅁㅂㅅㄴㅁㅂㅁㄹㅅㅅㅅㄴㅈㅁㄱㄹㅅㅅㅅㄹㅂㅁㄱㄹㄷㅂㅅㅂㅁㅂㅁㄴㄷㄱㄷㄷㄹㅈㅂㄷㄷㅁㄴㅈㄷㅈㄴㅂㄷㄱㄹㄴㄹㄴㄱㅁㄱㅅㅅㅂㅈㅁㄱㄷㄷㅅㅅㄴㅈㅁㄱㅁㄷㅅㅅㄹㅅㅁㄱㄱㄷㄱㄷㅁㄷㅈㅅㅅㄷㅅㄱㅈㄷㅈㅅㅁㄷㅅㄷㄴㄹㅈㅈㄷㄷㄱㄴㄴㄱㄴㄹㅂㄹㄷㄴㄴㅁㅂㄹㅂㅈㄷㄷㄴㅂㅂㄹㅂㄹㅂㄱㄴㅂㅁㄱㅁㄱㅅㅅㄹㅁㅂㅂㄱㄷㅅㅅㅂㅈㅁㅁㄱㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㄱㄹㅈㅂㄹㄷㅁㄴㅈㄷㅈㅁㅂㄷㄷㄹㅈㄷㅈㅂㅁㄷㅅㄹㄴㄱㄴㅁㅂㅈㅁㄴㄴㄴㅁㅁㅂㄹㅁㄱㄴㅅㅁㅂㅂㅈㄷㄴㄴㅅㅁㄷㅂㄹㄴㄹㄴㄹㅁㄱㅁㅁㅅㅅㄹㅂㅁㄱㄹㄷㅅㅅㅈㅂㅁㅁㅂㄷㅅㄷㄱㄱㄴㅁㅂㅈㄷㄴㄴㄷㅁㅁㅂㄹㅅㄴㄴㅈㅂㄹㅂㅈㄱㄷㄴㅈㅁㄹㅂㄹㅂㄱㄴㅂㅁㄱㅁㄱㅂㅅㄹㅂㅂㅂㅂㅅㅂㅅㅈㄹㅂㅁㅈㄷㅅㅅㅈㄱㅁㅂㄹㅅㅅㅅㄹㅅㅁㅁㄹㄷㅅㅅㄹㅈㅁㄱㄹㄷㄱㄷㅁㄷㅈㅈㅅㄷㄱㄷㅈㄷㅈㄹㄷㅅㄱㄹㄹㄹㅈㅂㄷㄷㅅㄴㄴㄱㄴㅂㅂㄹㄹㄴㄹㄴㅂㅁㅂㅈㄴㄱㄹㄱㅁㅁㅂㅈㅅㄴㄴㄴㅁㄱㅁㄱㅂㅅㄴㅅㅂㄱㅅㅅㅅㅅㄹㅂㅁㄱㄹㄷㅂㅅㅈㅁㅂㄱㅁㄷㄱㄷㅅㄷㅈㄱㅅㄷㄹㄴㄴㄹㅈㅁㄹㄷㅅㄹㅈㄷㅈㄴㅁㄷㅅㄴㅈㄷㅈㄷㄴㄷㄷㄴㄴㄱㄴㅂㅂㅈㄷㄴㄹㄹㅂㄷㅂㅈㄷㄹㄴㄹㅂㅁㅂㄹㄱㄷㄹㄱㅁㅁㅂㅈㅅㄴㄴㅅㅂㄱㅁㄱㅅㅅㄴㄴㅁㄱㅈㄷㅂㅅㅈㅁㅂㅁㄱㅅㅅㅅㅈㄹㅁㄴㄴㅅㅅㅅㄹㅅㅁㅁㄷㄷㅅㅅㄹㅅㅁㄱㄱㄷㄱㄷㄱㄹㅈㅂㄹㄷㅁㄹㅈㄷㅈㅂㅁㄷㅁㄴㅂㄷㅈㄹㅅㅅㄷㄹㄴㄹㅈㄱㄹㅅㄱㄱㄴㄹㅈㅈㄷㄷㄱㄴㄴㄱㄴㅁㅂㅈㅅㄴㄴㅂㅂㄹㅂㄹㄱㄹㄴㅂㅁㅁㅂㅈㄹㄷㄴㄱㅁㅂㅂㅈㄷㄴㄴㄷㅂㅁㅂㄹㅅㄴㄴㅈㅂㄹㅂㅈㄱㄷㄴㅈㅁㅁㅂㅈㅅㄱㄴㄷㅂㄱㅁㄱㅅㅅㅂㅅㅁㄱㅅㅅㅂㅅㅂㄴㅂㅁㅂㅅㅂㅅㅈㅁㅁㅁㅁㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㄱㄹㅈㄷㄹㄷㄱㄹㅈㄷㅈㅅㅁㄷㅅㄷㅈㄷㅈㄹㄷㄷㄷㄷㄴㄹㅈㅂㄹㄷㅁㄴㄴㄱㄴㅁㅂㄹㅈㄴㄴㅁㅁㅁㅂㄹㄹㄱㄴㅁㅁㅁㅂㅈㅅㄴㄴㅅㅁㄱㅁㄱㅅㅅㄹㅂㅁㄱㄴㄷㅅㅅㄴㄱㅂㅁㄱㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㄱㄹㅈㅅㄹㄷㄱㄴㄴㄹㅈㅁㄹㄷㄱㄷㄴㄹㅈㄴㄹㄷㄱㄱㄴㄱㄴㅂㅂㄹㄹㄴㄹㄷㅁㄹㅂㅈㄴㄹㄹㅂㅂㅁㅂㅈㅅㄴㄴㄴㅁㄱㅁㄱㅅㅅㄴㅅㅁㄴㄱㄷㅅㅅㅈㅅㅁㄱㄷㅅㅅㅅㅂㅈㅁㄱㄴㄷㄱㄷㄷㄹㅈㄴㄹㅅㄷㄴㅈㄷㅈㄹㅅㄷㄷㄹㄹㄹㅈㅂㄷㄷㄱㄷㄴㄱㄴㄷㅂㄹㄴㄹㅈㄱㅁㅁㅂㅈㅅㄴㄴㄴㅁㄱㅁㅁㅂㅅㅈㄷㅁㅁㅁㄷㅅㅅㅈㄴㅂㄱㄷㅅㅅㅅㄹㅂㅁㄱㄹㅅㅂㅅㄹㄷㅂㅁㅅㄷㅅㅅㄴㄴㅁㅁㄹㄷㄱㄷㄷㅁㄴㄴㅈㄱㄷㄹㄱㅅㄴㄹㅂㅈㄷㄱㄴㄴㅁㄱㅁㅁㄹㄹㄱㄹㅈㄹㄹㄷㄷㄴㄴㄱㄴㄴㅅㄱㄴㄹㄱㄹㅈㅂㄹㄷㅅㄹㄴㄹㅈㅈㄷㄷㄱㄴㄴㄱㄴㅁㅂㄹㄱㄷㄴㅈㅁㅁㅂㄹㄱㄷㄹㅂㅁㄹㅂㄹㄱㄴㄴㅅㅁㄷㅂㅈㄴㄹㄴㄱㅂㄱㅁㄱㅁㄹㄱㄹㅈㄱㅅㄷㅁㄷㄴㄹㅈㅈㄷㄷㄱㄴㄴㄱㄴㄷㅂㅈㄱㄹㄴㅅㅂㅁㅂㅈㄴㄹㄴㅁㅁㄱㅁㄱㅂㅅㄴㅁㅂㅁㄹㄷㅅㅅㄴㄱㅂㅂㄷㅅㅂㅅㄴㅁㅁㅁㄹㄷㄱㄷㄷㄹㅈㅈㄷㄷㅅㄱㅈㄷㅈㄷㅅㅅㄷㄴㄴㄹㅈㅂㄹㄷㄷㄱㄴㄱㄴㅁㅂㅈㅅㄴㄴㅂㅂㅁㅂㄹㄱㄷㄴㅈㅁㄱㅁㄱㅂㅅㄹㅂㅂㅂㅂㅅㅅㅅㅂㅅㅁㅁㄴㄷㅅㅅㄹㅈㅁㄱㄹㄷㄱㄷㄱㄹㅈㅂㄹㄷㅁㄴㅂㄷㅈㄷㅅㄷㄱㄹㄴㄹㅈㅂㄹㄷㄷㄱㄴㄱㄴㄷㅂㅈㄱㄹㄴㅁㅂㅁㅂㅈㄴㄹㄴㅁㅁㄱㅁㄱㅂㅅㄹㅂㅂㅂㅂㅅㅂㅅㅈㄹㅂㅁㅈㅅㅅㅅㄴㄷㅁㅁㅂㅅㅅㅅㄹㅁㅁㅁㄹㄷㅅㅅㅈㅂㅁㄱㄷㄷㄱㄷㄱㄹㅈㅂㄹㄷㅁㄴㄹㄹㅈㅂㄷㄷㅁㄴㄴㄹㅈㅈㄷㄷㅅㄷㄴㄱㄴㄷㅂㄹㄱㄹㄴㅈㅁㅁㅂㄹㄱㄷㄹㅂㅁㅂㅂㅈㄷㄴㄴㅈㅁㄹㅂㅈㅂㄱㄴㄴㅂㅅㅂㄱ (ㄴ ㅂㅂㄱㄷㄱ ㄱㅇㄱㅎㄷ)ㅎㄴ (ㄱ ㄴ ㄱㅇㄱㅎㄷ)ㅎㄴ ㅎㅎㄴ')
        _test('(ㅂ ㅂ ㅂㅎㄷ) ㅁㅂㄹㅅㄴㄴㄱㅂㄷㅂㅈㄷㄹㄴㄹㅂㅂㅂㅈㄷㄴㄴㅈㅁㄱㅁㄱㅅㅅㅈㅂㅁㅂㅂㄷㅅㅅㅂㄱㅁㅁㅂㄷㅅㅅㄹㅅㅁㄱㄱㄷㄱㄷㄱㄹㅈㄱㅁㄷㄷㄱㄹㄹㅈㅅㄱㅅㄷㄹㄴㄹㅈㅈㄷㄷㄱㄴㄴㄱㄴㄹㅂㅈㅁㄹㅈㅅㅁㄹㅂㄹㄴㄱㄴㅅㅁㄹㅂㄹㅂㄱㄴㅂㅁㄱㅁㄱㅅㅅㅂㅅㅁㄱㅅㅅㅂㅅㅂㄴㅂㅁㅂㄷㄱㄷㅅㄷㅈㅁㄴㄷㄱㄱㄹㄹㅈㅂㄷㄷㅅㄴㅂㄷㅈㅂㅅㅅㅅㄷㅈㄷㅈㅈㅂㄷㅅㄹㄴㄹㅈㅂㄹㄷㄱㄱㄴㄱㄴㄹㅅㄱㄴㅁㅈㅂㅂㄴㅅㄱㅅㅅㅂㅅㅁㅁㅅㅅㅂㅅㅈㄹㅁㄴㄹㄷㅅㅅㄴㅈㅁㅁㅈㅅㅂㅅㄹㄱㅂㅁㄹㄷㄱㄷㅁㄷㅈㄴㅅㄷㄷㄹㅈㄷㅈㅅㅁㅅㅅㄹㅈㄷㅈㄱㄷㄷㅅㄴㄴㄱㄴㄹㅂㄹㅅㄱㄴㄱㅁㅂㅂㅈㄷㄴㄴㅈㅁㄹㅂㅈㅈㄷㄴㅈㅂㄷㅂㅈㄷㄹㄹㄹㅂㅁㅂㄹㅈㄴㄴㄴㅁㅁㅂㅈㅂㄱㄴㅈㅁㅁㅂㄹㄱㄷㄹㅂㅁㄹㅂㄹㄹㄹㄴㄱㅁㅁㅂㅈㅅㄴㄴㅅㅁㄱㅁㅁㅂㅅㅂㅁㅂㅂㄷㅅㅅㅅㅂㄴㅁㅂㅅㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㅅㄷㅈㅅㅅㄷㅁㄱㄴㄹㅈㅂㄹㄷㅁㄴㄴㄹㅈㅈㄷㄷㄱㄴㄴㄱㄴㅂㅂㅈㄷㄴㄹㄹㅂㄷㅂㅈㄱㄹㄴㅁㅂㅂㅂㅈㄷㄴㄴㅈㅁㄱㅁㄱㄷㄹㅁㄱㅅㅈㅅㅅㄱㄹㄷㅅㄴㄹㅂㅈㅈㄷㄴㅈㅂㅁㅂㅈㄴㄷㄴㅈㅂㅁㅂㅈㅅㄴㄴㅂㅂㄹㅂㅈㄷㄱㄴㅁㅁㅁㅂㅈㅅㄴㄴㄴㅁㄱㅁㄱㅂㅅㅈㅁㅂㅁㄱㄷㅅㅅㅂㄷㅁㄴㅈㅅㅅㅅㄹㅂㅁㄱㄹㄷㅂㅅㅈㅁㅂㄱㅁㄷㅅㄷㄱㄱㄴㅁㅂㅈㄱㄷㄴㅁㅂㄷㅂㅈㄷㄹㄹㄹㅂㅁㅂㅈㅅㄴㄴㅅㅁㄱㅁㅁㅂㅅㅈㄹㅂㅁㅈㄷㅅㅅㅈㄱㅂㅁㅈㄷㅂㅅㄴㅁㅂㅁㄹㅅㅅㅅㄴㅅㅁㄴㄱㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㄷㄹㅈㅈㄴㅅㅁㄱㄹㄹㅈㄴㄹㄷㄷㄴㄴㄹㅈㄱㅁㅅㄱㄱㄴㄱㄴㅂㅂㄹㄹㄱㄹㅂㅂㅁㅂㅈㅅㄴㄴㅈㅂㅁㅂㅈㅅㄴㄴㅅㅁㄱㅁㄱㅅㅅㅂㄱㅁㅁㅂㅅㅂㅅㅂㄷㅂㅂㄱㄷㅅㅅㅈㅂㅁㄱㄷㄷㄱㄷㄱㄹㅈㅅㄹㅅㄷㄱㅂㄷㅈㄱㅅㅅㄱㄱㄹㄹㅈㅂㄷㄷㅁㄴㄴㄹㅈㅈㄷㄷㅅㄷㄴㄱㄴㅁㅂㄹㄱㄷㄹㅂㅁㅁㅂㅈㅅㄴㄴㅅㅁㄷㄱㅈㄹㄹㄴㄹㅈㅂㄹㄷㅁㄹㅈㄷㅈㅈㄴㄷㄷㄱㄴㄹㅈㄴㄹㄷㄱㄱㄴㄱㄴㄹㅂㅈㅈㄱㄹㅅㅁㅂㅂㅈㅈㄱㄴㄹㅂㅁㅂㅈㄷㄴㄴㄱㅂㄹㅂㅈㄱㄷㄴㅈㅁㅁㅂㅈㅅㄱㄴㄷㅂㄱㅁㅁㅂㅅㅈㄹㅂㅁㅈㄷㅅㅅㄹㄱㅂㄴㅅㄷㅅㅅㄹㅈㅁㄱㄹㄷㄱㄷㅅㄷㅈㄹㄴㄷㅁㄷㅂㄷㅈㄷㅅㄷㄱㄹㄴㄹㅈㅂㄹㄷㄷㄱㄴㄱㄴㄷㅂㅈㄴㄹㄹㅂㅂㄷㅂㅈㄴㄹㄴㄱㅂㅂㅂㄹㅈㄴㄴㄷㅁㄱㅁㅁㅅㅅㄹㅂㅁㄱㄹㄷㅂㅅㅈㅁㅂㄱㅁㄷㅅㄷㄱㄱㄴㄹㅂㄹㅂㄷㄴㄷㅂㄹㅂㅈㄴㄴㄴㄱㅂㄱㅁㄱㅅㅅㅂㄱㅁㅁㅂㅅㅅㅅㅂㅅㅁㅁㄴㄷㅅㅅㄴㄱㅂㄴㄱㄷㄱㄷㄷㄹㅈㅈㄴㄷㄱㄴㄴㄹㅈㄷㄴㅅㄷㄹㅂㄷㅈㄹㅅㄷㅅㄹㄴㄱㄴㄹㅂㄹㄹㄹㄴㄷㅁㅁㅂㅈㅅㄴㄴㅅㅁㄹㅂㅈㄷㄷㄴㅈㅂㄱㅁㅁㅅㅅㅈㄱㅁㄱㄱㅅㅅㅅㄴㄹㅁㅁㄴㅅㅅㅅㄹㅂㅁㄱㄹㅅㅂㅅㄹㄷㅂㄱㅅㄷㅅㄷㄱㄱㄴㅁㅂㄹㅈㄴㄴㅁㅁㅁㅂㄹㅅㄴㄴㄷㅂㄷㅂㅈㄴㄹㄴㅈㅂㄱㅁㄱㅅㅅㄹㄱㅂㄱㅅㅅㅅㅅㄹㅅㅁㅁㄷㅅㅂㅅㄹㄴㅂㅁㅈㄷㄱㄷㅅㄷㅈㄱㅅㄷㄷㄴㄹㄹㅈㄹㄱㅅㄷㄴㄴㄹㅈㅁㄹㄷㅅㄹㅈㄷㅈㄴㅁㄷㅅㄴㄴㄱㄴㅁㅂㄹㅈㄴㄴㅁㅁㅁㅂㄹㅅㄴㄴㄱㅂㄹㅂㅈㅈㄷㄴㅈㅂㅁㅂㅈㄴㄷㄴㅈㅂㅁㅂㄹㄱㄷㄹㄱㅁㄱㅁㄱㅂㅅㄴㅅㅂㄱㅅㅅㅂㅅㅈㅁㅂㄱㅈㄷㅅㅅㅈㄴㅂㄱㄴㄷㅅㅅㄴㄴㅁㅁㄹㅅㅂㅅㄹㄴㅂㅁㅈㄷㄱㄷㅅㄷㅈㅂㄴㄷㄷㄴㄴㄹㅈㄷㄹㅅㄱㄹㄴㄱㄴㅂㅂㅈㅁㄴㄹㅂㅁㄷㅂㅈㄴㄹㄴㄱㅂㅂㅂㄹㅈㄴㄴㄷㅁㄱㅁㅁㅅㅅㄹㅂㅁㄱㄹㄷㅅㅅㅈㅂㅁㅁㅂㄷㄱㄷㄱㄹㅈㄱㅁㅅㄷㄴㄴㄹㅈㄴㅈㄷㅁㄴㅂㄱㅅㅈㅅㄷㅂㅅㅂㅁㅂㅂㅈㄷㅅㅅㄴㄱㅂㅁㄹㄷㄴㅁㅈㅂㅂㅁㅂㄹㄴㄱㄴㄹㅂㅂㅂㄹㅂㄴㄴㄹㅁㄷㄱㅈㄹㄹㅈㄷㅈㅁㅂㄷㅁㄹㄹㄹㅈㄴㄹㄷㄷㄴㄴㄹㅈㅂㄹㄷㅁㄴㄴㄱㄴㄹㅂㄹㅂㄷㄴㄷㅂㄹㅂㅈㄴㄴㄴㄱㅂㄱㅁㄱㅅㅅㄴㅅㅁㄴㄱㄷㅅㅅㅈㅂㅁㅂㅂㄷㅅㅅㅈㅂㅁㄱㄷㄷㄱㄷㄱㄹㅈㅅㄹㄷㅁㄱㄴㄹㅈㅅㄷㄷㄷㄹㄴㄹㅈㅁㄱㄷㅅㄴㄴㄱㄴㄷㅂㄹㄱㄹㄹㄱㅁㅁㅂㅈㅅㄴㄴㅅㅂㅁㅂㅈㅅㄴㄴㅅㅁㄱㅁㄱㅂㅅㄴㅅㅂㄱㅅㅅㅅㅅㅂㅅㅁㅁㄴㅅㅂㅅㄹㄴㅂㅁㅈㄷㄱㄷㅁㄷㅈㅈㅅㄷㄱㄷㅈㄷㅈㄹㄷㅅㄱㄹㄹㄹㅈㅅㄹㄷㅁㄱㄴㄱㄴㅂㅂㅈㄷㄴㄴㅅㅁㄷㅂㅈㄴㄹㄴㄱㅂㅁㅂㄱㄱㄷㅅㄷㅈㄷㄴㅅㄷㄷㅈㄷㅈㄱㅁㅅㄷㄷㄴㄹㅈㅂㄹㄷㄷㄱㄴㄱㄴㅁㅂㅈㄷㄹㄴㅈㅁㄷㅂㅈㄴㄹㄴㄱㅂㄹㅂㅈㅈㄱㄴㄴㅁㄹㅂㅈㄱㄷㄴㅈㅁㄱㅁㅁㅂㅅㄴㅁㅂㅁㄹㅅㅅㅅㄴㅈㅁㄱㄹㅅㅅㅅㄹㅂㅁㄱㄹㄷㅂㅅㅂㅁㅂㅁㄴㄷㄱㄷㄷㄹㅈㅂㄷㄷㅁㄴㅈㄷㅈㄴㅂㄷㄱㄹㄴㄹㄴㄱㅁㄱㅅㅅㅂㅈㅁㄱㄷㄷㅅㅅㄴㅈㅁㄱㅁㄷㅅㅅㄹㅅㅁㄱㄱㄷㄱㄷㅁㄷㅈㅅㅅㄷㅅㄱㅈㄷㅈㅅㅁㄷㅅㄷㄴㄹㅈㅈㄷㄷㄱㄴㄴㄱㄴㄹㅂㄹㄷㄴㄴㅁㅂㄹㅂㅈㄷㄷㄴㅂㅂㄹㅂㄹㅂㄱㄴㅂㅁㄱㅁㄱㅅㅅㄹㅁㅂㅂㄱㄷㅅㅅㅂㅈㅁㅁㄱㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㄱㄹㅈㅂㄹㄷㅁㄴㅈㄷㅈㅁㅂㄷㄷㄹㅈㄷㅈㅂㅁㄷㅅㄹㄴㄱㄴㅁㅂㅈㅁㄴㄴㄴㅁㅁㅂㄹㅁㄱㄴㅅㅁㅂㅂㅈㄷㄴㄴㅅㅁㄷㅂㄹㄴㄹㄴㄹㅁㄱㅁㅁㅅㅅㄹㅂㅁㄱㄹㄷㅅㅅㅈㅂㅁㅁㅂㄷㅅㄷㄱㄱㄴㅁㅂㅈㄷㄴㄴㄷㅁㅁㅂㄹㅅㄴㄴㅈㅂㄹㅂㅈㄱㄷㄴㅈㅁㄹㅂㄹㅂㄱㄴㅂㅁㄱㅁㄱㅂㅅㄹㅂㅂㅂㅂㅅㅂㅅㅈㄹㅂㅁㅈㄷㅅㅅㅈㄱㅁㅂㄹㅅㅅㅅㄹㅅㅁㅁㄹㄷㅅㅅㄹㅈㅁㄱㄹㄷㄱㄷㅁㄷㅈㅈㅅㄷㄱㄷㅈㄷㅈㄹㄷㅅㄱㄹㄹㄹㅈㅂㄷㄷㅅㄴㄴㄱㄴㅂㅂㄹㄹㄴㄹㄴㅂㅁㅂㅈㄴㄱㄹㄱㅁㅁㅂㅈㅅㄴㄴㄴㅁㄱㅁㄱㅂㅅㄴㅅㅂㄱㅅㅅㅅㅅㄹㅂㅁㄱㄹㄷㅂㅅㅈㅁㅂㄱㅁㄷㄱㄷㅅㄷㅈㄱㅅㄷㄹㄴㄴㄹㅈㅁㄹㄷㅅㄹㅈㄷㅈㄴㅁㄷㅅㄴㅈㄷㅈㄷㄴㄷㄷㄴㄴㄱㄴㅂㅂㅈㄷㄴㄹㄹㅂㄷㅂㅈㄷㄹㄴㄹㅂㅁㅂㄹㄱㄷㄹㄱㅁㅁㅂㅈㅅㄴㄴㅅㅂㄱㅁㄱㅅㅅㄴㄴㅁㄱㅈㄷㅂㅅㅈㅁㅂㅁㄱㅅㅅㅅㅈㄹㅁㄴㄴㅅㅅㅅㄹㅅㅁㅁㄷㄷㅅㅅㄹㅅㅁㄱㄱㄷㄱㄷㄱㄹㅈㅂㄹㄷㅁㄹㅈㄷㅈㅂㅁㄷㅁㄴㅂㄷㅈㄹㅅㅅㄷㄹㄴㄹㅈㄱㄹㅅㄱㄱㄴㄹㅈㅈㄷㄷㄱㄴㄴㄱㄴㅁㅂㅈㅅㄴㄴㅂㅂㄹㅂㄹㄱㄹㄴㅂㅁㅁㅂㅈㄹㄷㄴㄱㅁㅂㅂㅈㄷㄴㄴㄷㅂㅁㅂㄹㅅㄴㄴㅈㅂㄹㅂㅈㄱㄷㄴㅈㅁㅁㅂㅈㅅㄱㄴㄷㅂㄱㅁㄱㅅㅅㅂㅅㅁㄱㅅㅅㅂㅅㅂㄴㅂㅁㅂㅅㅂㅅㅈㅁㅁㅁㅁㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㄱㄹㅈㄷㄹㄷㄱㄹㅈㄷㅈㅅㅁㄷㅅㄷㅈㄷㅈㄹㄷㄷㄷㄷㄴㄹㅈㅂㄹㄷㅁㄴㄴㄱㄴㅁㅂㄹㅈㄴㄴㅁㅁㅁㅂㄹㄹㄱㄴㅁㅁㅁㅂㅈㅅㄴㄴㅅㅁㄱㅁㄱㅅㅅㄹㅂㅁㄱㄴㄷㅅㅅㄴㄱㅂㅁㄱㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㄱㄹㅈㅅㄹㄷㄱㄴㄴㄹㅈㅁㄹㄷㄱㄷㄴㄹㅈㄴㄹㄷㄱㄱㄴㄱㄴㅂㅂㄹㄹㄴㄹㄷㅁㄹㅂㅈㄴㄹㄹㅂㅂㅁㅂㅈㅅㄴㄴㄴㅁㄱㅁㄱㅅㅅㄴㅅㅁㄴㄱㄷㅅㅅㅈㅅㅁㄱㄷㅅㅅㅅㅂㅈㅁㄱㄴㄷㄱㄷㄷㄹㅈㄴㄹㅅㄷㄴㅈㄷㅈㄹㅅㄷㄷㄹㄹㄹㅈㅂㄷㄷㄱㄷㄴㄱㄴㄷㅂㄹㄴㄹㅈㄱㅁㅁㅂㅈㅅㄴㄴㄴㅁㄱㅁㅁㅂㅅㅈㄷㅁㅁㅁㄷㅅㅅㅈㄴㅂㄱㄷㅅㅅㅅㄹㅂㅁㄱㄹㅅㅂㅅㄹㄷㅂㅁㅅㄷㅅㅅㄴㄴㅁㅁㄹㄷㄱㄷㄷㅁㄴㄴㅈㄱㄷㄹㄱㅅㄴㄹㅂㅈㄷㄱㄴㄴㅁㄱㅁㅁㄹㄹㄱㄹㅈㄹㄹㄷㄷㄴㄴㄱㄴㄴㅅㄱㄴㄹㄱㄹㅈㅂㄹㄷㅅㄹㄴㄹㅈㅈㄷㄷㄱㄴㄴㄱㄴㅁㅂㄹㄱㄷㄴㅈㅁㅁㅂㄹㄱㄷㄹㅂㅁㄹㅂㄹㄱㄴㄴㅅㅁㄷㅂㅈㄴㄹㄴㄱㅂㄱㅁㄱㅁㄹㄱㄹㅈㄱㅅㄷㅁㄷㄴㄹㅈㅈㄷㄷㄱㄴㄴㄱㄴㄷㅂㅈㄱㄹㄴㅅㅂㅁㅂㅈㄴㄹㄴㅁㅁㄱㅁㄱㅂㅅㄴㅁㅂㅁㄹㄷㅅㅅㄴㄱㅂㅂㄷㅅㅂㅅㄴㅁㅁㅁㄹㄷㄱㄷㄷㄹㅈㅈㄷㄷㅅㄱㅈㄷㅈㄷㅅㅅㄷㄴㄴㄹㅈㅂㄹㄷㄷㄱㄴㄱㄴㅁㅂㅈㅅㄴㄴㅂㅂㅁㅂㄹㄱㄷㄴㅈㅁㄱㅁㄱㅂㅅㄹㅂㅂㅂㅂㅅㅅㅅㅂㅅㅁㅁㄴㄷㅅㅅㄹㅈㅁㄱㄹㄷㄱㄷㄱㄹㅈㅂㄹㄷㅁㄴㅂㄷㅈㄷㅅㄷㄱㄹㄴㄹㅈㅂㄹㄷㄷㄱㄴㄱㄴㄷㅂㅈㄱㄹㄴㅁㅂㅁㅂㅈㄴㄹㄴㅁㅁㄱㅁㄱㅂㅅㄹㅂㅂㅂㅂㅅㅂㅅㅈㄹㅂㅁㅈㅅㅅㅅㄴㄷㅁㅁㅂㅅㅅㅅㄹㅁㅁㅁㄹㄷㅅㅅㅈㅂㅁㄱㄷㄷㄱㄷㄱㄹㅈㅂㄹㄷㅁㄴㄹㄹㅈㅂㄷㄷㅁㄴㄴㄹㅈㅈㄷㄷㅅㄷㄴㄱㄴㄷㅂㄹㄱㄹㄴㅈㅁㅁㅂㄹㄱㄷㄹㅂㅁㅂㅂㅈㄷㄴㄴㅈㅁㄹㅂㅈㅂㄱㄴㄴㅂㅅㅂㄱ (ㄴ ㅂㅂㄱㄷㄱ ㄱㅇㄱㅎㄷ)ㅎㄴ (ㄱ ㄴ ㄱㅇㄱㅎㄷ)ㅎㄴ ㅎㅎㄴ', "'유구한 역사와 전통에 빛나는 우리 대한국민은 3·1운동으로 건립된 대한민국임시정부의 법통과 불의에 항거한 4·19민주이념을 계승하고, 조국의 민주개혁과 평화적 통일의 사명에 입각하여 정의·인도와 동포애로써 민족의 단결을 공고히 하고, 모든 사회적 폐습과 불의를 타파하며, 자율과 조화를 바탕으로 자유민주적 기본질서를 더욱 확고히 하여 정치·경제·사회·문화의 모든 영역에 있어서 각인의 기회를 균등히 하고, 능력을 최고도로 발휘하게 하며, 자유와 권리에 따르는 책임과 의무를 완수하게 하여, 안으로는 국민생활의 균등한 향상을 기하고 밖으로는 항구적인 세계평화와 인류공영에 이바지함으로써 우리들과 우리들의 자손의 안전과 자유와 행복을 영원히 확보할 것을 다짐하면서 1948년 7월 12일에 제정되고 8차에 걸쳐 개정된 헌법을 이제 국회의 의결을 거쳐 국민투표에 의하여 개정한다.'")
