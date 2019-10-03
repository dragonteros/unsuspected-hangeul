import ast
from glob import glob
import json


def proc_module(module_node):
    results = []
    for statement in module_node.body:
        if isinstance(statement, ast.ClassDef):
            name, funs = statement.name, statement.body
            results.append('describe("' + name + '", function () {')
            results.append('\n'.join(proc_fundef(fun) for fun in funs))
            results.append('})')
    return '\n\n'.join(results)


def proc_fundef(fundef_node):
    results = []
    results.append('  it("' + fundef_node.name + '", function () {')
    for expr in fundef_node.body:
        value = expr.value
        if isinstance(value, ast.Call):
            results.append(proc_funcall(value))
    results.append('  })')
    return '\n'.join(results)


def proc_funcall(call_node):
    args = call_node.args
    args = (ast.literal_eval(arg) for arg in args)
    args = (repr(arg) for arg in args)
    return '    _test({})'.format(', '.join(args))


if __name__ == '__main__':
    generated = []

    tests = ['test/test_*.py', 'test/test_builtins/test_*.py',
             'test/test_modules/test_*.py']
    tests = [files for fpath in tests for files in glob(fpath)]
    for path in tests:
        if 'test_base.py' in path or 'test_check.py' in path:
            continue
        print(path)
        with open(path, 'r') as reader:
            program = reader.read()

        module_node = ast.parse(program)
        generated.append(proc_module(module_node))

    with open('test/test.js', 'w') as writer:
        writer.write('''const pbhhg = require('../pbhhg_js/dist/pbhhg')
const loadUtils = require('../pbhhg_js/node').loadUtils
const assert = require('assert')

function makeInput (input) {
  var lines = input? input.split('\\n'): ''
  return () => lines.shift()
}

function _test (program, value, input, output) {
  var printed = []
  const ioUtils = {
    input: makeInput(input),
    print: s => printed.push(s)
  }
  const result = pbhhg.main(program, ioUtils, loadUtils, false)
  assert.deepStrictEqual(result[0], value)
  if (output) {
    assert.strictEqual(printed.join('\\n').trim(), output.trim())
  }
}
''')
        writer.write('\n\n'.join(generated) + '\n')
