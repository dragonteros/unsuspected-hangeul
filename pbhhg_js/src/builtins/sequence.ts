import * as AS from '../abstractSyntax'
import * as E from '../error'
import {
  checkArity,
  checkType,
  extractValue,
  getLength,
  matchDefaults,
} from '../utils'

function* slice<T>(arr: T[], start: number, end: number, step: number) {
  const startIdx = start < 0 ? start + arr.length : start
  const endIdx = end < 0 ? end + arr.length : end

  if (step > 0) {
    const _startIdx = Math.max(0, startIdx)
    const _endIdx = Math.min(endIdx, arr.length)
    for (let i = _startIdx; i < _endIdx; i += step) {
      yield arr[i]
    }
  } else {
    const _startIdx = Math.min(startIdx, arr.length - 1)
    const _endIdx = Math.max(-1, endIdx)
    for (let i = _startIdx; i > _endIdx; i += step) {
      yield arr[i]
    }
  }
}

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
): Record<string, AS.Evaluation> {
  function _len(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 1)
    const [seq] = checkType(metadata, argv.map(strict), [
      ...AS.SequenceV,
      AS.ErrorV,
    ])
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
    if (step === 0) {
      throw new E.UnsuspectedHangeulValueError(
        metadata,
        '0은 ㅂㅈ 함수의 네 번째 인수로 적합하지 않습니다.'
      )
    }

    if (seq instanceof AS.ListV) {
      const items = slice(seq.value, start, end, step)
      return new AS.ListV(Array.from(items))
    }
    if (seq instanceof AS.StringV) {
      const items = slice(seq.value, start, end, step)
      return new AS.StringV(Array.from(items).join(''))
    }
    const _seq = Array.from(new Uint8Array(seq.value))
    const sliced = slice(_seq, start, end, step)
    return new AS.BytesV(new Uint8Array(sliced).buffer)
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
