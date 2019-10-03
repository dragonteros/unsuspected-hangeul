import * as AS from '../abstractSyntax.js'
import { checkArity, checkType, recursiveMap, toString } from '../utils.js'

export default function (procFunctional, strict) {
  function _list (argv) {
    return new AS.ListV(argv)
  }
  function _dict (argv) {
    const len = argv.length
    if (len % 2 === 1) {
      throw SyntaxError('Dict requires even numbers of arguments ' +
        'but received: ' + len)
    }
    var keys = argv.filter((_, i) => i % 2 === 0)
    var values = argv.filter((_, i) => i % 2 === 1)
    keys = keys.map(item => recursiveMap(item, strict))
    keys = keys.map(v => toString(v, strict))
    var result = {}
    for (let i = 0; i < len / 2; i++) {
      result[keys[i]] = values[i]
    }
    return new AS.DictV(result)
  }
  function _string (argv) {
    checkArity(argv, [0, 1])
    if (argv.length === 0) return new AS.StringV('')
    var arg = strict(argv[0])
    checkType(arg, [AS.NumberV, AS.StringV])
    if (arg instanceof AS.StringV) return arg
    var value = arg.value
    if (value === (value | 0)) {
      value = value | 0
    }
    return new AS.StringV(value.toString())
  }
  function _nil (argv) {
    checkArity(argv, 0)
    return new AS.NilV()
  }

  return {
    ㅅㅈ: _dict,
    ㅁㄹ: _list,
    ㅁㅈ: _string,
    ㅂㄱ: _nil
  }
}
