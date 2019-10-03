import * as AS from '../abstractSyntax.js'
import { checkArity, checkType, checkMinArity } from '../utils.js'

export default function (procFunctional, strict) {
  function _input (argv) {
    checkArity(argv, 0)
    return new AS.IOV('ㄹ', argv)
  }
  function _print (argv) {
    checkArity(argv, 1)
    argv = argv.map(strict)
    checkType(argv, AS.StringV)
    return new AS.IOV('ㅈㄹ', argv)
  }
  function _return (argv) {
    checkArity(argv, 1)
    return new AS.IOV('ㄱㅅ', argv)
  }
  function _bind (argv) {
    checkMinArity(argv, 1)
    return new AS.IOV('ㄱㄹ', argv)
  }

  return {
    ㄹ: _input,
    ㅈㄹ: _print,
    ㄱㅅ: _return,
    ㄱㄹ: _bind
  }
}
