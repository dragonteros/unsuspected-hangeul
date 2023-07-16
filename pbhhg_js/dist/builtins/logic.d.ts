import * as AS from '../abstractSyntax';
declare function _equals(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.BooleanV;
declare function _negate(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.BooleanV;
declare function _lessThan(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.BooleanV;
declare function _true(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.BooleanV;
declare function _false(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.BooleanV;
declare const _default: {
    ㄴ: typeof _equals;
    ㅁ: typeof _negate;
    ㅈ: typeof _lessThan;
    ㅈㅈ: typeof _true;
    ㄱㅈ: typeof _false;
};
export default _default;
