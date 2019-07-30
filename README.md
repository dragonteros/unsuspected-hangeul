﻿# > 평범한 한글 v0.4
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

### 다. 객체와 자료형
객체는 프로그램 실행의 기본 단위이며, 프로그램 역시 하나의 객체입니다. 객체는 `ㄱㄴㄷㄹㅁㅂㅅㅈ`으로만 단어를 구성한 정수 리터럴이거나, 함수 정의 혹은 호출로 만들어진 것이며, 인수로서 접근될 수 있습니다. 객체가 가질 수 있는 자료형은 실수(Number), 논릿값(Boolean), 문자열(String), 목록(List), 함수(Closure), 그리고 드나듦(IO)과 빈값(Nil) 일곱 가지가 있습니다.

### 라. 함수 정의
모든 함수는 0개 이상의 객체를 인수로 받아 객체 하나를 돌려줍니다. 함수를 정의할 때 이 함수가 몇 개의 인수를 요구하는지는 따로 표기하지 않으며, 인수 배열의 형태로 접근합니다. 함수를 정의하는 표현식은 다음과 같이 함수 몸통이 되는 객체 하나와 단어 `ㅎ`으로 이루어지며, 표현식 전체가 함수 객체가 됩니다.

`[함수 몸통] ㅎ`

예를 들어 인수에 상관 없이 실수 3을 돌려주는 함수는 `ㄹ ㅎ`과 같이 정의합니다.

### 마. 함수 호출
인수 n개를 써서 함수를 호출하는 표현식은 다음과 같이, (n+1)개의 객체에 이어 `ㅎ` 뒤에 인수 개수 n을 부호화한 정수 리터럴을 붙인 단어 1개로 구성됩니다. 마지막 객체가 호출할 함수이고, 첫 n개의 객체가 이 함수에 인수로 전달됩니다.

`[인수0] [인수1] [인수2] ... [인수n-1] [함수] ㅎ[정수 리터럴 n]`

인수에 상관 없이 실수 3을 돌려주는 함수에 두 개의 인수 1과 -1을 전달하여 호출하는 표현식은 다음과 같습니다.

`ㄴ ㄴㄱ ㄹ ㅎ ㅎㄷ`

#### 기본 제공 함수
본래 호출할 함수는 함수 객체여야 하지만, 정수 리터럴에 한해 실수 객체를 허용하며, 논릿값과 문자열 및 목록 객체도 허용합니다. 이 때의 행동은 나열된 바와 같습니다.

* 산술 연산
  * `ㄱ` 곱셈: 실수를 하나 이상 받아 모두 곱하거나, 논릿값을 하나 이상 받아 모두 참인지를 논릿값으로 내놓습니다.
    * 예시: `ㄱㄴ ㄷㄹ ㅁ ㄱ ㅎㄹ` => -0o10 * -0o32 * 0o4 = 0o1500 = 832
  * `ㄷ` 덧셈: 실수를 하나 이상 받아 모두 더하거나, 논릿값을 하나 이상 받아 하나라도 참인지를 논릿값으로 내놓습니다.
    * 예시: `ㄱㄴ ㄷㄹ ㅁ ㄷ ㅎㄹ` => -0o10 + -0o32 + 0o4 = -0o36 = -30
  * `ㅅ` 거듭제곱: 실수 두 개를 받아 첫번째 인수를 두번째 인수만큼 거듭제곱합니다.
    * 예시: `ㄷ ㄹ ㅅ ㅎㄷ` => 2 ** 3 = 8

* 논리 연산
  * `ㄴ` 같다: 객체를 두 개 받아 둘이 같은지를 논릿값으로 내놓습니다. 자료형이 다르면 다른 객체이고, 함수는 자기 자신과만 같으며, 목록과 드나듦은 내용으로 비교하며, 그 밖에는 값으로 비교합니다.
    * 예시: `ㄱ ㄱㄱ ㄴ ㅎㄷ` => (0 == -0) = `True`
  * `ㅈ` 보다 작다: 실수 두 개를 받아 첫번째 인수가 두번째 인수보다 작은지를 논릿값으로 내놓습니다.
    * 예시: `ㄴㄱ ㄴ ㅈ ㅎㄷ` => (-1 < 1) = `True`
  * `ㅁ` 논리 부정: 논릿값 한 개를 받아 부정합니다.
    * 예시: `ㄱ ㄴ ㄴ ㅎㄷ ㅁ ㅎㄴ` => `True`
  * `ㅈㅈ`: 논릿값 `True`를 만듭니다.
    * 예시: `ㅈㅈ ㅎㄱ` => `True`
  * `ㄱㅈ` 논릿값 `False`를 만듭니다.
    * 예시: `ㄱㅈ ㅎㄱ` => `False`
  * `True`: 인수 두 개를 받아 첫번째 인수를 내놓습니다.
    * 예시: `ㄱ ㄴ ㄷ ㄹ ㅈ ㅎㄷ ㅎㄷ` => 0
  * `False`: 인수 두 개를 받아 두번째 인수를 내놓습니다.
    * 예시: `ㄱ ㄴ ㄷ ㄹ ㄴ ㅎㄷ ㅎㄷ` => 1

* 문자열 연산
  * `ㅁㅈ` 문자열: 실수 하나를 받아 십진법으로 문자열로 변환합니다. 인수를 생략하면 빈 문자열을 내놓습니다.
    * 예시: `ㅁㅈ ㅎㄱ` => `''`
    * 예시: `ㅁ ㄴㄱ ㅅ ㅎㄷ ㅁㅈ ㅎㄴ` => `'0.25'`
  * `ㅅㅅ` 실수: 문자열 하나와 실수 하나를 받아 첫번째 인수를 실수로 변환하며, 이때 두번째 인수를 진법으로 사용합니다. 두번째 인수를 생략하면 십진법을 사용합니다.
    * 예시: `ㄷㄴㄱ ㅁㅈ ㅎㄴ ㅅㅅ ㅎㄴ` => 10
    * 예시: `ㄷㄴㄱ ㅁㅈ ㅎㄴ ㄷ ㅅㅅ ㅎㄷ` => 2
  * `ㅂㄹ` 분리(split): 문자열 두 개를 받아 두번째 인수를 구분자로 써서 첫번째 인수를 문자열의 목록으로 조각냅니다. 두번째 인수를 생략하거나 빈 문자를 쓰면 첫번째 인수를 글자 단위로 조각냅니다.
    * 예시: `ㅁ ㄷㄱ ㅅ ㅎㄷ ㅁㅈ ㅎㄴ ㅂㄹ ㅎㄴ` => `['0', '.', '0', '6', '2', '5']`
    * 예시: `ㅁ ㄷㄱ ㅅ ㅎㄷ ㅁㅈ ㅎㄴ ㄱ ㅁㅈ ㅎㄴ ㅂㄹ ㅎㄷ` => `['', '.', '625']`
  * `ㄱㅁ` 꿰매기(join): 문자열의 목록 하나와 문자열 하나를 받아 첫번째 인수의 구성원들 사이에 두번째 인수를 끼워넣어 하나의 문자열로 이어붙입니다. 두번째 인수를 생략하면 빈 문자열을 끼워넣습니다.
    * 예시: `ㅁ ㄴㄱ ㅅ ㅎㄷ ㅁㅈ ㅎㄴ ㅂㄹ ㅎㄴ ㄱㅁ ㅎㄴ` => `'0.25'`
    * 예시: `ㅁ ㄴㄱ ㅅ ㅎㄷ ㅁㅈ ㅎㄴ ㅂㄹ ㅎㄴ ㄴ ㅁㅈ ㅎㄴ ㄱㅁ ㅎㄷ` => `'01.1215'`
  * 문자열: 실수 하나를 받아 그 값이 x로 평가되면 round(x)번째 글자를 내놓습니다. x가 음수이면 뒤에서부터 셉니다.
    * 예시: `ㄱ ㄷㄴㄱ ㅁㅈ ㅎㄴ ㅎㄴ` => `'1'`

* 목록 연산
  * `ㅁㄹ` 목록: 0개 이상의 인수를 받아 목록으로 만듭니다.
    * 예시: `ㄱ ㄱㅈ ㅎㄱ ㄱ ㅁㅈ ㅎㄴ ㄱ ㅁㄹ ㅎㄴ ㅁㄹ ㅎㅁ` => `[0, False, '0', [0]]`
  * `ㅈㄷ` 길이: 목록이나 문자열 하나를 받아 길이를 내놓습니다.
    * 예시: `ㄱ ㄴ ㄷ ㅁㄹ ㅎㄹ ㅈㄷ ㅎㄴ` => 3
  * `ㅂㅈ` 발췌(slice): 목록이나 문자열 하나와 실수 세 개를 받아 발췌한 새 목록이나 문자열을 내놓습니다. 두번째 인수는 발췌를 시작할 곳, 세번째 인수는 더 이상 포함하지 않을 곳, 네번째 인수는 몇 글자마다 하나씩 뽑을지를 지정합니다. 세번째 인수를 생략하면 끝까지, 네번째 인수를 생략하면 중간에 빠뜨리는 글자 없이 모두 가져옵니다. 두번째나 세번째 인수로 음수를 지정하면 끝에서부터 셉니다.
    * 예시: `ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅁㄹ ㅎㅅ ㄴ ㄴㄱ ㄷ ㅂㅈ ㅎㅁ` => `[1, 3]`
  * `ㅁㄷ` 요소마다 적용(map): 목록 하나와 함수 하나를 받아, 목록의 각 요소마다 함수를 적용해 새 목록을 만듭니다.
    * 예시: `ㄱ ㄴ ㄷ ㄹ ㅁㄹ ㅎㅁ ㄱ ㅇㄱ ㅁㅈ ㅎㄴ ㅎ ㅁㄷ ㅎㄷ` => `['0', '1', '2', '3']` (`ㄱ ㅇㄱ`은 [사. 정적 인수 접근](#사.-정적-인수-접근) 참고)
  * `ㅅㅂ` 선별(filter): 목록 하나와 함수 하나를 받아, 목록 중에서 함수를 적용했을 때 참이 되는 요소만 추려 새 목록을 만듭니다.
    * 예시: `ㄱ ㄴ ㄴㄱ ㄷ ㄷㄱ ㅁㄹ ㅎㅂ ㄱ ㅇㄱ ㄱ ㅈ ㅎㄷ ㅎ ㅅㅂ ㅎㄷ` => `[-1, -2]` (`ㄱ ㅇㄱ`은 [사. 정적 인수 접근](#사.-정적-인수-접근) 참고)
  * 목록: 실수 하나를 받아 그 값이 x로 평가되면 round(x)번째 요소를 내놓습니다. x가 음수이면 뒤에서부터 셉니다.
    * 예시: `ㄹㄱ ㄱ ㄴ ㄷ ㄹ ㅁㄹ ㅎㅁ ㅎㄴ` => 1


* 드나듦 연산
  자세한 사용법은 이후 [가나가. 드나듦(IO)](#가나가.-드나듦(IO))에 나와있습니다.
  * `ㄹ` 표준 입력: 드나듦 객체 하나를 만듭니다. 이 객체의 역할은 표준 입력에서 개행 문자 직전까지 읽어와 문자 객체를 만드는 것입니다. 다만 이 드나듦 객체 자체는 문자가 아니므로 바로 쓸 수 없는 점에 주의하세요. 
  * `ㅈㄹ` 표준 출력: 문자 하나를 받아 드나듦 객체를 만듭니다. 이 객체의 역할은 인수로 받은 문자를 표준 출력으로 내보내고는 빈값(Nil)을 내놓는 것입니다.
  * `ㄱㄹ` 묶기(bind): 드나듦 객체 여럿과 함수 하나를 받아 새 드나듦 객체를 내놓습니다. 이 드나듦 객체는 인수로 받은 드나듦 객체들이 가져올 값을 받은 함수의 인수로 넣어 호출하는 역할입니다.
  * `ㄱㅅ` 감싸기(return): 객체 하나를 받아 드나듦 객체로 한 꺼풀 감쌉니다. 이 드나듦 객체는 갖고 있던 객체를 그대로 내놓는 역할입니다.

* 기타
  * `ㅂㄱ` 빈값: 빈값(Nil)을 만듭니다.

### 바. 재귀 함수
함수를 정의할 때 정의하려는 함수 및 둘러싼 함수를 함수 몸통에서 호출할 수 있습니다. 정의하려는 함수를 0번째라고 하고, k번째 함수를 바로 둘러싼 함수를 (k+1)번째라고 합시다. m번째 함수를 접근하려면 다음과 같이 합니다. m이 음수인 경우 바깥쪽에서 (-m-1)번째 함수를 접근합니다. 참고로 이 번호는 함수(Closure) 객체 안에 환경(Environment)으로서 저장되어 함수 객체를 어느 문맥에서 호출하더라도 일관된 행동을 보장합니다.

`[정수 리터럴 m] ㅇ`

예를 들어 1번째 함수를 접근하려면 다음과 같이 합니다.

`ㄴ ㅇ`

### 사. 정적 인수 접근
함수를 정의할 때 정의하려는 함수 또는 둘러싼 함수에 전달되는 인수에 접근할 수 있습니다. 앞서와 같이 함수에 번호를 매겨서, m번째 함수의 n번째 인수를 접근하는 표현식은 다음과 같습니다. m이 음수인 경우 바깥쪽에서 (-m-1)번째 함수의 n번째 인수를 접근합니다. 다만 n이 음수인 경우는 금지됩니다.

`[정수 리터럴 n] ㅇ[정수 리터럴 m]`

예를 들어 자기가 받은 0번째 인수를 반환하는 함수는 다음과 같습니다.

`ㄱ ㅇㄱ ㅎ`

또, 자기가 받은 0번째 인수와 1번째 함수를 더해 반환하는 함수는 다음과 같습니다.

`ㄱ ㅇㄱ ㄴ ㅇㄱ ㄷ ㅎㄷ ㅎ`

한편 함수 λx.λy.(x+y)는 다음과 같이 작성할 수 있습니다.

`ㄱ ㅇㄴ ㄱ ㅇㄱ ㄷ ㅎㄷ ㅎ ㅎ`

이 함수에 차례로 3과 4를 인수로 넣어 호출하는 표현식은 다음과 같습니다.

`ㄹ ㅁ ㄱ ㅇㄴ ㄱ ㅇㄱ ㄷ ㅎㄷ ㅎ ㅎ ㅎㄴ ㅎㄴ`

### 자. 동적 인수 접근
몇 번째 인수를 접근할지가 미리 정해지지 않으면 동적으로 값을 평가해 그 값으로 접근할 수 있습니다. 다음과 같이 객체 하나와 `ㅇ`으로 시작하는 단어 하나로 이뤄진 표현식을 생각합시다. 객체를 평가했을 때 실수 x가 나온다고 할 때, 이 표현식은 m번째 함수의 round(x)번째 인수를 접근합니다. 다만 x가 음수인 경우는 금지됩니다.

`[객체] ㅇ[정수 리터럴 m]`

예를 들어 `ㄱ ㅇㄱ ㅇㄱ ㅎ`은 다음 의사 코드로 표현할 수 있습니다.

```
def func(*argv):
  idx := int(round(argv[0]))
  return argv[idx]
```

또 `ㄱ ㅇㄱ ㄴ ㄷ ㅎㄷ ㅇㄱ ㅎ`은 다음 의사 코드로 표현할 수 있습니다.

```
def func(*argv):
  idx := argv[0] + 1
  idx := int(round(idx))
  return argv[idx]
```

### 가나가. 드나듦(IO)
'평범한 한글'의 드나듦 객체는 하스켈의 IO 모나드(Monad)에서 따왔습니다. 이것은 부작용이 있는 연산을 격리하고 실행 순서를 명확하게 하기 위한 목적입니다. 이를 위해 입력받은 값을 바로 활용하는 것은 금지되고, 대신 그 값을 어떻게 활용할지를 미리 계획합니다. 표현식을 전부 평가했을 때 드나듦 객체가 나오면, 인터프리터는 그때부터 드나듦 객체에 적힌 계획에 따라 입출력 연산을 실행하게 됩니다.

먼저, 기본 제공 함수 `ㄹ`을 호출하면 표준 입력에서 문자를 받아오는 계획이 담긴 드나듦 객체를 얻습니다. 이것과 함께 나중에 그 값으로 무엇을 할지 계획한 함수로 기본 제공 함수 `ㄱㄹ`을 불러 새 드나듦 객체를 만듭니다. 이때 마지막 인수인 함수는 드나듦 객체 형태로 반환해야 합니다.

예를 들어, 표준 입력에서 문자를 받아 그대로 표준 출력으로 보내는 계획을 담은 드나듦 객체는 다음과 같습니다.

`ㄹ ㅎㄱ ㄱ ㅇㄱ ㅈㄹ ㅎㄴ ㅎ ㄱㄹ ㅎㄷ`

여기서 `ㄹ ㅎㄱ`은 앞서 언급했듯 문자를 입력받는 계획이 담긴 드나듦 객체입니다. 한편 `ㅈㄹ ㅎㄴ`은 인수를 출력하는 계획이 담긴 드나듦 객체입니다. 따라서 `ㄱ ㅇㄱ ㅈㄹ ㅎㄴ ㅎ`은 인수를 받아서 그것을 출력할 드나듦 객체를 만드는 함수입니다. 기본 제공 함수 `ㄱㄹ`은 드나듦 객체와 드나듦 객체를 만들 함수를 하나씩 인수로 받아 새 드나듦 객체를 만듭니다. 인터프리터는 이 드나듦 객체를 만나면 첫번째 인수를 실행해 값을 얻고, 이것으로 두번째 인수를 호출합니다. 그 결과로 인터프리터는 표준 출력을 하는 드나듦 객체를 만나, 출력을 수행하고 끝냅니다.

다른 예로, 입력값을 받아 실수로 변환하는 프로그램은 다음과 같습니다. 여기서 기본 제공 함수 `ㄱㅅ`은 나중에 실행되면 인수로 받은 값을 그대로 돌려주는 드나듦을 만듭니다.

`ㄹ ㅎㄱ ㄱ ㅇㄱ ㅅㅅ ㅎㄴ ㄱㅅ ㅎㄴ ㅎ ㄱㄹ ㅎㄷ`

여기서 함수 `ㄱ ㅇㄱ ㅅㅅ ㅎㄴ ㄱㅅ ㅎㄴ ㅎ`은 0번째 인수로 받은 문자를 실수로 변환한 뒤 드나듦 객체로 감싸 반환하는 함수입니다. 기본 제공 함수 `ㄱㄹ`은 `ㄹ`을 호출해 받은 드나듦 객체와 이 함수를 묶어 새 드나듦 객체를 만듭니다. 이후에 이 드나듦 객체가 실행되면 먼저 드나듦 `ㄹ ㅎㄱ`을 실행해 값을 받은 후 이것을 인수로 위 함수를 호출해 최종 드나듦을 받게 됩니다. 이것까지 실행하면 원하는 실수값이 반환됩니다.

이것을 응용하여 입력값을 두 개 받아 거듭제곱을 출력하는 프로그램을 다음과 같이 짤 수 있습니다.

`ㄹ ㅎㄱ ㄱ ㅇㄱ ㅅㅅ ㅎㄴ ㄱㅅ ㅎㄴ ㅎ ㄱㄹ ㅎㄷ ㄱ ㅇㄱ ㄱ ㅇㄱ ㄱ ㅇㄱ ㄴ ㅇㄱ ㅅ ㅎㄷ ㅁㅈ ㅎㄴ ㅈㄹ ㅎㄴ ㅎ ㄱㄹ ㅎㄹ ㅎ ㅎㄴ`

여기서 `ㄱ ㅇㄱ ㄴ ㅇㄱ ㅅ ㅎㄷ ㅁㅈ ㅎㄴ ㅈㄹ ㅎㄴ ㅎ`은 받은 인수로 계산한 거듭제곱을 문자로 바꿔 출력하는 드나듦 객체를 만드는 함수입니다. 기본 제공 함수 `ㄱㄹ`은 앞서 입력값을 받아 실수로 변환하는 드나듦 객체 두 개와 이 함수를 묶어 우리가 원하는 드나듦 객체를 만들어 줍니다.


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

  * `ㄱ [ㄴ {(ㄱㅇㄱ ㄴㄱ ㄷㅎㄷ ㄱㅇㅎㄴ) (ㄱㅇㄱ ㄷㄱ ㄷㅎㄷ ㄱㅇㅎㄴ) ㄷㅎㄷ} (ㄱㅇㄱ ㄷ ㅈㅎㄷ) ㅎㄷ] ㅎ ㅎㄴ` = 1
  * `ㅅ [ㄴ {(ㄱㅇㄱ ㄴㄱ ㄷㅎㄷ ㄱㅇㅎㄴ) (ㄱㅇㄱ ㄷㄱ ㄷㅎㄷ ㄱㅇㅎㄴ) ㄷㅎㄷ} (ㄱㅇㄱ ㄷ ㅈㅎㄷ) ㅎㄷ] ㅎ ㅎㄴ` = 13

6. 배열 비슷한 무언가(?)

  * `ㄱ [ㄴ, ㄷ, ㄹ] ㄱㅇㄱㅇㄴㅎㅎ ㅎㄹ ㅎㄴ` = 1
  * `ㄴ [ㄴ, ㄷ, ㄹ] ㄱㅇㄱㅇㄴㅎㅎ ㅎㄹ ㅎㄴ` = 2
  
7. 논리 부정(?)

  * `난 지금도 가끔 얘기 해. 누군간 여길 꿈꿨을까, 끝없는 헛된 후회 하나 했던걸까...` = 135
  * `난 지금도 늘 얘기 해. 누군간 여길 꿈꿨을까, 끝없는 헛된 후회 하나 했던걸까...` = 1

8. 문자열 입력을 여러 개 받아 이어붙이는 드나듦. 빈 문자열을 입력받으면 종료.

  * `ㅁㅈㅎㄱ [ㄹㅎㄱ {(ㄱㅇㄴ ㄱㅅㅎㄴ) (ㄱㅇㄴ ㄱㅇㄱ ㄷㅎㄷ ㄴㅇㅎㄴ) (ㄱㅇㄱ ㅈㄷㅎㄴ ㄱ ㄴㅎㄷ) ㅎㄷ ㅎ} ㄱㄹㅎㄷ ㅎ] ㅎㄴ`

9. 실수 입력을 여러 개 받아 더하는 드나듦. 0을 입력받으면 종료.

  * `ㄱ [(ㄹㅎㄱ ㄱㅇㄱ ㅅㅅㅎㄴ ㄱㅅㅎㄴㅎ ㄱㄹㅎㄷ) {(ㄱㅇㄴ ㄱㅅㅎㄴ) (ㄱㅇㄴ ㄱㅇㄱ ㄷㅎㄷ ㄴㅇㅎㄴ) (ㄱㅇㄱ ㄱ ㄴㅎㄷ) ㅎㄷ ㅎ} ㄱㄹㅎㄷ ㅎ] ㅎㄴ`


## ㄷ. 구현체 목록
* Python 구현체
  * `python py_pbhhg/main.py` => stdin에서 줄별로 문자열을 읽어 각각을 실행해 결과 출력
  * `python pbhhg_py/main.py [문자열]` => 주어진 문자열을 실행해서 결과 출력
* JS 구현체: [`pbhhg.html`](https://dragonteros.github.io/unsuspected-hangeul/pbhhg.html)
* C++ 구현체: [kmc7468/unsuspected-hangeul-cpp](https://github.com/kmc7468/unsuspected-hangeul-cpp)


## ㄹ. 판올림 기록
* v0.5 (2019.07.28)
  * 목록 및 문자열과 관련 기본 제공 함수가 추가되었습니다. 빈값도 추가되어, 이제 객체는 실수, 논릿값, 목록, 문자열, 함수, 드나듦, 빈값의 일곱 종류입니다.
  * 기본 제공 함수 `ㄱ`과 `ㄷ`가 다른 자료형으로 확장되었습니다.
  * 표준 출력 기본 제공 함수 `ㅈㄹ`이 추가되고, 기본 제공 함수 `ㄱㄹ`의 행동이 변경되었습니다.
  * 기본 제공 함수 `ㄹ`의 행동이 변경되었습니다.
    - 주의: v0.4의 행동과 호환되지 않습니다.
  * 프로그램이 하나의 객체만을 가지도록 제한되었습니다.


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
  * 추가적인 산술 연산자
  * 모듈 불러오기
  * 사용자 정의 자료형
  * foldl, foldr

* 언어 차원에서 문자열 지원이 추가될 수 있습니다.

## ㅂ. 함께 보기

* [평범한 한글 배우기 by @andrea9292](https://www.notion.so/e75c59b8c4514f87822011f2f08715c6)
