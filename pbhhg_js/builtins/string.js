import BigInteger from 'big-integer'

import * as AS from '../abstractSyntax.js'
import { checkArity, checkType, extractValue } from '../utils.js'

function checkRadix(string, significant, base) {
  const vocab = '0123456789abcdefghijklmnopqrstuvwxyz'.slice(0, base)
  if (significant.search('^[+-]?[' + vocab + ']+$') === -1) {
    throw EvalError('Cannot convert "' + string + '" to Number.')
  }
}

export default function (procFunctional, strict) {
  function _strToNumber(argv) {
    checkArity(argv, [1, 2])
    argv = argv.map(strict)
    let string = argv[0]
    let base = argv.length > 1 ? argv[1] : new AS.NumberV(10)
    checkType(string, AS.StringV)
    checkType(base, AS.NumberV)
    string = string.value
    base = base.value
    try {
      return new AS.NumberV(BigInteger(string, base))
    } catch (e) {
      if (base == 10 && !isNaN(+string)) {
        return new AS.NumberV(+string)
      }
      const parts = string.trim().split('.').concat([''])
      const significant = parts.join('')
      checkRadix(string, significant, base)
      let num = parseInt(significant, base) / Math.pow(base, parts[1].length)
      return new AS.NumberV(num)
    }
  }

  function _split(argv) {
    checkArity(argv, [1, 2])
    argv = argv.map(strict)
    checkType(argv, AS.StringV)
    var src = argv[0].value
    var delimiter = argv.length > 1 ? argv[1].value : ''
    var pieces = src.split(delimiter)
    return new AS.ListV(pieces.map(piece => new AS.StringV(piece)))
  }

  function _join(argv) {
    checkArity(argv, [1, 2])
    argv = argv.map(strict)
    var seq = argv[0]
    var delimiter = argv.length > 1 ? argv[1] : new AS.StringV('')
    checkType(seq, AS.ListV)
    checkType(delimiter, AS.StringV)
    var pieces = seq.value.map(strict)
    checkType(pieces, AS.StringV)
    return new AS.StringV(pieces.map(extractValue).join(delimiter.value))
  }

  return {
    ㅅㅅ: _strToNumber,
    ㅂㄹ: _split,
    ㄱㅁ: _join
  }
}
