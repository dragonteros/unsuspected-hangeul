/* Parser for unsuspected hangeul. */
import BigInteger from 'big-integer'
import * as AS from './abstractSyntax.js'

/** Normalizer **/

// TABLES
// note all ㅇ and ㅎ has a preceding space in following tables
const U1100 = (
  'ㄱ|ㄱ|ㄴ|ㄷ|ㄷ|ㄹ|ㅁ|ㅂ|ㅂ|ㅅ|ㅅ| ㅇ|ㅈ|ㅈ|ㅈ|ㄱ|ㄷ|ㅂ| ㅎ|ㄴㄱ|ㄴ|ㄴㄷ|ㄴㅂ|ㄷㄱ|ㄹㄴ|ㄹ|' +
  'ㄹ ㅎ|ㄹ|ㅁㅂ|ㅁ|ㅂㄱ|ㅂㄴ|ㅂㄷ|ㅂㅅ|ㅂㅅㄱ|ㅂㅅㄷ|ㅂㅅㅂ|ㅂㅅ|ㅂㅅㅈ|ㅂㅈ|ㅂㅈ|ㅂㄷ|ㅂㅂ|ㅂ|' +
  'ㅂ|ㅅㄱ|ㅅㄴ|ㅅㄷ|ㅅㄹ|ㅅㅁ|ㅅㅂ|ㅅㅂㄱ|ㅅㅅ|ㅅ ㅇ|ㅅㅈ|ㅅㅈ|ㅅㄱ|ㅅㄷ|ㅅㅂ|ㅅ ㅎ|ㅅ|ㅅ|ㅅ|ㅅ|' +
  'ㅅ| ㅇㄱ| ㅇㄷ| ㅇㅁ| ㅇㅂ| ㅇㅅ| ㅇㅅ| ㅇ| ㅇㅈ| ㅇㅈ| ㅇㄷ| ㅇㅂ| ㅇ|ㅈ ㅇ|ㅈ|ㅈ|ㅈ|ㅈ|' +
  'ㅈㄱ|ㅈ ㅎ|ㅈ|ㅈ|ㅂㅂ|ㅂ| ㅎ| ㅎ|ㄱㄷ|ㄴㅅ|ㄴㅈ|ㄴ ㅎ|ㄷㄹ'
).split('|')
const JAMO = (
  'ㄱ|ㄱ|ㄱㅅ|ㄴ|ㄴㅈ|ㄴ ㅎ|ㄷ|ㄷ|ㄹ|ㄹㄱ|ㄹㅁ|ㄹㅂ|ㄹㅅ|ㄹㄷ|ㄹㅂ|ㄹ ㅎ|ㅁ|ㅂ|ㅂ|ㅂㅅ|ㅅ|ㅅ|' +
  ' ㅇ|ㅈ|ㅈ|ㅈ|ㄱ|ㄷ|ㅂ| ㅎ'
).split('|')
const U3165 = (
  'ㄴ|ㄴㄷ|ㄴㅅ|ㄴㅅ|ㄹㄱㅅ|ㄹㄷ|ㄹㅂㅅ|ㅁㅅ|ㅁ|ㅂㄱ|ㅂㄷ|ㅂㅅㄱ|ㅂㅅㄷ|ㅂㅈ|ㅂㄷ|ㅂ|ㅂ|ㅅㄱ|ㅅㄴ|' +
  ' ㅇ| ㅇ| ㅇㅅ| ㅇㅅ|ㅂ| ㅎ| ㅎ'
).split('|')
const UA960 = (
  'ㄷㅁ|ㄷㅂ|ㄷㅅ|ㄷㅈ|ㄹㄱ|ㄹㄱ|ㄹㄷ|ㄹㄷ|ㄹㅁ|ㄹㅂ|ㄹㅂ|ㄹㅂ|ㄹㅅ|ㄹㅈ|ㄹㄱ|ㅁㄱ|ㅁㄷ|ㅁㅅ|' +
  'ㅂㅅㄷ|ㅂㄱ|ㅂ ㅎ|ㅅㅂ| ㅇㄹ| ㅇ ㅎ|ㅈ ㅎ|ㄷ|ㅂ ㅎ| ㅎㅅ| ㅎ'
).split('|')

/** Normalizes each character into standard form */
function normalizeChar(c) {
  if (c.length !== 1) {
    throw Error(
      '[normalizeChar] Length of string should be 1, not ' + c.length + ': ' + c
    )
  }

  function _get(arr, ref, divisor = 1) {
    var idx = c.charCodeAt(0) - ref.charCodeAt(0)
    idx = Math.floor(idx / divisor)
    if (idx >= 0 && idx < arr.length) {
      return arr[idx]
    }
    return ''
  }

  if (c >= '\u1100' && c <= '\u11FF') {
    return _get(U1100, '\u1100')
  } else if (c >= '\u302E' && c <= '\u302F') {
    return ''
  } else if (c >= '\u3131' && c <= '\u3164') {
    return _get(JAMO, '\u3131')
  } else if (c >= '\u3165' && c <= '\u318E') {
    return _get(U3165, '\u3165')
  } else if (c >= '\uA960' && c <= '\uA97C') {
    return _get(UA960, '\uA960')
  } else if (c >= '\uAC00' && c <= '\uD7AF') {
    return _get(U1100, '\uAC00', 588)
  } else if (c >= '\uD7B0' && c <= '\uD7C6') {
    return ''
  } else if (c >= '\uD7CB' && c <= '\uD7FB') {
    return ''
  } else if (c >= '\uFFA0' && c <= '\uFFBE') {
    return _get(JAMO, '\uFFA1')
  } else if ('ￂￃￄￅￆￇￊￋￌￍￎￏￒￓￔￕￖￗￚￛￜ'.indexOf(c) >= 0) {
    return ''
  } else return ' '
}

export function normalize(sentence) {
  const normalized = sentence.split('').map(normalizeChar).join('').trim()
  return normalized.split(/( )/)
}

function mergeMetadata(a, b) {
  return AS.Metadata(a.filename, a.line_no, a.start_col, b.end_col, a.line)
}

function tokenize(filename, sentence) {
  if (sentence === '') return []
  const lines = sentence.split('\n')
  const characters = lines.flatMap((line, i) =>
    (line + '\n').split('').flatMap((c, j) =>
      normalize(c)
        .filter((d) => d !== '')
        .map((d) => [d, AS.Metadata(filename, i, j, j + 1, line)])
    )
  )
  let tokens = [characters[0]]
  for (const [cur, metadata] of characters.slice(1)) {
    const [prev, prevMetadata] = tokens.pop()
    if (prev === ' ' && cur === ' ') {
      tokens.push([prev, prevMetadata])
    } else if (prev !== ' ' && cur === ' ') {
      tokens.push([prev + cur, mergeMetadata(prevMetadata, metadata)])
    } else {
      tokens.push([cur, metadata])
    }
  }
  return tokens.filter(([c, metadata]) => c !== ' ')
}

/* Parses jamo-encoded variable length integer into JS Number */
export function parseNumber(s) {
  var tbl = 'ㄱㄴㄷㄹㅁㅂㅅㅈ'
  var varlen = s.split('').map(function (c) {
    return tbl.indexOf(c)
  })
  if (varlen.indexOf(-1) !== -1) {
    throw SyntaxError('Argument ' + s + ' has an unsupported character')
  }
  var num = BigInteger(varlen.reverse().join(''), 8)
  if (s.length % 2 === 0) {
    num = num.times(-1)
  }
  return num
}

/* Encodes JS integer to jamo-encoded variable length integer. */
export function encodeNumber(number) {
  number = BigInteger(number)
  var isNegative = number.isNegative()
  number = number.abs()
  var oct = number.toArray(8).value.reverse()
  var tbl = 'ㄱㄴㄷㄹㅁㅂㅅㅈ'
  var encoded = oct.map((s) => tbl[s]).join('')
  if ((encoded.length % 2 === 0) !== isNegative) {
    encoded += 'ㄱ'
  }
  return encoded
}

/* Parses concrete syntax to abstract syntax
Args:
    word: string. word to parse
    stack: list of parsed legal arguments so far that we will modify
*/
function parseToken(token, stack) {
  const [word, metadata] = token
  if (word.indexOf('ㅎ') !== -1) {
    var arity = word.slice(1)

    if (arity) {
      // AS.FunCall
      arity = parseNumber(arity).toJSNumber()
      if (arity < 0) {
        throw SyntaxError(`함수 호출 시 ${arity}개의 인수를 요구했습니다.`)
      }

      var fun = stack.pop()
      if (arity === 0) {
        stack.push(new AS.FunCall(metadata, fun, []))
      } else {
        var argv = stack.splice(-arity, arity)
        if (argv.length < arity) {
          throw SyntaxError(
            `함수 호출 시 ${arity}개의 인수를 요구했으나 표현식이 ${argv.length}개밖에 없습니다.`
          )
        }
        stack.push(new AS.FunCall(metadata, fun, argv))
      }
    } else {
      // AS.FunDef
      var body = stack.pop()
      stack.push(new AS.FunDef(metadata, body))
    }
  } else if (word.indexOf('ㅇ') !== -1) {
    var trailer = word.slice(1)
    var relF
    if (trailer) {
      // AS.ArgRef
      var relA = stack.pop()
      relF = parseNumber(trailer).toJSNumber()
      stack.push(new AS.ArgRef(metadata, relA, relF))
    } else {
      // AS.FunRef
      relF = stack.pop()
      if (relF instanceof AS.Literal) {
        relF = relF.value.toJSNumber()
      } else {
        throw SyntaxError(
          `함수 참조 시에는 정수 리터럴만 허용되는데 ${relF}를 받았습니다.`
        )
      }
      stack.push(new AS.FunRef(metadata, relF))
    }
  } else {
    stack.push(new AS.Literal(metadata, parseNumber(word)))
  }
}

/* Parses program into abstract syntax */
export function parse(filename, sentence) {
  var tokens = tokenize(filename, sentence)
  var stack = []
  for (const token of tokens) {
    parseToken(token, stack)
  }
  return stack
}

export { normalize, parseNumber, encodeNumber, parse }
