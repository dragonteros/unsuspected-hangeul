import * as AS from '../abstractSyntax';
declare function _input(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IOV;
declare function _print(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IOV;
declare function _return(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IOV;
declare function _bind(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IOV;
declare function _file(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IOV;
declare const _default: {
    ㄹ: typeof _input;
    ㅈㄹ: typeof _print;
    ㄱㅅ: typeof _return;
    ㄱㄹ: typeof _bind;
    ㄱㄴ: typeof _file;
};
export default _default;
