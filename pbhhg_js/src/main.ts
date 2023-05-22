import * as AS from './abstractSyntax'
import { interpret, strict } from './interpret'
import { parse } from './parse'

/** Receives an IOV and produces non-IOV non-ExprV value. */
async function doIO(
  value: AS.StrictValue,
  ioUtils: AS.IOUtils
): Promise<AS.NonIOStrictValue> {
  const _doIO = (value: AS.StrictValue) => doIO(value, ioUtils)
  while (value instanceof AS.IOV) {
    value = await value.continuation(_doIO, ioUtils)
  }
  return value
}

/** Converts the value into string for display */
async function toString(
  value: AS.Value,
  strict: (v: AS.Value) => AS.StrictValue,
  ioUtils: AS.IOUtils,
  formatIO: boolean
): Promise<string> {
  const _partial = (v: AS.Value) => toString(v, strict, ioUtils, formatIO)
  value = strict(value)
  if (ioUtils && value instanceof AS.IOV) {
    value = await doIO(value, ioUtils)
    const formatted = await _partial(value)
    return formatIO ? 'IO(' + formatted + ')' : formatted
  }
  if (value instanceof AS.ListV) {
    return '[' + (await Promise.all(value.value.map(_partial))).join(', ') + ']'
  } else if (value instanceof AS.DictV) {
    const d = value.value
    const keys = value.keys()
    const pairs = await Promise.all(
      keys.map(async (k) => k + ': ' + (await _partial(d[k])))
    )
    return '{' + pairs.join(', ') + '}'
  } else if (value instanceof AS.IOV) {
    const argvStr = (await Promise.all(value.argv.map(_partial))).join(',')
    return '<IO ' + value.inst + ' (' + argvStr + ')>'
  }
  return value.toString()
}

/** Main procedure. Parses, evaluates, and converts to str.
 * @param filename File name of the program
 * @param program raw string that encodes a program
 * @returns A string representing the resulting value */
export async function main(
  filename: string,
  program: string,
  ioUtils: AS.IOUtils,
  loadUtils: AS.LoadUtils,
  formatIO = true
): Promise<string[]> {
  const exprs = parse(filename, program)
  const env = new AS.Env([], [], loadUtils)
  const values = exprs.map((expr) => interpret(expr, env))
  return Promise.all(values.map((v) => toString(v, strict, ioUtils, formatIO)))
}

exports.main = main
