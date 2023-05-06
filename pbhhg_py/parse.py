"""Parser for esoteric language Unsuspected Hangeul."""
import unicodedata

from pbhhg_py import abstract_syntax as AS

# TABLES
# note all ㅇ and ㅎ has a preceding space in following tables
U1100 = (
    "ㄱ|ㄱ|ㄴ|ㄷ|ㄷ|ㄹ|ㅁ|ㅂ|ㅂ|ㅅ|ㅅ| ㅇ|ㅈ|ㅈ|ㅈ|ㄱ|ㄷ|ㅂ| ㅎ|ㄴㄱ|ㄴ|ㄴㄷ|ㄴㅂ|ㄷㄱ|ㄹㄴ|ㄹ|"
    "ㄹ ㅎ|ㄹ|ㅁㅂ|ㅁ|ㅂㄱ|ㅂㄴ|ㅂㄷ|ㅂㅅ|ㅂㅅㄱ|ㅂㅅㄷ|ㅂㅅㅂ|ㅂㅅ|ㅂㅅㅈ|ㅂㅈ|ㅂㅈ|ㅂㄷ|ㅂㅂ|ㅂ|"
    "ㅂ|ㅅㄱ|ㅅㄴ|ㅅㄷ|ㅅㄹ|ㅅㅁ|ㅅㅂ|ㅅㅂㄱ|ㅅㅅ|ㅅ ㅇ|ㅅㅈ|ㅅㅈ|ㅅㄱ|ㅅㄷ|ㅅㅂ|ㅅ ㅎ|ㅅ|ㅅ|ㅅ|ㅅ|"
    "ㅅ| ㅇㄱ| ㅇㄷ| ㅇㅁ| ㅇㅂ| ㅇㅅ| ㅇㅅ| ㅇ| ㅇㅈ| ㅇㅈ| ㅇㄷ| ㅇㅂ| ㅇ|ㅈ ㅇ|ㅈ|ㅈ|ㅈ|ㅈ|"
    "ㅈㄱ|ㅈ ㅎ|ㅈ|ㅈ|ㅂㅂ|ㅂ| ㅎ| ㅎ|ㄱㄷ|ㄴㅅ|ㄴㅈ|ㄴ ㅎ|ㄷㄹ"
).split("|")
JAMO = (
    "ㄱ|ㄱ|ㄱㅅ|ㄴ|ㄴㅈ|ㄴ ㅎ|ㄷ|ㄷ|ㄹ|ㄹㄱ|ㄹㅁ|ㄹㅂ|ㄹㅅ|ㄹㄷ|ㄹㅂ|ㄹ ㅎ|ㅁ|ㅂ|ㅂ|ㅂㅅ|ㅅ|ㅅ|"
    " ㅇ|ㅈ|ㅈ|ㅈ|ㄱ|ㄷ|ㅂ| ㅎ"
).split("|")
U3165 = (
    "ㄴ|ㄴㄷ|ㄴㅅ|ㄴㅅ|ㄹㄱㅅ|ㄹㄷ|ㄹㅂㅅ|ㅁㅅ|ㅁ|ㅂㄱ|ㅂㄷ|ㅂㅅㄱ|ㅂㅅㄷ|ㅂㅈ|ㅂㄷ|ㅂ|ㅂ|ㅅㄱ|ㅅㄴ|"
    " ㅇ| ㅇ| ㅇㅅ| ㅇㅅ|ㅂ| ㅎ| ㅎ"
).split("|")
UA960 = (
    "ㄷㅁ|ㄷㅂ|ㄷㅅ|ㄷㅈ|ㄹㄱ|ㄹㄱ|ㄹㄷ|ㄹㄷ|ㄹㅁ|ㄹㅂ|ㄹㅂ|ㄹㅂ|ㄹㅅ|ㄹㅈ|ㄹㄱ|ㅁㄱ|ㅁㄷ|ㅁㅅ|"
    "ㅂㅅㄷ|ㅂㄱ|ㅂ ㅎ|ㅅㅂ| ㅇㄹ| ㅇ ㅎ|ㅈ ㅎ|ㄷ|ㅂ ㅎ| ㅎㅅ| ㅎ"
).split("|")


def normalize_char(c: str):
    """Normalizes each character into standard form"""
    if len(c) != 1:
        raise ValueError(
            "Length of string should be 1, not {}: {}".format(len(c), c)
        )

    def _get(arr: list[str], offset: str):
        idx = ord(c) - ord(offset)
        if 0 <= idx < len(arr):
            return arr[idx]
        return ""

    if "\u1100" <= c <= "\u11FF":  # 첫가끝
        return _get(U1100, "\u1100")
    if "\u302E" <= c <= "\u302F":  # 방점
        return ""
    if "\u3131" <= c <= "\u3164":  # 호환용 (현대 한글)
        return _get(JAMO, "\u3131")
    if "\u3165" <= c <= "\u318E":  # 호환용 (옛한글)
        return _get(U3165, "\u3165")
    if "\uA960" <= c <= "\uA97C":  # 확장A
        return _get(UA960, "\uA960")
    if "\uD7B0" <= c <= "\uD7C6":  # 확장B
        return ""
    if "\uD7CB" <= c <= "\uD7FB":
        return ""
    if "\uFFA1" <= c <= "\uFFBE":  # 반각
        return _get(JAMO, "\uFFA1")
    if c in "ￂￃￄￅￆￇￊￋￌￍￎￏￒￓￔￕￖￗￚￛￜ":
        return ""
    return " "


def normalize(sentence: str):
    sentence = unicodedata.normalize("NFD", sentence)
    sentence = "".join(normalize_char(c) for c in sentence)
    return sentence.strip()


def parse_number(s: str):
    """Parses jamo-encoded variable length integer into python int"""
    tbl = "ㄱㄴㄷㄹㅁㅂㅅㅈ"
    varlen = [tbl.index(c) for c in s]  # LSB first
    octal = "".join([str(d) for d in reversed(varlen)])  # MSB first
    num = int(octal, base=8)
    if len(s) % 2 == 0:
        num = -num
    return num


def encode_number(number: int):
    """Jamo-encodes an python int."""
    is_negative = number < 0
    if is_negative:
        number = -number
    # nonnegative integer
    octal: list[int] = [int(d) for d in f"{number:o}"]
    tbl = "ㄱㄴㄷㄹㅁㅂㅅㅈ"
    encoded = [tbl[s] for s in reversed(octal)]
    if (len(encoded) % 2 == 0) != is_negative:
        encoded.append("ㄱ")
    return "".join(encoded)


def parse_word(word: str, stack: list[AS.AST]) -> list[AS.AST]:
    """Parses concrete syntax to abstract syntax
    Args:
        word: str. word to parse
        stack: list of parsed legal arguments so far

    Returns:
        new stack with newly parsed argument appended
    """
    if "ㅎ" in word:
        _, arity = word.split("ㅎ")  # Assume space before every ㅎ

        if arity:  # FunCall
            arity = parse_number(arity)
            if arity < 0:
                raise SyntaxError(f"함수 호출 시 {arity}개의 인수를 요구했습니다.")

            fun = stack.pop()
            argv = stack[-arity:] if arity else []
            rest = stack[:-arity] if arity else stack
            if len(argv) < arity:
                raise SyntaxError(
                    f"함수 호출 시 {arity}개의 인수를 요구했으나 "
                    f"표현식이 {len(argv)}개밖에 없습니다."
                )

            return rest + [AS.FunCall(fun, tuple(argv))]

        else:  # FunDef
            body = stack.pop()
            return stack + [AS.FunDef(body)]

    elif "ㅇ" in word:
        _, trailer = word.split("ㅇ")  # Assume space before every ㅇ

        if trailer:  # ArgRef
            relF = parse_number(trailer)
            relA = stack.pop()
            return stack + [AS.ArgRef(relA, relF)]

        else:  # FunRef
            relF = stack.pop()
            if not isinstance(relF, AS.Literal):
                raise SyntaxError(f"함수 참조 시에는 정수 리터럴만 허용되는데 {relF}를 받았습니다.")
            relF = relF.value
            return stack + [AS.FunRef(relF)]

    else:
        return stack + [AS.Literal(parse_number(word))]


def parse(sentence: str):
    """Parses program into abstract syntax"""
    words = normalize(sentence).split(" ")
    stack = []
    for word in words:
        if word:
            stack = parse_word(word, stack)
    return stack
