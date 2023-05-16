import * as AS from '../abstractSyntax.js'
import { checkArity, checkMinArity, checkType } from '../utils.js'

export default function (procFunctional, strict) {
  function _input(metadata, argv) {
    checkArity(metadata, argv, 0)
    return new AS.IOV('ㄹ', argv)
  }
  function _print(metadata, argv) {
    checkArity(metadata, argv, 1)
    argv = argv.map(strict)
    checkType(metadata, argv, AS.StringV)
    return new AS.IOV('ㅈㄹ', argv)
  }
  function _return(metadata, argv) {
    checkArity(metadata, argv, 1)
    return new AS.IOV('ㄱㅅ', argv)
  }
  function _bind(metadata, argv) {
    checkMinArity(metadata, argv, 1)
    return new AS.IOV('ㄱㄹ', argv)
  }

  return {
    ㄹ: _input,
    ㅈㄹ: _print,
    ㄱㅅ: _return,
    ㄱㄹ: _bind,
  }
}
