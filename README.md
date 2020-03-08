# > 평범한 한글 v0.7
함수형 난해한 언어 '평범한 한글'의 명세와 구현체입니다. 평범한 한글 문장으로 보이는 프로그램을 짜보세요!

## ㄱ. 명세
[명세](docs/spec.md) 문서를 참조해주세요.

## ㄴ. 예시

1. 산술 연산 예시

  * `나 과제 다 했다.` = -55

2. 비교 연산 예시

  * `그는 자는 척했다.` = False
  
3. 함수 예시

  * `날마다 날마다 늘어간 기약과 더하던 후회다.` = 322

4. 팩토리얼 예시

  * 0!=1 계산:

        '......까? 누, 구에게......'
        그가 여길 나갈 때,
        "......형도 결국은......하네......"
        ...갑갑하다. 그에게 또 잡힐듯하다.
        "......형? 혼나......"
  * 4!=24 계산:

        '......면? 누, 구에게......'
        그가 여길 나갈 때,
        "......형도 결국은......하네......"
        ...갑갑하다. 그에게 또 잡힐듯하다.
        "......형? 혼나......"

5. 피보나치 예시

  * Fib(0)=1 계산:

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

  * Fib(3)=3 계산:

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

6. 배열 비슷한 무언가(?)

  * `ㄱ [ㄴ, ㄷ, ㄹ] ㄱㅇㄱㅇㄴㅎㅎ ㅎㄹ ㅎㄴ` = 1
  * `ㄴ [ㄴ, ㄷ, ㄹ] ㄱㅇㄱㅇㄴㅎㅎ ㅎㄹ ㅎㄴ` = 2
  
7. 논리 부정(?)

  * `난 지금도 가끔 얘기 해. 누군간 여길 꿈꿨을까, 끝없는 헛된 후회 하나 했던걸까...` = 135
  * `난 지금도 늘 얘기 해. 누군간 여길 꿈꿨을까, 끝없는 헛된 후회 하나 했던걸까...` = 1

8. 문자열 입력을 여러 개 받아 이어붙이는 드나듦. 빈 문자열을 입력받으면 종료.

  * `ㅁㅈㅎㄱ [ㄹㅎㄱ {(ㄱㅇㄴ ㄱㅅㅎㄴ) (ㄱㅇㄴ ㄱㅇㄱ ㄷㅎㄷ ㄴㅇㅎㄴ) (ㄱㅇㄱ ㅈㄷㅎㄴ ㄱ ㄴㅎㄷ) ㅎㄷ ㅎ} ㄱㄹㅎㄷ ㅎ] ㅎㄴ`

9. 실수 입력을 여러 개 받아 더하는 드나듦. 0을 입력받으면 종료.

  * `ㄱ [(ㄹㅎㄱ ㅅㅅ ㄱㅅ ㄴㄱㅎㄷ ㄱㄹㅎㄷ) {(ㄱㅇㄴ ㄱㅅㅎㄴ) (ㄱㅇㄴ ㄱㅇㄱ ㄷㅎㄷ ㄴㅇㅎㄴ) (ㄱㅇㄱ ㄱ ㄴㅎㄷ) ㅎㄷ ㅎ} ㄱㄹㅎㄷ ㅎ] ㅎㄴ`

'조각글' 폴더 아래 예시가 더 많이 있습니다. 이 예시는 '평범한 한글' 구현 또는 명세의 일부는 아닙니다.

10. 입력 받은 문자열을 생성하는 '평범한 한글' 코드 생성

  * `조각글 문자만드는평범코드드립니다 ㅂㅎㄷ`
    - '하늘과 바람과 별과 詩' 입력 ⇒ `'(ㅂ ㅂ ㅂㅎㄷ) ㅂㅂㅈㄷㄴㄴㅅㅁㄹㅂㄹㅂㄱㄴㅅㅁㄷㅂㅈㄴㄹㄴㅈㅂㄱㅁㅁㅂㅅㄴㅁㅂㅁㄷㅅㅂㅅㅂㅈㅁㅁㄴㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㅅㄷㅈㄹㅅㄷㄷㄱㅂㄷㅈㄹㅅㄷㅅㄹㄴㄱㄴㄱㅂㅈㅁㄷㄹㄷㅂㄱ (ㄴ ㅅㄹㄱ ㄱㅇㄱㅎㄷ)ㅎㄴ (ㄱ ㄴ ㄱㅇㄱㅎㄷ)ㅎㄴ ㅎㅎㄴ'` 출력
    - 위 코드 실행 ⇒ `'하늘과 바람과 별과 詩'`

11. 입력 받은 숫자를 '평범한 한글' 식으로 바꾸기

  * `ㄹㅎㄱ ㅈㅅ (조각글 평범숫자 ㅂㅎㄷ) ㅈㄹ ㄴㄱㅎㄹ ㄱㄹㅎㄷ`
    - '19480403' 입력 ⇒ `'ㄹㄷㅂㅈㄹㄷㄷㄴㄴ'` 출력
    - `ㄹㄷㅂㅈㄹㄷㄷㄴㄴ` ⇒ 19480403


## ㄷ. 구현체 목록
* Python 구현체
  * `python -m pbhhg_py.main` ⇒ stdin에서 줄별로 문자열을 읽어 각각을 실행해 결과 출력
  * `python -m pbhhg_py.main [문자열]` ⇒ 주어진 문자열을 실행해서 결과 출력
* JS 구현체:
  * Node.js 환경: `npm install`로 의존성 설치 후 `node pbhhg_js/node.js`
  * 웹 환경:
    - [`pbhhg.html`](https://dragonteros.github.io/unsuspected-hangeul/pbhhg.html) (파일에서 모듈 불러오기는 미구현)
    - [unsuspected-hangeul-ide](https://dragonteros.github.io/unsuspected-hangeul-ide/index.html)
* C++ 구현체: [kmc7468/unsuspected-hangeul-cpp](https://github.com/kmc7468/unsuspected-hangeul-cpp)


## ㄹ. 판올림 기록
* v0.7 (2020.03.08)
  * 복소수가 추가되고 정수가 실수에서 분리되었습니다.
  * 기본 제공 함수로 정수 나눗셈과 나머지 연산이 추가되었습니다. 거듭제곱 연산은 모듈로 거듭제곱을 지원하도록 확장되었습니다.
  * 인수 접근 및 목록, 문자열 등의 인덱싱 행동이 실수를 반올림하는 것에서 정수를 사용하는 것으로 일괄 변경되었습니다.
    - 주의: v0.6의 행동과 호환되지 않습니다.
  * 수학 모듈과 비트 연산 모듈이 추가되었습니다.

* v0.6 (2019.10.03)
  * 옛한글 지원이 추가되었습니다. 이제 모음을 공백으로 취급하지 않습니다.
    - 주의: v0.5의 행동과 호환되지 않습니다.
  * 사전과 바이트열이 추가되었습니다. 이제 객체는 실수, 논릿값, 문자열, 바이트열, 목록, 사전, 함수, 드나듦, 빈값의 아홉 종류입니다.
  * 모듈 불러오기가 추가되었습니다.
    * 실수 및 문자열과 바이트열 사이를 변환하는 모듈 `ㅂ ㅂ`이 기본 제공 모듈로 지원됩니다.
  * 기본 제공 함수 `ㄴ`, `ㄷ`, `ㅈㄷ`, `ㅂㅈ`에 사전과 바이트열 지원을 추가했습니다.
  * 기본 제공 함수 `ㅅㄹ`과 `ㄴㄱ`, `ㅁㅂ`, `ㅂㅂ`이 추가되었습니다.
  * 기본 제공 함수 `ㅁㄷ`, `ㅅㅂ`, `ㅅㄹ`, `ㄱㄹ`가 함수 대신 정수 리터럴, 논릿값 등을 받을 수 있게 변경되었습니다.

* v0.5 (2019.07.28)
  * 목록 및 문자열과 관련 기본 제공 함수가 추가되었습니다. 빈값도 추가되어, 이제 객체는 실수, 논릿값, 목록, 문자열, 함수, 드나듦, 빈값의 일곱 종류입니다.
  * 기본 제공 함수 `ㄱ`과 `ㄷ`가 다른 자료형으로 확장되었습니다.
  * 표준 출력 기본 제공 함수 `ㅈㄹ`이 추가되고, 기본 제공 함수 `ㄱㄹ`의 행동이 변경되었습니다.
  * 기본 제공 함수 `ㄹ`의 행동이 변경되었습니다.
    - 주의: v0.4의 행동과 호환되지 않습니다.

* v0.4 (2019.03.16)
  * IO 모나드를 도입했습니다. 이제 객체는 실수, 논릿값, 함수, 드나듦의 네 종류입니다.
    - 주의: v0.2와 v0.3의 입출력 행동과 호환되지 않습니다.

* v0.3 (2019.03.02)
  * 언어 차원에서 논릿값(Boolean)을 지원합니다. 이제 객체는 실수, 논릿값, 함수의 세 종류입니다.
  * 이제 `ㄹㅎㄱ ㄱㅇㄱ ㄱㅇㄱ ㄷㅎㄷ ㅎ ㅎㄴ`을 실행하면 올바르게 입력을 한번만 받습니다.
    - 알려진 문제(v0.4에서 해결): 입력을 받는 표현식이 문장에 여러 번 나올 때 어느 것을 먼저 실행할지가 정의되어 있지 않았습니다.

* v0.2 (2019.02.26)
  * ㅇ의 행동을 변경했습니다.
    - 인수 위치를 정수 리터럴로만 지정 가능 -> 동적으로 평가해 그 값으로 지정 가능
    - 주의: v0.1의 행동과 호환이 되지 않습니다.
  * 기본 함수 ㄹ, ㅁ을 추가했습니다.
    - ㄹ: 표준 입력
      * 알려진 문제 (v0.3에서 해결): `ㄹㅎㄱ ㄱㅇㄱ ㄱㅇㄱ ㄷㅎㄷ ㅎ ㅎㄴ`을 실행하면 입력을 따로 두 번 받는 문제가 있었습니다.
    - ㅁ: 논리 부정

* v0.1 (2019.02.24)


## ㅁ. 특이사항 및 추가할 기능

* 기본 제공 함수에 다음 기능이 추가될 수 있습니다.
  * 사용자 정의 자료형
* 알려진 버그 (v0.7 현재):
  * 파이썬 구현체에서 사전의 표제로 쓸 때 논릿값 `False`와 정수 `0`을 구분하지 못하는 문제가 있습니다.
  * JS 구현체에서 사전의 표제로 쓸 때 정수 `0`, 실수 `0.0`, 복소수 `0i`를 모두 다르게 취급하는 문제가 있습니다.

## ㅂ. 함께 보기

* [평범한 한글 배우기 by @andrea9292](https://www.notion.so/e75c59b8c4514f87822011f2f08715c6)
