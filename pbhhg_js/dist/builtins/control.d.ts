import * as AS from '../abstractSyntax';
declare function _throw(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.Value;
declare function _try(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IntegerV | AS.FloatV | AS.ComplexV | AS.ListV | AS.StringV | AS.BytesV | AS.BooleanV | AS.DictV | AS.ErrorV | AS.FunctionV | AS.NilV | AS.IOV | AS.ExprV;
declare const _default: {
    ㄷㅈ: typeof _throw;
    ㅅㄷ: typeof _try;
};
export default _default;
