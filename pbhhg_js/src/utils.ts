/** Useful utilities **/
import { josa } from 'josa'
import * as AS from './abstractSyntax'
import * as E from './error'

export function isLiteralExpr(
  expr: AS.Value
): expr is AS.ExprV & { expr: AS.Literal } {
  return expr instanceof AS.ExprV && expr.expr instanceof AS.Literal
}

export function extractValue<T>(arg: { value: T }): T {
  return arg.value
}

export function getLength(arg: { length: number } | ArrayBuffer) {
  return 'length' in arg ? arg.length : arg.byteLength
}

export function joinArrayBuffer(bufs: ArrayBuffer[]) {
  const size = bufs.map((a) => a.byteLength).reduce((a, b) => a + b, 0)
  const newBuf = new ArrayBuffer(size)
  const view = new Uint8Array(newBuf)
  bufs.reduce(function (idx, buf) {
    view.set(new Uint8Array(buf), idx)
    return idx + buf.byteLength
  }, 0)
  return newBuf
}

export function recursiveMap(
  item: AS.Value,
  fn: (value: AS.Value) => AS.StrictValue
): AS.StrictValue {
  const _item = fn(item)
  if (_item instanceof AS.ListV) {
    return new AS.ListV(_item.value.map((v) => recursiveMap(v, fn)))
  }
  if (_item instanceof AS.DictV) {
    const d = _item.value
    const result: Record<string, AS.StrictValue> = {}
    Object.keys(d).forEach(function (k) {
      result[k] = recursiveMap(d[k], fn)
    })
    return new AS.DictV(result)
  }
  if (_item instanceof AS.ErrorV) {
    return new AS.ErrorV(
      _item.metadatas,
      _item.message,
      _item.value.map((v) => recursiveMap(v, fn))
    )
  }
  return _item
}

export function allEqual<T>(arr: T[]): boolean {
  if (arr.length === 0) return true
  return arr.every(function (a) {
    return a === arr[0]
  })
}

/* Argument constraint checkers */
export function isType<T extends AS.StrictValueType>(
  argv: AS.StrictValue[],
  desiredTypes: readonly T[]
): argv is InstanceType<T>[] {
  function _matches(arg: AS.StrictValue) {
    return desiredTypes.some(function (desiredType) {
      return arg instanceof desiredType
    })
  }
  return argv.every(_matches)
}

function _formatArray(arr: string[], conj = ', ') {
  return arr.join(conj)
}

export function checkType<T extends AS.StrictValueType>(
  metadata: AS.Metadata,
  argv: AS.StrictValue[],
  desiredTypes: readonly T[]
): InstanceType<T>[] {
  if (isType(argv, desiredTypes)) return argv
  const desiredTypeNames = desiredTypes.map((t) => t.typeName)
  const argTypeNames = argv.map(
    (a) => (a.constructor as AS.StrictValueType).typeName
  )
  throw new E.UnsuspectedHangeulTypeError(
    metadata,
    josa(
      `인수를 ${_formatArray(desiredTypeNames)} 중에서 주어야 하는데 ` +
        `${_formatArray(argTypeNames)}#{를} 주었습니다.`
    )
  )
}

export function checkArity<T>(
  metadata: AS.Metadata,
  argv: T[],
  desiredArities: number | number[]
) {
  const arities = Array.isArray(desiredArities)
    ? desiredArities
    : [desiredArities]
  if (arities.indexOf(argv.length) !== -1) return
  throw new E.UnsuspectedHangeulValueError(
    metadata,
    `인수를 ${_formatArray(
      arities.map((a) => a.toString()),
      '개나 '
    )}개를 주어야 하는데 ` + `${argv.length}개의 인수를 주었습니다.`
  )
}

export function checkMinArity<T>(
  metadata: AS.Metadata,
  argv: T[],
  minimumArity: number
) {
  if (argv.length >= minimumArity) return
  throw new E.UnsuspectedHangeulValueError(
    metadata,
    `인수를 ${minimumArity}개 이상 주어야 하는데` +
      `${argv.length}개 주었습니다.`
  )
}

export function checkMaxArity<T>(
  metadata: AS.Metadata,
  argv: T[],
  maximumArity: number
) {
  if (argv.length <= maximumArity) return
  throw new E.UnsuspectedHangeulValueError(
    metadata,
    `인수를 ${maximumArity}개 이하 주어야 하는데` +
      `${argv.length}개 주었습니다.`
  )
}

export function matchDefaults<T>(
  metadata: AS.Metadata,
  argv: T[],
  arity: number,
  defaults?: T[]
) {
  if (defaults === undefined) {
    defaults = []
  }
  checkMaxArity(metadata, argv, arity)
  checkMinArity(metadata, argv, arity - defaults.length)
  if (argv.length < arity) {
    let deficiency = arity - argv.length
    argv = argv.concat(defaults.slice(-deficiency))
  }
  return argv
}
