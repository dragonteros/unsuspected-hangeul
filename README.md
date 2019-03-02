﻿# > 평범한 한글 v0.3
함수형 난해한 언어 '평범한 한글'의 명세와 구현체입니다.
'평범한 한글' 프로그램은 한글과 그 외 문자로 이루어진 문자열입니다.
여기서 한글은 다음의 범위에 들어가는 유니코드 문자를 말합니다.

* U+1100-U+1112 (한글 자모 중 초성)
* U+3131-U+314E (호환용 한글 자모 중 자음)
* U+AC00-U+D7AF (한글 음절)
* U+FFA1-U+FFBE (반각 한글 자모 중 자음)

한글 음절은 초성만 추출하여 한글 자모와 같이 취급하며, 한글 자모와 반각 한글 자모는 대응되는 호환용 한글 자모로 변환됩니다. 편의를 위해 언어 명세는 호환용 한글 자모로 기술했습니다. 한편 한글이 아닌 문자는 달리 구분하지 않고 공백과 같이 생각합니다. 따라서 이후의 설명에도 한글이 아닌 문자는 공백이 대표합니다.

## ㄱ. 명세

거센소리와 된소리는 예사소리와 같게 취급하며, 겹자음은 자음 두 개로 분리하여 생각합니다. 이는 작문 시 단어 선택의 폭을 넓히기 위한 선택입니다. 예시로, 다음 단어쌍들은 동일합니다.

* `ㄱㄲㅅㄹ` = `ㄱㄱㅅㄹ`
* `ㅇㅊㅂㅌ` = `ㅇㅈㅂㄷ`
* `ㄳㅎㄴㄷ` = `ㄱㅅㅎㄴㄷ`

간결한 설명을 위해 예사소리 단자음 10개 `ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅎ`만 사용하여 설명하겠습니다. 또한, 모든 `ㅇ`과 `ㅎ`은 그 앞에 공백이 있는 것과 없는 것을 동일하게 봅니다. 따라서 편의를 위해 모든 `ㅇ`과 `ㅎ` 앞에 공백이 있는 것으로 생각합니다.

### 가. 정수 리터럴
`ㅇ`과 `ㅎ`을 제외한 8개 자음 `ㄱㄴㄷㄹㅁㅂㅅㅈ`은 8진수 가변 길이 정수를 부호화하기 위한 목적으로**만** 사용됩니다.

* 자음 `ㄱ, ㄴ, ㄷ, ㄹ, ㅁ, ㅂ, ㅅ, ㅈ`은 각각 8진수 숫자 0, 1, 2, 3, 4, 5, 6, 7을 뜻합니다.
* 가장 낮은 자리수가 가장 먼저 옵니다. 즉, 역순으로 부호화합니다. 예를 들어, 8진수 210은 `ㄱㄴㄷ`로 적습니다.
* 자음 개수가 홀수면 양수를, 자음 개수가 짝수면 음수를 부호화합니다. 뒤에 `ㄱ`(0)을 덧붙이는 방법으로 원하는 부호를 지정할 수 있습니다.

예시는 다음과 같습니다.

* `ㄱ` (oct +0) = 0
* `ㄴ` (oct +1) = 1
* `ㄴㄱ` (oct -01) = -1
* `ㄴㄱㄱ` (oct +001) = 1
* `ㄱㄴ` (oct -10) = -8
* `ㄱㄴㄱ` (oct +010) = +8
* `ㄱㄱㄴ` (oct +100) = +64
* `ㄱㄱㄴㄱ` (oct -0100) = -64

### 나. 단어
단어란 공백을 포함하지 않는 가장 긴 연속한 한글 자음열을 말합니다. 예를 들어 프로그램 `ㄱ ㄴㄷ   ㄱ ㅎㄷ`은 단어 네 개 `ㄱ`, `ㄴㄷ`, `ㄱ`, `ㅎㄷ`으로 이루어져 있습니다.

### 다. 객체와 타입
객체는 프로그램 실행의 기본 단위입니다. 현재 객체가 가질 수 있는 타입은 실수(Number), 논릿값(Boolean), 그리고 함수(Closure) 세 가지입니다. 실수 객체는 8개 자음 `ㄱㄴㄷㄹㅁㅂㅅㅈ`으로만 단어를 구성한 정수 리터럴로 생성하거나, 함수의 호출 결과로 생성될 수 있습니다. 논릿값 또한 함수 호출 결과로 생성합니다. 함수는 함수 정의로 생성하거나, 마찬가지로 다른 함수의 호출 결과로 생성될 수 있습니다.

### 라. 함수 정의
모든 함수는 0개 이상의 객체를 인수로 받아 객체 하나를 돌려줍니다. 함수를 정의할 때 이 함수가 몇 개의 인수를 요구하는지는 따로 표기하지 않으며, 인수 배열의 형태로 접근합니다. 함수를 정의하는 구문은 다음과 같이 함수 몸통이 되는 객체 하나와 단어 `ㅎ`으로 이루어지며, 구문 전체가 함수 객체가 됩니다.

`[함수 몸통] ㅎ`

예를 들어 인수에 상관 없이 실수 3을 돌려주는 함수는 `ㄹ ㅎ`과 같이 정의합니다.

### 마. 함수 호출
인수 n개를 써서 함수를 호출하는 구문은 다음과 같이, (n+1)개의 객체에 이어 `ㅎ` 뒤에 인수 개수 n을 부호화한 정수 리터럴을 붙인 단어 1개로 구성됩니다. 마지막 객체가 호출할 함수이고, 첫 n개의 객체가 이 함수에 인수로 전달됩니다. 

`[인수0] [인수1] [인수2] ... [인수n-1] [함수] ㅎ[정수 리터럴 n]`

인수에 상관 없이 실수 3을 돌려주는 함수에 두 개의 인수 1과 -1을 전달하여 호출하는 구문은 다음과 같습니다.

`ㄴ ㄴㄱ ㄹ ㅎ ㅎㄷ`

#### 기본 제공 함수
본래 호출할 함수는 함수 객체여야 하지만, 정수 리터럴에 한해 실수 객체를 허용하며, 논릿값 객체도 허용합니다. 이 때의 행동은 나열된 바와 같습니다.

* 산술 연산
  * `ㄱ` 곱셈: 실수 여러 개를 받아 모두 곱합니다.
    * 예시: `ㄱㄴ ㄷㄹ ㅁ ㄱ ㅎㄹ` = -0o10 * -0o32 * 0o4 = 0o1500 = 832
  * `ㄷ` 덧셈: 실수 여러 개를 받아 모두 더합니다.
    * 예시: `ㄱㄴ ㄷㄹ ㅁ ㄷ ㅎㄹ` = -0o10 + -0o32 + 0o4 = -0o36 = -30
  * `ㅅ` 거듭제곱: 실수 두 개를 받아 첫번째 인수를 두번째 인수만큼 거듭제곱합니다.
    * 예시: `ㄷ ㄹ ㅅ ㅎㄷ` = 2 ** 3 = 8

* 논리 연산
  * `ㄴ` 같다: 실수 두 개 혹은 논릿값 두 개를 받아 둘이 같으면 `True`를, 다르면 `False`를 반환합니다.
    * 예시: `ㄱ ㄱㄱ ㄴ ㅎㄷ` = (0 == -0) = `True`
  * `ㅈ` 보다 작다: 실수 두 개를 받아 첫번째 인수가 두번째 인수보다 작으면 `True`를, 크거나 같으면 `False`를 반환합니다.
    * 예시: `ㄴㄱ ㄴ ㅈ ㅎㄷ` = (-1 < 1) = `True`
  * `ㅁ` 논리 부정: 논릿값 한 개를 받아 부정합니다.
    * 예시: `ㄱ ㄴ ㄴ ㅎㄷ ㅁ ㅎㄷ` = `True`
  * `ㅈㅈ`: 논릿값 `True`를 만듭니다.
    * 예시: `ㅈㅈ ㅎㄱ` = `True`
  * `ㄱㅈ` 논릿값 `False`를 만듭니다.
    * 예시: `ㄱㅈ ㅎㄱ` = `False`
  * `True`: 인수 두 개를 받아 첫번째 인수를 반환합니다.
    * 예시: `ㄱ ㄴ ㄷ ㄹ ㅈ ㅎㄷ ㅎㄷ` = 0
  * `False`: 인수 두 개를 받아 두번째 인수를 반환합니다.
    * 예시: `ㄱ ㄴ ㄷ ㄹ ㄴ ㅎㄷ ㅎㄷ` = 1

* 기타
  * `ㄹ` 표준 입력: 개행 문자 직전까지 읽어와 적절한 객체로 변환합니다. (현재는 실수만 지원)
    * 예시: `ㄹ ㅎㄱ ㄷ ㅅ ㅎㄷ`은 입력값을 받아 제곱합니다.

### 바. 재귀 함수
함수를 정의할 때 정의하려는 함수 및 둘러싼 함수를 함수 몸통에서 호출할 수 있습니다. 정의하려는 함수를 0번째라고 하고, k번째 함수를 바로 둘러싼 함수를 (k+1)번째라고 합시다. m번째 함수를 접근하려면 다음과 같이 합니다. 참고로 이 번호는 함수(Closure) 객체 안에 환경(Environment)으로서 저장되어 함수 객체를 어느 문맥에서 호출하더라도 일관된 행동을 보장합니다. 다만 m이 음수인 경우는 금지됩니다.

`[정수 리터럴 m] ㅇ`

예를 들어 1번째 함수를 접근하려면 다음과 같이 합니다.

`ㄴ ㅇ`

### 사. 정적 인수 접근
함수를 정의할 때 정의하려는 함수 또는 둘러싼 함수에 전달되는 인수에 접근할 수 있습니다. 앞서와 같이 함수에 번호를 매겨서, m번째 함수의 n번째 인수를 접근하는 구문은 다음과 같습니다. 다만 m이나 n이 음수인 경우는 금지됩니다.

`[정수 리터럴 n] ㅇ[정수 리터럴 m]`

예를 들어 자기가 받은 0번째 인수를 반환하는 함수는 다음과 같습니다.

`ㄱ ㅇㄱ ㅎ`

또, 자기가 받은 0번째 인수와 1번째 함수를 더해 반환하는 함수는 다음과 같습니다.

`ㄱ ㅇㄱ ㄴ ㅇㄱ ㄷ ㅎㄷ ㅎ`

한편 함수 λx.λy.(x+y)는 다음과 같이 작성할 수 있습니다.

`ㄱ ㅇㄴ ㄱ ㅇㄱ ㄷ ㅎㄷ ㅎ ㅎ`

이 함수에 차례로 3과 4를 인수로 넣어 호출하는 구문은 다음과 같습니다.

`ㄹ ㅁ ㄱ ㅇㄴ ㄱ ㅇㄱ ㄷ ㅎㄷ ㅎ ㅎ ㅎㄴ ㅎㄴ`

### 자. 동적 인수 접근
몇 번째 인수를 접근할지가 미리 정해지지 않으면 동적으로 값을 평가해 그 값으로 접근할 수 있습니다. 다음과 같이 객체 하나와 `ㅇ`으로 시작하는 단어 하나로 이뤄진 구문을 생각합시다. 객체를 평가했을 때 실수 x가 나온다고 할 때, 이 구문은 m번째 함수의 round(x)번째 인수를 접근합니다. 다만 round(x)가 음수인 경우는 행동이 정의되어있지 않습니다.

`[객체] ㅇ[정수 리터럴 m]`

예를 들어 `ㄱ ㅇㄱ ㅇㄱ ㅎ`은 다음 의사 코드로 표현할 수 있습니다.

```
def func(*argv):
  idx := int(round(argv[0]))
  return argv[idx]
```

또 `ㄱ ㅇㄱ ㄴ ㄷㅎㄷ ㅇㄱ ㅎ`은 다음 의사 코드로 표현할 수 있습니다.

```
def func(*argv):
  idx := argv[0] + 1
  idx := int(round(idx))
  return argv[idx]
```

## ㄴ. 예시

1. 산술 연산 예시

  * `나 과제 다 했다.` = -55

2. 비교 연산 예시

  * `그는 자는 척했다.` = False
  
3. 함수 예시

  * `날마다 날마다 늘어간 기약과 더하던 후회다.` = 322

4. 팩토리얼 예시

  * `ㄱ [ㄴ {ㄱㅇㄱ (ㄱㅇㄱ ㄴㄱ ㄷㅎㄷ ㄱㅇㅎㄴ) ㄱㅎㄷ} (ㄱㅇㄱ ㄷ ㅈㅎㄷ) ㅎㄷ] ㅎ ㅎㄴ` = 1
  * `ㅂ [ㄴ {ㄱㅇㄱ (ㄱㅇㄱ ㄴㄱ ㄷㅎㄷ ㄱㅇㅎㄴ) ㄱㅎㄷ} (ㄱㅇㄱ ㄷ ㅈㅎㄷ) ㅎㄷ] ㅎ ㅎㄴ` = 120

5. 피보나치 예시

  * `ㄱ [ㄴ {(ㄱㅇㄱ ㄴㄱ ㄷㅎㄷ ㄱㅇㅎㄴ) (ㄱㅇㄱ ㄷㄱ ㄷㅎㄷ ㄱㅇㅎㄴ) ㄷㅎㄷ} (ㄱㅇㄱ ㄷ ㅈㅎㄷ) ㅎㄷ] ㅎ ㅎㄴ` = 1
  * `ㅅ [ㄴ {(ㄱㅇㄱ ㄴㄱ ㄷㅎㄷ ㄱㅇㅎㄴ) (ㄱㅇㄱ ㄷㄱ ㄷㅎㄷ ㄱㅇㅎㄴ) ㄷㅎㄷ} (ㄱㅇㄱ ㄷ ㅈㅎㄷ) ㅎㄷ] ㅎ ㅎㄴ` = 13

6. 배열 비슷한 무언가(?)

  * `ㄱ [ㄴ, ㄷ, ㄹ] ㄱㅇㄱㅇㄴㅎㅎ ㅎㄹ ㅎㄴ` = 1
  * `ㄴ [ㄴ, ㄷ, ㄹ] ㄱㅇㄱㅇㄴㅎㅎ ㅎㄹ ㅎㄴ` = 2
  
7. 논리 부정(?)

  * `난 지금도 가끔 얘기 해. 누군간 여길 꿈꿨을까, 끝없는 헛된 후회 하나 했던걸까...` = 135
  * `난 지금도 늘 얘기 해. 누군간 여길 꿈꿨을까, 끝없는 헛된 후회 하나 했던걸까...` = 1


## ㄷ. 구현체 목록
* Python 구현체
  * `python pbhhg.py` => stdin에서 줄별로 문자열을 읽어 각각을 실행해 결과 출력
  * `python pbhhg.py [문자열]` => 주어진 문자열을 실행해서 결과 출력
* JS 구현체
  * 브라우저로 `pbhhg.html`를 열어 코드를 적은 뒤 실행 버튼 누르기
* C++ 구현체: [kmc7468/unsuspected-hangeul-cpp](https://github.com/kmc7468/unsuspected-hangeul-cpp)


## ㄹ. 판올림 기록
* v0.3 (2019.03.02)
  * 언어 차원에서 논릿값(Boolean)을 지원합니다. 이제 객체는 실수, 논릿값, 함수의 세 종류입니다.
  * 이제 `ㄹㅎㄱ ㄱㅇㄱ ㄱㅇㄱ ㄷㅎㄷ ㅎ ㅎㄴ`을 실행하면 올바르게 입력을 한번만 받습니다.

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
  * 추가적인 산술 연산자와 논리 연산자
  * 외부 파일에서 함수 불러오기
  * 사용자 정의 자료형 (클래스) 생성자 및 속성/메소드 접근
  * map, filter, reduce 등

* 언어 차원에서 문자열 지원이 추가될 수 있습니다.
