import * as AS from '../abstractSyntax'
import {
  checkArity,
  checkType,
  extractValue,
  getLength,
  matchDefaults,
} from '../utils'

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
): Record<string, AS.Evaluation> {
  function _len(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 1)
    const [seq] = checkType(metadata, argv.map(strict), AS.SequenceV)
    if (seq instanceof AS.BytesV) {
      return new AS.IntegerV(BigInt(seq.value.byteLength))
    }
    return new AS.IntegerV(BigInt(seq.value.length))
  }

  function _slice(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [2, 3, 4])
    const _argv = argv.map(strict)
    const [seq] = checkType(metadata, [_argv[0]], AS.SequenceV)
    const rest = checkType(metadata, _argv.slice(1), [AS.IntegerV])
    const _rest = rest.map((arg) => Number(arg.value))
    const [start, end, step] = matchDefaults(metadata, _rest, 3, [
      getLength(seq.value),
      1,
    ])
    const _seq = seq.value.slice(start, end)
    var cond = <T>(_: T, idx: number) => idx % step === 0
    if (Array.isArray(_seq)) {
      return new AS.ListV(_seq.filter(cond))
    }
    if (typeof _seq === 'string') {
      return new AS.StringV(_seq.split('').filter(cond).join(''))
    }
    const filtered = new Uint8Array(_seq).filter(cond)
    const buf = new ArrayBuffer(filtered.byteLength)
    new Uint8Array(buf).set(filtered)
    return new AS.BytesV(buf)
  }

  function _map(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 2)
    const [seq] = checkType(metadata, [strict(argv[0])], [AS.ListV])
    const fn = procFunctional(metadata, argv[1])
    return new AS.ListV(seq.value.map((a) => fn(metadata, [a])))
  }

  function _filter(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 2)
    const [seq] = checkType(metadata, [strict(argv[0])], [AS.ListV])
    const fn = procFunctional(metadata, argv[1])

    const fitCheck = seq.value.map((a) => fn(metadata, [a])).map(strict)
    const fit = checkType(metadata, fitCheck, [AS.BooleanV]).map(extractValue)
    return new AS.ListV(seq.value.filter((_, idx) => fit[idx]))
  }

  function _fold(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [2, 3])
    let init: AS.Value | null = null
    if (argv.length === 3) {
      init = argv[1]
      argv = [argv[0], argv[2]]
    }

    const first = strict(argv[0])
    const fromRight = first instanceof AS.ListV
    function maybeReversed<T>(arr: T[]): T[] {
      if (!fromRight) return arr
      return arr.slice().reverse()
    }

    argv = maybeReversed(argv)
    const fn = procFunctional(metadata, argv[0])
    const [seq] = checkType(metadata, [strict(argv[1])], [AS.ListV])

    let feed = maybeReversed(seq.value)
    if (init == null) {
      init = feed[0]
      feed = feed.slice(1)
    }
    return feed.reduce(function (acc, item) {
      const args = maybeReversed([acc, item])
      return fn(metadata, args)
    }, init)
  }

  return {
    ㅈㄷ: _len,
    ㅂㅈ: _slice,
    ㅁㄷ: _map,
    ㅅㅂ: _filter,
    ㅅㄹ: _fold,
  }
}
