import * as AS from '../abstractSyntax';
declare class Codec extends AS.FunctionV {
    private scheme;
    private numBytes;
    private bigEndian?;
    private endianness;
    private codec;
    constructor(metadata: AS.Metadata, scheme: AS.StrictValue, numBytes: AS.StrictValue, bigEndian?: AS.StrictValue);
    execute(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.Value;
    getCodec(): AS.Evaluation;
    unicodeCodec(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.StringV | AS.BytesV;
    integerCodec(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IntegerV | AS.BytesV;
    floatingPointCodec(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.Value;
}
declare function codec(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): Codec;
declare const _default: {
    ㅂ: typeof codec;
};
export default _default;
