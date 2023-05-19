import * as AS from './abstractSyntax.js'
import { interpret, strict } from './interpret.js'
import { parse } from './parse.js'

/** Receives an IOV and produces non-IOV non-ExprV value. */
function doIO(value: AS.StrictValue, ioUtils: AS.IOUtils): AS.NonIOStrictValue {
  const _doIO = (value: AS.StrictValue) => doIO(value, ioUtils)
  while (value instanceof AS.IOV) {
    value = value.continuation(_doIO, ioUtils)
  }
  return value
}

/** Converts the value into string for display */
export function toString(
  value: AS.Value,
  strict: (v: AS.Value) => AS.StrictValue,
  ioUtils: AS.IOUtils,
  formatIO: boolean
): string {
  const _partial = (v: AS.Value) => toString(v, strict, ioUtils, formatIO)
  value = strict(value)
  if (ioUtils && value instanceof AS.IOV) {
    value = doIO(value, ioUtils)
    const formatted = _partial(value)
    return formatIO ? 'IO(' + formatted + ')' : formatted
  }
  if (value instanceof AS.ListV) {
    return '[' + value.value.map(_partial).join(', ') + ']'
  } else if (value instanceof AS.DictV) {
    const d = value.value
    const keys = value.keys()
    const pairs = keys.map((k) => k + ': ' + _partial(d[k]))
    return '{' + pairs.join(', ') + '}'
  } else if (value instanceof AS.IOV) {
    const argvStr = value.argv.map(_partial).join(',')
    return '<IO ' + value.inst + ' (' + argvStr + ')>'
  }
  return value.toString()
}

/** Main procedure. Parses, evaluates, and converts to str.
 * @param filename File name of the program
 * @param program raw string that encodes a program
 * @returns A string representing the resulting value */
export function main(
  filename: string,
  program: string,
  ioUtils: AS.IOUtils,
  loadUtils: AS.LoadUtils,
  formatIO = true
) {
  const exprs = parse(filename, program)
  const env = new AS.Env([], [], loadUtils)
  const values = exprs.map((expr) => interpret(expr, env))
  return values.map((v) => toString(v, strict, ioUtils, formatIO))
}
