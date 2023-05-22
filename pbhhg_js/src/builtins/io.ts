import * as AS from '../abstractSyntax'
import { checkArity, checkType } from '../utils'

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
): Record<string, AS.Evaluation> {
  function _input(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 0)
    return new AS.IOV('ㄹ', argv, async function (doIO, ioUtils) {
      const input = await ioUtils.input()
      return input == null ? new AS.NilV() : new AS.StringV(input)
    })
  }
  function _print(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 1)
    const _argv = checkType(metadata, argv.map(strict), [AS.StringV])
    return new AS.IOV('ㅈㄹ', _argv, async function (doIO, ioUtils) {
      ioUtils.print(_argv[0].value)
      return new AS.NilV()
    })
  }
  function _return(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 1)
    return new AS.IOV('ㄱㅅ', argv, async function (doIO, ioUtils) {
      return strict(argv[0])
    })
  }
  function _bind(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [2, 3])
    const [ioToBind] = checkType(metadata, [strict(argv[0])], [AS.IOV])
    return new AS.IOV('ㄱㄹ', argv, async function (doIO, ioUtils) {
      let arg: AS.NonIOStrictValue
      try {
        arg = await doIO(ioToBind)
      } catch (error) {
        if (error instanceof AS.UnsuspectedHangeulError) {
          if (argv.length < 3) throw error
          const result = procFunctional(metadata, argv[2])(metadata, [
            error.err,
          ])
          const [_result] = checkType(metadata, [strict(result)], [AS.IOV])
          return _result
        }
        throw error
      }
      const result = procFunctional(metadata, argv[1])(metadata, [arg])
      const [_result] = checkType(metadata, [strict(result)], [AS.IOV])
      return _result
    })
  }

  return {
    ㄹ: _input,
    ㅈㄹ: _print,
    ㄱㅅ: _return,
    ㄱㄹ: _bind,
  }
}
