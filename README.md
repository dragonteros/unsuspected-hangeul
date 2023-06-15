# ![로고](docs/logo.gif) 평범한 한글 v0.8

함수형 난해한 언어 '평범한 한글'의 명세와 구현체입니다. 평범한 한글 문장으로 보이는 프로그램을 짜보세요!

## ㄱ. 명세

[명세](docs/spec.md) 문서를 참조해주세요.

## ㄴ. 예시

1. 산술 연산 예시

- `나 과제 다 했다.` = -55

2. 비교 연산 예시

- `그는 자는 척했다.` = False

3. 함수 예시

- `날마다 날마다 늘어간 기약과 더하던 후회다.` = 322

4. 팩토리얼 예시

- 0!=1 계산:

      '......까? 누, 구에게......'
      그가 여길 나갈 때,
      "......형도 결국은......하네......"
      ...갑갑하다. 그에게 또 잡힐듯하다.
      "......형? 혼나......"

- 4!=24 계산:

      '......면? 누, 구에게......'
      그가 여길 나갈 때,
      "......형도 결국은......하네......"
      ...갑갑하다. 그에게 또 잡힐듯하다.
      "......형? 혼나......"

5. 피보나치 예시

- Fib(0)=1 계산:

      그
      누
      구에게
      나가끔격
      동하던
      기억,
      하늘
      과
      용과
      땅과
      통하던
      감각을,

      훗날
      또
      힘든
      길을걷
      다가기
      적같게회동해동행할날

- Fib(3)=3 계산:

      룡:
      누
      구에게
      나가끔격
      동하던
      기억,
      하늘
      과
      용과
      땅과
      통하던
      감각을,

      훗날
      또
      힘든
      길을걷
      다가기
      적같게회동해동행할날

6. 논리 부정(?)

- `난 지금도 가끔 얘기 해. 누군간 여길 꿈꿨을까, 끝없는 헛된 후회 하나 했던걸까...` = 135
- `난 지금도 늘 얘기 해. 누군간 여길 꿈꿨을까, 끝없는 헛된 후회 하나 했던걸까...` = 1

7. 문자열 입력을 여러 개 받아 이어붙이는 드나듦. 빈 문자열을 입력받으면 종료.

- `ㅁㅈㅎㄱ [ㄹㅎㄱ {(ㄱㅇㄴ ㄱㅅㅎㄴ) (ㄱㅇㄴ ㄱㅇㄱ ㄷㅎㄷ ㄴㅇㅎㄴ) (ㄱㅇㄱ ㅈㄷㅎㄴ ㄱ ㄴㅎㄷ) ㅎㄷ ㅎ} ㄱㄹㅎㄷ ㅎ] ㅎㄴ`

8. 실수 입력을 여러 개 받아 더하는 드나듦. 0을 입력받으면 종료.

- `ㄱ [(ㄹㅎㄱ ㅅㅅ ㄱㅅ ㄴㄱㅎㄷ ㄱㄹㅎㄷ) {(ㄱㅇㄴ ㄱㅅㅎㄴ) (ㄱㅇㄴ ㄱㅇㄱ ㄷㅎㄷ ㄴㅇㅎㄴ) (ㄱㅇㄱ ㄱ ㄴㅎㄷ) ㅎㄷ ㅎ} ㄱㄹㅎㄷ ㅎ] ㅎㄴ`

'조각글' 폴더 아래 예시가 더 많이 있습니다. 이 예시는 '평범한 한글' 구현 또는 명세의 일부는 아닙니다.

9. 입력 받은 문자열을 생성하는 '평범한 한글' 코드 생성

- `조각글 문자만드는평범코드드립니다 ㅂㅎㄷ`
  - '하늘과 바람과 별과 詩' 입력 ⇒ `'(ㅂ ㅂ ㅂㅎㄷ) ㅂㅂㅈㄷㄴㄴㅅㅁㄹㅂㄹㅂㄱㄴㅅㅁㄷㅂㅈㄴㄹㄴㅈㅂㄱㅁㅁㅂㅅㄴㅁㅂㅁㄷㅅㅂㅅㅂㅈㅁㅁㄴㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㅅㄷㅈㄹㅅㄷㄷㄱㅂㄷㅈㄹㅅㄷㅅㄹㄴㄱㄴㄱㅂㅈㅁㄷㄹㄷㅂㄱ (ㄴ ㅅㄹㄱ ㄱㅇㄱㅎㄷ)ㅎㄴ (ㄱ ㄴ ㄱㅇㄱㅎㄷ)ㅎㄴ ㅎㅎㄴ'` 출력
  - 위 코드 실행 ⇒ `'하늘과 바람과 별과 詩'`

10. 입력 받은 숫자를 '평범한 한글' 식으로 바꾸기

- `ㄹㅎㄱ ㅈㅅ (조각글 평범숫자 ㅂㅎㄷ) ㅈㄹ ㄴㄱㅎㄹ ㄱㄹㅎㄷ`
  - '19480403' 입력 ⇒ `'ㄹㄷㅂㅈㄹㄷㄷㄴㄴ'` 출력
  - `ㄹㄷㅂㅈㄹㄷㄷㄴㄴ` ⇒ 19480403

11. 빠른정렬(quick sort)

- `ㄱ ㄴ ㄴㄱ ㄷ ㄷㄱ ㄹ ㄹㄱ ㅁㄹㅎㅈ (조각글 빠른정렬 ㅂㅎㄷ)ㅎㄴ` ⇒ `[-3, -2, -1, 0, 1, 2, 3]`

12. [아희](https://aheui.readthedocs.io/ko/latest/index.html) 해석기😎

- `ㄹㅎㄱ (조각글 가나다라마바사즤츼킈틔픠 ㅂㅎㄷ) ㄱㄹㅎㄷ`
  - "./조각글/가나다라마바사즤츼킈틔픠.pbhhg' 입력 ⇒ `2` 출력 후 결과로 `IO(2)`

## ㄷ. 구현체 목록

- Python 구현체
  - 실행하기 위해서는 Python 버전 3.11 이상이 필요합니다.
  - `python -m pbhhg_py.cli` ⇒ 사용자 상호작용형 평범한 한글 해석기
  - `python -m pbhhg_py.cli <파일명> [<인수>...]` ⇒ 평범한 한글로 작성된 파일을 실행해서 결과 출력
  - `python -m pbhhg_py.cli -c <코드> [<인수>...]` ⇒ 평범한 한글 코드를 실행해서 결과 출력
- JS 구현체:
  - Node.js 환경:
    - `node pbhhg_js/cli.js` ⇒ 사용자 상호작용형 평범한 한글 해석기
    - `node pbhhg_js/cli.js <파일명> [<인수>...]` ⇒ 평범한 한글로 작성된 파일을 실행해서 결과 출력
    - `node pbhhg_js/cli.js -c <코드> [<인수>...]` ⇒ 평범한 한글 코드를 실행해서 결과 출력
  - 웹 환경:
    - [`pbhhg.html`](https://dragonteros.github.io/unsuspected-hangeul/pbhhg.html) (파일에서 모듈 불러오기는 미구현)
    - [unsuspected-hangeul-ide](https://dragonteros.github.io/unsuspected-hangeul-ide/index.html)
- C++ 구현체: [kmc7468/unsuspected-hangeul-cpp](https://github.com/kmc7468/unsuspected-hangeul-cpp)

## ㄹ. 판올림 기록

[판올림 기록](CHANGELOG.md) 문서를 참조해주세요.

## ㅁ. 특이사항 및 추가할 기능

- 알려진 버그 (v0.8 현재):
  - 일부 구문에서 느긋한 평가로 인해 예외 처리가 안되는 현상
    - 예: `(ㄱ ㄴㄱ ㅅㅎㄷ) [ㄱㅇㄴㅎ] ㅎㅎㄴ [ㄱㅎ] ㅅㄷㅎㄷ`

## ㅂ. 함께 보기

- [평범한 한글 배우기 by @andrea9292](https://www.notion.so/e75c59b8c4514f87822011f2f08715c6)
- [평범한 한글 vim 개발 환경](https://github.com/dragonteros/unsuspected-hangeul-vim)
