import * as AS from '../abstractSyntax';
declare class PipeV extends AS.FunctionV {
    private funs;
    constructor(funs: AS.Evaluation[]);
    execute(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.Value;
}
declare class CollectV extends AS.FunctionV {
    private context;
    private fn;
    constructor(context: AS.EvalContextBase, fn: AS.Evaluation);
    execute(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.Value;
}
declare class SpreadV extends AS.FunctionV {
    private fn;
    constructor(fn: AS.Evaluation);
    execute(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.Value;
}
declare function _pipe(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): PipeV;
declare function _collect(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): CollectV;
declare function _spread(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): SpreadV;
declare const _default: {
    ㄴㄱ: typeof _pipe;
    ㅁㅂ: typeof _collect;
    ㅂㅂ: typeof _spread;
};
export default _default;
