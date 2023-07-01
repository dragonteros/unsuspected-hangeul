import * as AS from './abstractSyntax';
/** Forces strict evaluation of the value */
export declare function strict(value: AS.Value): AS.StrictValue;
/** Evaluates the expression in given environment and returns a value */
export declare function interpret(expr: AS.AST, env: AS.Env): AS.Value;
/**
 * Converts function-like values into functions.
 * @param metadata Caller's metadata.
 * @param fun A maybe-Expr value that may correspond to a function.
 * @param allow A list of types that are allowed for execution.
 * @returns A recipe function that receives argument list and returns the value.
 */
export declare function procFunctional(metadata: AS.Metadata, fun: AS.Value, generalCallable?: boolean): AS.Evaluation;
