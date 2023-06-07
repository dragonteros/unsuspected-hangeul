import * as AS from './abstractSyntax'
import { interpret, procFunctional, strict } from './interpret'
import { parse } from './parse'
import { checkType } from './utils'

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
  if (value instanceof AS.IOV) {
    value = await doIO(value, ioUtils)
    const formatted = await _partial(value)
    return formatIO ? 'IO(' + formatted + ')' : formatted
  }

  if (value instanceof AS.ListV) {
    return '[' + (await Promise.all(value.value.map(_partial))).join(', ') + ']'
  }
  if (value instanceof AS.DictV) {
    const d = value.value
    const keys = value.keys()
    const pairs = await Promise.all(
      keys.map(async (k) => k + ': ' + (await _partial(d[k])))
    )
    return '{' + pairs.join(', ') + '}'
  }
  if (value instanceof AS.ErrorV) {
    const argvStr = (await Promise.all(value.value.map(_partial))).join(', ')
    return '<예외: [' + argvStr + ']>'
  }
  return value.format(strict)
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

/** Main procedure. Parses, evaluates, and converts to str.
 * @param filename File name of the program
 * @param program raw string that encodes a program
 * @returns A string representing the resulting value */
export async function run(
  filename: string,
  program: string,
  argv: string[],
  ioUtils: AS.IOUtils,
  loadUtils: AS.LoadUtils
): Promise<number> {
  const metadata = new AS.Metadata('<main>', 0, 0, 0, '')
  const args = argv.map((arg) => new AS.StringV(arg))

  const exprs = parse(filename, program)
  if (exprs.length === 0) return 0
  if (exprs.length > 1) {
    const error = new AS.ErrorV(
      exprs.map((expr) => expr.metadata),
      `모듈에는 표현식이 하나만 있어야 하는데 ${exprs.length}개가 있습니다.`,
      []
    )
    throw new AS.UnsuspectedHangeulError(error)
  }

  const env = new AS.Env([], [], loadUtils)
  let value = strict(interpret(exprs[0], env))

  if (value instanceof AS.FunctionV) {
    const recipe = procFunctional(metadata, value)
    value = strict(recipe(metadata, args))
  }

  if (value instanceof AS.IOV) {
    value = await doIO(value, ioUtils)
  }

  const [exitCode] = checkType(metadata, [value], [AS.IntegerV, AS.NilV])
  if (exitCode instanceof AS.NilV) return 0
  return Number(exitCode.value)
}

exports.main = main
exports.run = run
