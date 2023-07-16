import * as AS from '../abstractSyntax';
declare function _split(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.ListV;
declare function _join(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.StringV | AS.BytesV;
declare const _default: {
    ㅂㄹ: typeof _split;
    ㄱㅁ: typeof _join;
};
export default _default;
