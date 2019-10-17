# > 평범한 한글 v0.6
함수형 난해한 언어 '평범한 한글'의 명세와 구현체입니다.
'평범한 한글' 프로그램은 한글과 그 외 문자로 이루어진 문자열입니다.
여기서 한글은 다음의 범위에 들어가는 유니코드 문자를 말합니다.

* U+1100-U+11FF (한글 자모)
* U+302E-U+302F (방점)
* U+3131-U+318E (호환용 한글 자모)
* U+A960-U+A97C (한글 자모 확장 A)
* U+AC00-U+D7AF (한글 음절)
* U+D7B0-U+D7C6, U+D7CB-U+D7FB (한글 자모 확장 B)
* U+FFA1-U+FFBE, U+FFC2-U+FFC7, U+FFCA-U+FFCF, U+FFD2-U+FFD7, U+FFDA-U+FFDC (반각 한글 자모)

한글은 다시 초성(호환용 한글 자모와 반각 한글 자모는 자음) 및 그 외 한글로 구분해, 초성이 아닌 한글은 삭제하고 초성은 해당하는 호환용 한글 자모로 변환합니다. 한글 음절은 초성만 추출하여 변환합니다. 편의를 위해 이후의 언어 명세에서 한글은 호환용 한글 자모 중 자음이 대표합니다. 변환 예시는 다음과 같습니다.

* `동해물과 백두산이` = `ㄷㅎㅁㄱ ㅂㄷㅅㅇ`
* `나랏〮말〯ᄊᆞ미〮 듕귁〮에〮달아〮` = `ㄴㄹㅁㅆㅁ ㄷㄱㅇㄷㅇ`

한편 한글이 아닌 문자는 달리 구분하지 않고 공백과 같이 생각합니다. 따라서 이후의 설명에도 한글이 아닌 문자는 공백이 대표합니다.

## ㄱ. 명세

거센소리와 된소리는 예사소리와 같게 취급하며, 겹자음은 자음 여러 개로 분리하여 생각합니다. 이는 작문 시 단어 선택의 폭을 넓히기 위한 선택입니다. 예시로, 다음 단어쌍들은 동일합니다.

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
단어란 공백을 포함하지 않는 가장 긴 연속한 한글열을 말합니다. 예를 들어 프로그램 `ㄱ ㄴㄷ   ㄱ ㅎㄷ`은 단어 네 개 `ㄱ`, `ㄴㄷ`, `ㄱ`, `ㅎㄷ`으로 이루어져 있습니다.

### 다. 객체와 자료형
객체는 프로그램 실행의 기본 단위입니다. 객체는 `ㄱㄴㄷㄹㅁㅂㅅㅈ`으로만 단어를 구성한 정수 리터럴이거나, 함수 정의 혹은 호출로 만들어진 것이며, 인수로서 접근될 수 있습니다. 객체가 가질 수 있는 자료형은 실수(Number), 논릿값(Boolean), 문자열(String), 바이트열(Bytes), 목록(List), 사전(Dict), 함수(Closure), 그리고 드나듦(IO)과 빈값(Nil) 일곱 가지가 있습니다.

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
  * `ㄷ` 덧셈: 실수를 하나 이상 받아 모두 더하거나, 논릿값을 하나 이상 받아 하나라도 참인지를 논릿값으로 내놓거나, 한 개 이상의 문자열, 바이트열, 목록 또는 사전을 받아 합칩니다.
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
  * `ㅂㄹ` 분리(split): 문자열 두 개를 받아 두번째 인수를 구분자로 써서 첫번째 인수를 문자열의 목록으로 조각냅니다. 두번째 인수를 생략하거나 빈 문자열을 쓰면 첫번째 인수를 글자 단위로 조각냅니다.
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
  * `ㅈㄷ` 길이: 목록이나 문자열, 바이트열 하나를 받아 길이를 내놓습니다.
    * 예시: `ㄱ ㄴ ㄷ ㅁㄹ ㅎㄹ ㅈㄷ ㅎㄴ` => 3
  * `ㅂㅈ` 발췌(slice): 목록이나 문자열, 바이트열 하나와 실수 세 개를 받아 발췌한 새 목록이나 문자열, 바이트열을 내놓습니다. 두번째 인수는 발췌를 시작할 곳, 세번째 인수는 더 이상 포함하지 않을 곳, 네번째 인수는 몇 글자마다 하나씩 뽑을지를 지정합니다. 세번째 인수를 생략하면 끝까지, 네번째 인수를 생략하면 중간에 빠뜨리는 글자 없이 모두 가져옵니다. 두번째나 세번째 인수로 음수를 지정하면 끝에서부터 셉니다.
    * 예시: `ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅁㄹ ㅎㅅ ㄴ ㄴㄱ ㄷ ㅂㅈ ㅎㅁ` => `[1, 3]`
  * `ㅁㄷ` 요소마다 적용(map): 목록 하나와 함수 하나를 받아, 목록의 각 요소마다 함수를 적용해 새 목록을 만듭니다. 함수는 정수 리터럴, 논릿값 등 함수 대신 호출할 수 있는 것으로 대체할 수 있습니다.
    * 예시: `ㄱ ㄴ ㄷ ㄹ ㅁㄹ ㅎㅁ ㅁㅈ ㅁㄷ ㅎㄷ` => `['0', '1', '2', '3']`
  * `ㅅㅂ` 선별(filter): 목록 하나와 함수 하나를 받아, 목록 중에서 함수를 적용했을 때 참이 되는 요소만 추려 새 목록을 만듭니다. 함수는 정수 리터럴, 논릿값 등 함수 대신 호출할 수 있는 것으로 대체할 수 있습니다.
    * 예시: `ㄱ ㄴ ㄴㄱ ㄷ ㄷㄱ ㅁㄹ ㅎㅂ ㄱ ㅇㄱ ㄱ ㅈ ㅎㄷ ㅎ ㅅㅂ ㅎㄷ` => `[-1, -2]` (`ㄱ ㅇㄱ`은 [사. 정적 인수 접근](#사-정적-인수-접근) 참고)
  * `ㅅㄹ` 수렴(fold): 목록 하나와 초기값으로 쓸 객체 하나, 그리고 함수 하나를 받아 하나의 값으로 수렴시킵니다. 수렴 방법은 목록의 뒤에서부터 객체를 하나씩 뽑아 그 값을 첫번째 인수로, 직전까지의 결과를 두번째 인수로 해 함수를 적용하는 것입니다(foldr). 함수와 목록의 순서를 바꾸어 목록의 앞에서 시작할 수 있으며, 이 경우 직전까지의 결과가 첫번째 인수, 현재 값이 두번째 인수로 전달됩니다(foldl). 두번째 인수를 생략하면 목록에서 적용을 시작할 객체를 초기값으로 대신 사용합니다. 함수는 정수 리터럴, 논릿값 등 함수 대신 호출할 수 있는 것으로 대체할 수 있습니다.
    * 예시: `ㄹ ㄷ ㄴㄱ ㅁㄹ ㅎㄹ ㅅ ㅅㄹ ㅎㄷ` => 3 ** (2 ** -1) = 1.73205...
    * 예시: `ㄹ ㄷ ㄴㄱ ㅁㄹ ㅎㄹ ㅁ ㅅ ㅅㄹ ㅎㄹ` => 3 ** (2 ** (-1 ** 4)) = 9
    * 예시: `ㅅ ㄷ ㄹ ㄷ ㄴㄱ ㅁㄹ ㅎㄹ ㅅㄹ ㅎㄹ` => ((2 ** 3) ** 2) ** -1 = 0.015625
  * 목록: 실수 하나를 받아 그 값이 x로 평가되면 round(x)번째 요소를 내놓습니다. x가 음수이면 뒤에서부터 셉니다.
    * 예시: `ㄹㄱ ㄱ ㄴ ㄷ ㄹ ㅁㄹ ㅎㅁ ㅎㄴ` => 1
  * 바이트열: 실수 하나를 받아 그 값이 x로 평가되면 round(x)번째 바이트를 내놓습니다. x가 음수이면 뒤에서부터 셉니다.

* 모듈
  * 모듈은 기본으로 제공하는 것을 가져오거나 외부 파일에서 직접 불러올 수 있는 '평범한 한글' 객체입니다. 파일에서 불러오는 경우 해당 파일은 UTF-8로 인코딩된 문자열이어야 합니다. 인터프리터는 이 파일을 '평범한 한글' 프로그램으로서 평가해 불러옵니다. 모듈 파일은 불러올 때 혼선이 없도록 하나의 객체만을 만들어야 합니다.
  * `ㅂ` 모듈 불러오기: 정수 리터럴 하나 이상이나 문자열 하나를 받아 해당 경로에서 모듈을 불러옵니다. 문자열은 모듈 파일의 경로로 바로 해석하며, 작업 디렉토리 기준으로 경로내 모든 이름들이 정수 리터럴로 해석할 수 있으면, 정수 리터럴을 대신 나열할 수 있습니다.
    * 예시: './조각글/절댓값.txt'의 내용이 `ㄱㅇㄱ (ㄴㄱ ㄴ ㄱㅇㄱ ㄱ ㅈㅎㄷ ㅎㄷ) ㄱㅎㄷ ㅎ`라고 하면,
      * `ㄷㄴ ㅈ ㅈㄷㄱ ㅂ ㅎㄷ ㅎㄴ` => 10
      * `ㄷㄴㄱ ㅈ ㅈㄷㄱ ㅂ ㅎㄷ ㅎㄴ` => 10
  * '평범한 한글'에서 기본으로 제공하는 모듈은 현재 다음과 같습니다.
    * `ㅂ ㅂ ㅂ ㅎㄷ` 바이트열 변환: 실수 및 문자열과 바이트열 간의 변환을 지원합니다. 실수 두 개와 논릿값 하나를 받아 적절한 새 함수를 내놓습니다. 첫번째 인수는 변환 종류로, 0은 유니코드 변환, 1은 부호 없는 정수 변환, 2는 부호 있는 정수 변환입니다. 두번째 인수는 바이트 몇 개를 사용할지를 지정합니다. 세번째 인수는 빅 엔디언을 사용할지 여부입니다. 세번째 인수를 생략하면 리틀 엔디언을 사용합니다.
      * `ㄱ ㄴ ㅂ ㅂ ㅂ ㅎㄷ ㅎㄷ`: 문자열을 받아 UTF-8 바이트열로 바꾸거나, 바이트열을 받아 UTF-8 문자열로 해독합니다.
      * `ㄱ ㄷ ㅂ ㅂ ㅂ ㅎㄷ ㅎㄷ`: 문자열을 받아 UTF-16 바이트열로 바꾸거나, 바이트열을 받아 UTF-16 문자열로 해독합니다. 바이트열로 바꿀 때 엔디언을 지정하지 않은 경우 BOM(Byte Order Marker)이 추가됩니다.
      * `ㄴ [바이트 수] ㅂ ㅂ ㅂ ㅎㄷ ㅎㄷ`: 음 아닌 정수인 실수를 받아 부호 없는 정수 형태로 지정한 길이의 바이트열로 변환하거나, 바이트열을 받아 부호 없는 정수로 해독합니다. (후자의 경우 두번째 인수는 무시됩니다.)
      * `ㄷ [바이트 수] ㅂ ㅂ ㅂ ㅎㄷ ㅎㄷ`: 정수인 실수를 받아 부호 있는 정수 형태로 지정한 길이의 바이트열로 변환하거나, 바이트열을 받아 부호 있는 정수로 해독합니다. (후자의 경우 두번째 인수는 무시됩니다.)
      * 예시: `ㄱㅁㄱ ㅁㅈ ㅎㄴ ㄱ ㄴ ㅂ ㅂ ㅂ ㅎㄷ ㅎㄷ ㅎㄴ` => `b'\x33\x32'`
      * 예시: `ㄱㅁㄱ ㅁㅈ ㅎㄴ ㄱ ㄷ ㅈㅈ ㅎㄱ ㅂ ㅂ ㅂ ㅎㄷ ㅎㄹ ㅎㄴ` => `b'\x00\x33\x00\x32'`
      * 예시: `ㄱㅁㄱ ㅁㅈ ㅎㄴ ㄱ ㄷ ㄱㅈ ㅎㄱ ㅂ ㅂ ㅂ ㅎㄷ ㅎㄹ ㅎㄴ` => `b'\x33\x00\x32\x00'`
      * 예시: `ㄱㅁㄱ ㄴ ㄹ ㅂ ㅂ ㅂ ㅎㄷ ㅎㄷ ㅎㄴ` => `b'\x20\x00\x00'`
      * 예시: `ㄱㅁ ㄷ ㅁ ㅈㅈ ㅎㄱ ㅂ ㅂ ㅂ ㅎㄷ ㅎㄹ ㅎㄴ` => `b'\xFF\xFF\xFF\xE0'`
      * 예시: `ㄴㄴㅈㄴㅂㄴㅂㅁㅁㅈㄷㅅㅂㄷㅂㅅㄱㅁㄱㄱㄱㄱㅈㄷㅂㄷㄹㄱㄱㅁㄹㅂㄱ ㄴ ㅁㄴㄱ ㅂ ㅂ ㅂ ㅎㄷ ㅎㄷ ㅎㄴ ㄱ ㄷ ㅂ ㅂ ㅂ ㅎㄷ ㅎㄷ ㅎㄴ` => `'평범한 한글'`
      * 예시: `ㅅㅂㅁㅈㄷㄱㄹㅈㄴㅁㄷㄱㄹㅂㄷㅈㄱㅅㅅㄱㄱㅂㄷㅈㄱㅈㄷㄱㄱㅈㄹㄴㅁㅂㄹㄱㄷㄴㄷㅁㄹㅂㄹㅅㄱㅈㅁㅁㄷㅂㄹㄱㄹㅂㅁㅁㅅㅂㄱㄷㅈㄱㅅㄹㅁㅅㄴ ㄴ ㄴㄹㄱ ㅂ ㅂ ㅂ ㅎㄷ ㅎㄷ ㅎㄴ ㄱ ㄴ ㅂ ㅂ ㅂ ㅎㄷ ㅎㄷ ㅎㄴ` => `'./조각글/절댓값.txt'`

* 함수 연산
  * `ㄴㄱ` 함수 연결: 함수를 0개 이상 받아 새 함수를 만듭니다. 새 함수가 호출되면 우선 첫번째 함수를 호출하고, 이후 결과는 다음 함수의 첫번째 인수로 전달되어 연쇄적으로 호출합니다. 함수를 0개 받으면 첫번째 인수를 그대로 내놓는 함수를 만듭니다. 함수는 정수 리터럴, 논릿값 등 함수 대신 호출할 수 있는 것으로 대체할 수 있습니다.
    * 예시: `ㄷ ㄴㄱ ㅎㄱ ㅎㄴ` => 2
    * 예시: `ㄷ ㅁㅈ ㅁㄹ ㄴㄱ ㅎㄷ ㅎㄴ` => `['2']`
  * `ㅁㅂ` 모아받기: 함수 하나를 받아 새 함수를 만듭니다. 새 함수는 목록 하나를 받아 하나하나 나열해 원래 함수에 전달합니다. 즉, 인수를 받을 때 목록으로 모아받도록 함수의 행동을 변경합니다. 함수는 정수 리터럴, 논릿값 등 함수 대신 호출할 수 있는 것으로 대체할 수 있습니다.
    * 예시: `ㄷ ㄹ ㅁㄹ ㅎㄷ ㅁㅈ ㅁㄷ ㅎㄷ ㄷ ㅁㅂ ㅎㄴ ㅎㄴ` => `'23'`
  * `ㅂㅂ` 펴받기: 함수 하나를 받아 새 함수를 만듭니다. 새 함수는 인수 여러 개를 받아 목록으로 만들어 원래 함수에 전달합니다. 함수는 정수 리터럴, 논릿값 등 함수 대신 호출할 수 있는 것으로 대체할 수 있습니다.
    * 예시: `ㅈㄷ ㅂㅂ ㅎㄴ ㅎㄱ` => 0
    * 예시: `ㄱ ㄴ ㄷ ㅈㄷ ㅂㅂ ㅎㄴ ㅎㄹ` => 3

* 드나듦 연산
  자세한 사용법은 이후 [가나가. 드나듦(IO)](#가나가-드나듦IO)에 나와있습니다.
  * `ㄹ` 표준 입력: 드나듦 객체 하나를 만듭니다. 이 객체의 역할은 표준 입력에서 개행 문자 직전까지 읽어와 문자열 객체를 만드는 것입니다. 다만 이 드나듦 객체 자체는 문자가 아니므로 바로 쓸 수 없는 점에 주의하세요.
  * `ㅈㄹ` 표준 출력: 문자열 하나를 받아 드나듦 객체를 만듭니다. 이 객체의 역할은 인수로 받은 문자열을 표준 출력으로 내보내고는 빈값(Nil)을 내놓는 것입니다.
  * `ㄱㄹ` 묶기(bind): 드나듦 객체 여럿과 함수 하나를 받아 새 드나듦 객체를 내놓습니다. 이 드나듦 객체는 인수로 받은 드나듦 객체들이 가져올 값을 받은 함수의 인수로 넣어 호출하는 역할입니다. 함수는 정수 리터럴, 논릿값 등 함수 대신 호출할 수 있는 것으로 대체할 수 있습니다.
  * `ㄱㅅ` 감싸기(return): 객체 하나를 받아 드나듦 객체로 한 꺼풀 감쌉니다. 이 드나듦 객체는 갖고 있던 객체를 그대로 내놓는 역할입니다.

* 기타
  * `ㅅㅈ` 사전: 짝수 개의 객체를 받아 사전(연관 배열)을 만듭니다. 홀수번째 인수와 짝수번째 인수가 키-값 쌍을 이룹니다.
    * 예시: `ㄱ ㄴ ㄷ ㄹ ㅅㅈ ㅎㅁ` => `{0: 1, 2: 3}`
  * 사전: 객체 하나를 받아 그 객체를 키로 하는 값을 내놓습니다.
    * 예시: `ㄷ ㄱ ㄴ ㄷ ㄹ ㅅㅈ ㅎㅁ ㅎㄴ` => `3`
  * 바이트열: 실수 하나를 받아 그 값이 x로 평가되면 round(x)번째 바이트를 내놓습니다. x가 음수이면 뒤에서부터 셉니다.
    * 예시: `ㄴ ㄱㅁㄱ ㅁㅈ ㅎㄴ ㄱ ㄴ ㅂ ㅂ ㅂ ㅎㄷ ㅎㄷ ㅎㄴ ㅎㄴ` => `b'\x32'`
  * `ㅂㄱ` 빈값: 빈값(Nil)을 만듭니다.

### 바. 재귀 함수
함수를 정의할 때 정의하려는 함수 및 둘러싼 함수를 함수 몸통에서 호출할 수 있습니다. 정의하려는 함수를 0번째라고 하고, k번째 함수를 바로 둘러싼 함수를 (k+1)번째라고 합시다. m번째 함수를 접근하려면 다음과 같이 합니다. m이 음수인 경우 바깥쪽에서 (-m-1)번째 함수를 접근합니다. 참고로 이 번호는 함수(Closure) 객체 안에 환경(Environment)으로서 저장되어 함수 객체를 어느 문맥에서 호출하더라도 일관된 행동을 보장합니다.

`[정수 리터럴 m] ㅇ`

예를 들어 1번째 함수를 접근하려면 다음과 같이 합니다.

`ㄴ ㅇ`

### 사. 정적 인수 접근
함수를 정의할 때 정의하려는 함수 또는 둘러싼 함수에 전달되는 인수에 접근할 수 있습니다. 앞서와 같이 함수에 번호를 매겨서, m번째 함수의 n번째 인수를 접근하는 표현식은 다음과 같습니다. m이 음수인 경우 바깥쪽에서 (-m-1)번째 함수의 n번째 인수를 접근합니다. 다만 n이 음수인 경우는 금지됩니다.

`[정수 리터럴 n] ㅇ[정수 리터럴 m]`

예를 들어 자기가 받은 0번째 인수를 내놓는 함수는 다음과 같습니다.

`ㄱ ㅇㄱ ㅎ`

또, 자기가 받은 0번째 인수와 1번째 인수를 더해 내놓는 함수는 다음과 같습니다.

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

먼저, 기본 제공 함수 `ㄹ`을 호출하면 표준 입력에서 문자열을 받아오는 계획이 담긴 드나듦 객체를 얻습니다. 이것과 함께 나중에 그 값으로 무엇을 할지 계획한 함수로 기본 제공 함수 `ㄱㄹ`을 불러 새 드나듦 객체를 만듭니다. 이때 마지막 인수인 함수는 드나듦 객체를 내놓아야 합니다.

예를 들어, 표준 입력에서 문자열을 받아 그대로 표준 출력으로 보내는 계획을 담은 드나듦 객체는 다음과 같습니다.

`ㄹ ㅎㄱ ㄱ ㅇㄱ ㅈㄹ ㅎㄴ ㅎ ㄱㄹ ㅎㄷ`

여기서 `ㄹ ㅎㄱ`은 앞서 언급했듯 문자열을 입력받는 계획이 담긴 드나듦 객체입니다. 한편 `ㅈㄹ ㅎㄴ`은 인수를 출력하는 계획이 담긴 드나듦 객체입니다. 따라서 `ㄱ ㅇㄱ ㅈㄹ ㅎㄴ ㅎ`은 인수를 받아서 그것을 출력할 드나듦 객체를 만드는 함수입니다. 기본 제공 함수 `ㄱㄹ`은 드나듦 객체와 드나듦 객체를 만들 함수를 하나씩 인수로 받아 새 드나듦 객체를 만듭니다. 인터프리터는 이 드나듦 객체를 만나면 첫번째 인수를 실행해 값을 얻고, 이것으로 두번째 인수를 호출합니다. 그 결과로 인터프리터는 표준 출력을 하는 드나듦 객체를 만나, 출력을 수행하고 끝냅니다.

다른 예로, 입력값을 받아 실수로 변환하는 프로그램은 다음과 같습니다. 여기서 기본 제공 함수 `ㄱㅅ`은 나중에 실행되면 인수로 받은 값을 그대로 돌려주는 드나듦을 만듭니다.

`ㄹ ㅎㄱ ㅅㅅ ㄱㅅ ㄴㄱㅎㄷ ㄱㄹ ㅎㄷ`

여기서 함수 `ㅅㅅ ㄱㅅ ㄴㄱㅎㄷ`은 문자열을 실수로 변환해 드나듦 객체로 감싸 내놓는 함수입니다. 기본 제공 함수 `ㄱㄹ`은 `ㄹ`을 호출해 받은 드나듦 객체와 이 함수를 묶어 새 드나듦 객체를 만듭니다. 이후에 이 드나듦 객체가 실행되면 먼저 드나듦 `ㄹ ㅎㄱ`을 실행해 값을 받은 후 이것을 인수로 위 함수를 호출해 최종 드나듦을 받게 됩니다. 이것까지 실행하면 원하는 실수값이 나옵니다.

이것을 응용하여 입력값을 두 개 받아 거듭제곱을 출력하는 프로그램을 다음과 같이 짤 수 있습니다.

`ㄹ ㅎㄱ ㅅㅅ ㄱㅅ ㄴㄱㅎㄷ ㄱㄹ ㅎㄷ ㄱ ㅇㄱ ㄱ ㅇㄱ ㅅ ㅁㅈ ㅈㄹ ㄴㄱ ㅎㄹ ㄱㄹ ㅎㄹ ㅎ ㅎㄴ`

여기서 `ㅅ ㅁㅈ ㅈㄹ ㄴㄱ ㅎㄹ`은 받은 인수로 계산한 거듭제곱을 문자열로 바꿔 출력하는 드나듦 객체를 만드는 함수입니다. 기본 제공 함수 `ㄱㄹ`은 앞서 입력값을 받아 실수로 변환하는 드나듦 객체 두 개와 이 함수를 묶어 우리가 원하는 드나듦 객체를 만들어 줍니다.


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

'조각글' 디렉토리 아래 더 많은 예시가 있습니다. 이는 '평범한 한글' 구현 또는 명세의 일부는 아닙니다.

10. 입력 받은 문자열을 생성하는 '평범한 한글' 코드 생성

  * `조각글 문자만드는평범코드드립니다 ㅂㅎㄷ`
    - '하늘과 바람과 별과 詩' 입력 => `'(ㅂ ㅂ ㅂㅎㄷ) ㅂㅂㅈㄷㄴㄴㅅㅁㄹㅂㄹㅂㄱㄴㅅㅁㄷㅂㅈㄴㄹㄴㅈㅂㄱㅁㅁㅂㅅㄴㅁㅂㅁㄷㅅㅂㅅㅂㅈㅁㅁㄴㄷㅂㅅㅈㅁㅂㅁㅈㄷㄱㄷㅅㄷㅈㄹㅅㄷㄷㄱㅂㄷㅈㄹㅅㄷㅅㄹㄴㄱㄴㄱㅂㅈㅁㄷㄹㄷㅂㄱ (ㄴ ㅅㄹㄱ ㄱㅇㄱㅎㄷ)ㅎㄴ (ㄱ ㄴ ㄱㅇㄱㅎㄷ)ㅎㄴ ㅎㅎㄴ'` 출력
    - 위 코드 실행 => `'하늘과 바람과 별과 詩'`

11. 입력 받은 숫자를 '평범한 한글' 식으로 바꾸기

  * `ㄹㅎㄱ ㅅㅅ (조각글 평범숫자 ㅂㅎㄷ) ㅈㄹ ㄴㄱㅎㄹ ㄱㄹㅎㄷ`
    - '19800518' 입력 => `'ㅅㄱㅈㄱㄷㅁㄹㄴㄴ'` 출력
    - `ㅅㄱㅈㄱㄷㅁㄹㄴㄴ` => 19800518


## ㄷ. 구현체 목록
* Python 구현체
  * `python -m pbhhg_py.main` => stdin에서 줄별로 문자열을 읽어 각각을 실행해 결과 출력
  * `python -m pbhhg_py.main [문자열]` => 주어진 문자열을 실행해서 결과 출력
* JS 구현체:
  * Node.js 환경: `npm install`로 의존성 설치 후 `node pbhhg_js/node.js`
  * 웹 환경:
    - [`pbhhg.html`](https://dragonteros.github.io/unsuspected-hangeul/pbhhg.html) (파일에서 모듈 불러오기는 미구현)
    - [unsuspected-hangeul-ide](https://dragonteros.github.io/unsuspected-hangeul-ide/index.html)
* C++ 구현체: [kmc7468/unsuspected-hangeul-cpp](https://github.com/kmc7468/unsuspected-hangeul-cpp)


## ㄹ. 판올림 기록
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
  * 추가적인 산술 연산자
  * 모듈 불러오기
  * 사용자 정의 자료형
  * foldl, foldr

## ㅂ. 함께 보기

* [평범한 한글 배우기 by @andrea9292](https://www.notion.so/e75c59b8c4514f87822011f2f08715c6)
