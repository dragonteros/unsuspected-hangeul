import * as AS from './abstractSyntax';
export declare class EvalContext implements AS.EvalContextBase {
    loadUtils: AS.LoadUtils;
    constructor(loadUtils: AS.LoadUtils);
    /** Forces strict evaluation of the value */
    strict(value: AS.Value): AS.StrictValue;
    /**
     * Converts function-like values into functions.
     * @param metadata Caller's metadata.
     * @param fun A maybe-Expr value that may correspond to a function.
     * @param generalCallable Whether to allow callable other than function.
     * @returns A recipe function that receives argument list and returns the value.
     */
    procFunctional(metadata: AS.Metadata, fun: AS.Value, generalCallable?: boolean | undefined): AS.Evaluation;
}
/** Evaluates the expression in given environment and returns a value */
export declare function interpret(context: AS.EvalContextBase, expr: AS.AST, env: AS.Env): AS.Value;
