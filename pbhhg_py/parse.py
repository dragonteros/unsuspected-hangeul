'''Parser for esoteric language Unsuspected Hangeul.'''
from pbhhg_py.abstract_syntax import *


def normalize_char(c):
    '''Normalizes each character into standard form'''
    # note all ㅇ and ㅎ has a preceding space in following tables
    jamo = ['ㄱ', 'ㄱ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴ ㅎ',
            'ㄷ', 'ㄷ', 'ㄹ', 'ㄹㄱ', 'ㄹㅁ', 'ㄹㅂ',
            'ㄹㅅ', 'ㄹㄷ', 'ㄹㅂ', 'ㄹ ㅎ', 'ㅁ', 'ㅂ',
            'ㅂ', 'ㅂㅅ', 'ㅅ', 'ㅅ', ' ㅇ', 'ㅈ', 'ㅈ',
            'ㅈ', 'ㄱ', 'ㄷ', 'ㅂ', ' ㅎ']
    choseong = ['ㄱ', 'ㄱ', 'ㄴ', 'ㄷ', 'ㄷ', 'ㄹ', 'ㅁ',
                'ㅂ', 'ㅂ', 'ㅅ', 'ㅅ', ' ㅇ', 'ㅈ', 'ㅈ',
                'ㅈ', 'ㄱ', 'ㄷ', 'ㅂ', ' ㅎ']
    if len(c) != 1:
        raise ValueError(
            'Length of string should be 1, not {}: {}'.format(len(c), c))

    if 'ㄱ' <= c <= 'ㅎ':
        idx = ord(c) - ord('ㄱ')
        return jamo[idx]
    elif '가' <= c <= '힣':
        idx = (ord(c) - ord('가')) // 588
        return choseong[idx]
    elif '\u1100' <= c <= '\u1112':  # 첫가끝 초성
        idx = ord(c) - ord('\u1100')
        return choseong[idx]
    elif '\uFFA1' <= c <= '\uFFBE':  # 반각
        idx = ord(c) - ord('\uFFA1')
        return jamo[idx]
    else:
        return ' '


def parse_number(s):
    '''Parses jamo-encoded variable length integer into python int'''
    tbl = 'ㄱㄴㄷㄹㅁㅂㅅㅈ'
    varlen = [tbl.index(c) for c in s]  # LSB first
    octal = ''.join([str(d) for d in reversed(varlen)])  # MSB first
    num = int(octal, base=8)
    if len(s) % 2 == 0:
        num = -num
    return num


def encode_number(number):
    """Jamo-encodes an python int."""
    is_negative = (number < 0)
    if is_negative:
        number = -number
    # nonnegative integer
    octal = [int(d) for d in '{:o}'.format(number)]
    tbl = 'ㄱㄴㄷㄹㅁㅂㅅㅈ'
    encoded = [tbl[s] for s in reversed(octal)]
    if (len(encoded) % 2 == 0) != is_negative:
        encoded.append('ㄱ')
    return ''.join(encoded)


def parse_word(word, stack):
    '''Parses concrete syntax to abstract syntax
    Args:
        word: str. word to parse
        stack: list of parsed legal arguments so far

    Returns:
        new stack with newly parsed argument appended
    '''
    if 'ㅎ' in word:
        _, arity = word.split('ㅎ')  # Assume space before every ㅎ

        if arity:  # FunCall
            arity = parse_number(arity)
            if arity < 0:
                raise ValueError('Function call with negative number of '
                                 'arguments: {}'.format(arity))

            fun = stack.pop()
            if isinstance(fun, Literal):
                fun = BuiltinFun(fun.value)

            argv = stack[-arity:] if arity else []
            rest = stack[:-arity] if arity else stack
            if len(argv) < arity:
                raise ValueError(
                    'Function call required {} arguments '.format(arity) +
                    'but there are only {}.'.format(len(argv)))

            return rest + [FunCall(fun, argv)]

        else:  # FunDef
            body = stack.pop()
            return stack + [FunDef(body)]

    elif 'ㅇ' in word:
        _, trailer = word.split('ㅇ')  # Assume space before every ㅇ

        if trailer:  # ArgRef
            relF = parse_number(trailer)
            relA = stack.pop()
            return stack + [ArgRef(relA, relF)]

        else:  # FunRef
            relF = stack.pop()
            if not isinstance(relF, Literal):
                raise ValueError(
                    'Function reference admits integer literals only, ' +
                    'but received: {}'.format(relF))
            else:
                relF = relF.value
            return stack + [FunRef(relF)]

    else:
        return stack + [Literal(parse_number(word))]


def parse(sentence):
    '''Parses program into abstract syntax'''
    sentence = ''.join([normalize_char(c) for c in sentence])

    words = sentence.strip().split(' ')
    stack = []
    for word in words:
        if word:
            stack = parse_word(word, stack)
    return stack


def print_parse_tree(arg, indent=0):
    '''Prints the parse tree
    Args:
        arg: Parsed argument whose parse tree is to be printed
        indent: Current indentation status
    Returns:
        None
    '''
    tab = ' ' * 2
    indenter = tab * indent
    if isinstance(arg, int):
        print(indenter + str(arg))
    elif isinstance(arg, list):
        for i, a in enumerate(arg):
            print(indenter + '[{}]'.format(i))
            print_parse_tree(a, indent + 2)
    else:
        typename = type(arg).__name__
        print(indenter + typename)
        for field in arg._fields:
            print(indenter + tab + field)
            print_parse_tree(getattr(arg, field), indent + 2)
