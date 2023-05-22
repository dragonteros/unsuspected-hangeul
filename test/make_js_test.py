import ast
from glob import glob


def proc_module(module_node: ast.Module):
    results: list[str] = []
    for statement in module_node.body:
        if isinstance(statement, ast.ClassDef):
            name, funs = statement.name, statement.body
            results.append('describe("' + name + '", function () {')
            results.append("\n".join(proc_fundef(fun) for fun in funs))
            results.append("})")
    return "\n\n".join(results)


def proc_fundef(fundef_node: ast.FunctionDef):
    results: list[str] = []
    results.append('  it("' + fundef_node.name + '", function () {')
    for expr in fundef_node.body:
        value = expr.value
        if isinstance(value, ast.Call):
            results.append(proc_funcall(value))
    results.append("  })")
    return "\n".join(results)


def proc_funcall(call_node: ast.Call):
    args = call_node.args
    args = (ast.literal_eval(arg) for arg in args)
    args = (repr(arg) for arg in args)
    return "    _test({})".format(", ".join(args))


if __name__ == "__main__":
    generated: list[str] = []

    tests = [
        "test/test_*.py",
        "test/test_builtins/test_*.py",
        "test/test_modules/test_*.py",
    ]
    tests = [files for fpath in tests for files in glob(fpath)]
    for path in tests:
        if "test_base.py" in path or "test_utils.py" in path:
            continue
        print(path)
        with open(path, "r", encoding="utf-8") as reader:
            program = reader.read()

        module_node = ast.parse(program)
        generated.append(proc_module(module_node))

    with open("pbhhg_js/test/test.ts", "w", encoding="utf-8") as writer:
        writer.write(
            r"""import { describe, it } from '@jest/globals'
import assert from 'assert'
import { loadUtils } from '../cli'
import { IOUtils } from '../src/abstractSyntax'
import { main } from '../src/main'

function makeInput(input: string | undefined) {
  var lines = input ? input.split('\n') : []
  return () => Promise.resolve(lines.shift())
}

function _test(
  program: string,
  value: string,
  input?: string,
  output?: string
) {
  const printed: string[] = []
  const ioUtils: IOUtils = {
    input: makeInput(input),
    print: (s: string) => printed.push(s),
  }
  main('<test>', program, ioUtils, loadUtils, false).then((result) => {
    assert.deepStrictEqual(result, [value])
    if (output) {
      assert.strictEqual(printed.join('\n').trim(), output.trim())
    }
  })
}
"""
        )
        writer.write("\n\n".join(generated) + "\n")
