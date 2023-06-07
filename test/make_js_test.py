import ast
import glob
import os


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
    results.append('  it("' + fundef_node.name + '", async function () {')
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
    return "    await test({})".format(", ".join(args))


if __name__ == "__main__":
    tests = [
        "test/test_*.py",
        "test/test_builtins/test_*.py",
        "test/test_modules/test_*.py",
    ]
    tests = [files for fpath in tests for files in glob.glob(fpath)]
    for path in tests:
        if "test_base.py" in path or "test_utils.py" in path:
            continue
        print(f"Converting {path}...")
        with open(path, "r", encoding="utf-8") as reader:
            program = reader.read()

        module_node = ast.parse(program)
        generated = proc_module(module_node)

        output_path = os.path.join("pbhhg_js", path.replace(".py", ".ts"))
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        base_rel_path = os.path.relpath(
            "pbhhg_js/test/base", output_dir
        ).replace("\\", "/")
        with open(output_path, "w", encoding="utf-8") as writer:
            writer.write(
                rf"""import {{ describe, it }} from '@jest/globals'
import {{ test }} from './{base_rel_path}'

{generated}
"""
            )
