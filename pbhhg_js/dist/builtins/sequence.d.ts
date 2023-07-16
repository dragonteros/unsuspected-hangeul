import * as AS from '../abstractSyntax';
declare function _len(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IntegerV;
declare function _slice(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.ListV | AS.StringV | AS.BytesV;
declare function _map(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.ListV;
declare function _filter(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.ListV;
declare function _fold(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.Value;
declare const _default: {
    ㅈㄷ: typeof _len;
    ㅂㅈ: typeof _slice;
    ㅁㄷ: typeof _map;
    ㅅㅂ: typeof _filter;
    ㅅㄹ: typeof _fold;
};
export default _default;
