import BigInteger from 'big-integer'

import * as AS from '../abstractSyntax.js'
import { extractValue, checkArity, checkType, isType } from '../utils.js'

export default function(procFunctional, strict) {
  function _len(argv) {
    checkArity(argv, 1)
    argv = argv.map(strict)
    checkType(argv, AS.SequenceV)
    const seq = argv[0].value
    const length = isType(argv, AS.BytesV) ? seq.byteLength : seq.length
    return new AS.IntegerV(BigInteger(length))
  }

  function _slice(argv) {
    checkArity(argv, [2, 3, 4])
    argv = argv.map(strict)
    checkType(argv[0], AS.SequenceV)
    checkType(argv.slice(1), AS.IntegerV)
    var seq = argv[0].value
    var start = argv[1].value
    var end = argv.length > 2 ? argv[2].value : seq.length
    seq = seq.slice(start, end)
    var step = argv.length > 3 ? argv[3].value : 1
    var cond = (_, idx) => idx % step === 0
    if (argv[0] instanceof AS.ListV) {
      return new AS.ListV(seq.filter(cond))
    } else if (argv[0] instanceof AS.StringV) {
      return new AS.StringV(
        seq
          .split('')
          .filter(cond)
          .join('')
      )
    } else if (argv[0] instanceof AS.BytesV) {
      const filtered = new Uint8Array(seq).filter(cond)
      const buf = new ArrayBuffer(filtered.byteLength)
      new Uint8Array(buf).set(filtered)
      return new AS.BytesV(buf)
    }
  }

  function _map(argv) {
    checkArity(argv, 2)
    var seq = strict(argv[0])
    checkType(seq, AS.ListV)
    var fn = procFunctional(argv[1])
    return new AS.ListV(seq.value.map(a => fn([a])))
  }

  function _filter(argv) {
    checkArity(argv, 2)
    var seq = strict(argv[0])
    checkType(seq, AS.ListV)
    var fn = procFunctional(argv[1])

    seq = seq.value
    var fitCheck = seq.map(a => fn([a])).map(strict)
    checkType(fitCheck, AS.BooleanV)
    fitCheck = fitCheck.map(extractValue)
    return new AS.ListV(seq.filter((_, idx) => fitCheck[idx]))
  }

  function _fold(argv) {
    checkArity(argv, [2, 3])
    var init = null
    if (argv.length === 3) {
      init = argv[1]
      argv = [argv[0], argv[2]]
    }

    var preservedArgv = argv
    argv = argv.map(strict)
    const fromRight = argv[0] instanceof AS.ListV
    function maybeReversed(arr) {
      if (!fromRight) return arr
      return arr.slice().reverse()
    }
    argv = maybeReversed(argv)
    preservedArgv = maybeReversed(preservedArgv)
    var fn = procFunctional(preservedArgv[0], [], argv[0])
    checkType(argv[1], AS.ListV)

    var feed = maybeReversed(argv[1].value)
    if (init === null) {
      init = feed[0]
      feed = feed.slice(1)
    }
    return feed.reduce(function(acc, item) {
      var args = maybeReversed([acc, item])
      return fn(args)
    }, init)
  }

  return {
    ㅈㄷ: _len,
    ㅂㅈ: _slice,
    ㅁㄷ: _map,
    ㅅㅂ: _filter,
    ㅅㄹ: _fold
  }
}
