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
    commented_out = '    // ' if len(args) != 2 else '    '
    args = [ast.literal_eval(arg) for arg in args]
    args = [json.dumps(arg, ensure_ascii=False) for arg in args]
    return commented_out + '_test({})'.format(', '.join(args))


if __name__ == '__main__':
    generated = []

    tests = ['test/test_*.py', 'test/builtins/test_*.py']
    tests = [files for fpath in tests for files in glob(fpath)]
    for path in tests:
        if 'test_base.py' in path or 'test_check.py' in path:
            continue
        print(path)
        with open(path, 'r') as reader:
            program = reader.read()

        module_node = ast.parse(program)
        generated.append(proc_module(module_node))

    with open('test.js', 'w') as writer:
        writer.write('''const main = require('./pbhhg').main
const assert = require('assert')

function _test (program, value) {
  assert.strictEqual(main(program)[0], value)
}

''')
        writer.write('\n\n'.join(generated) + '\n')
