import Complex from 'complex.js';
import * as AS from '../abstractSyntax';
export declare function wrapNumber(num: bigint | number | Complex): AS.IntegerV | AS.FloatV | AS.ComplexV;
declare function _multiply(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IntegerV | AS.FloatV | AS.ComplexV | AS.BooleanV;
declare function _add(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IntegerV | AS.FloatV | AS.ComplexV | AS.ListV | AS.StringV | AS.BytesV | AS.BooleanV | AS.DictV;
declare function _exponentiate(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IntegerV | AS.FloatV | AS.ComplexV;
declare function _integerDivision(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IntegerV | AS.FloatV | AS.ComplexV;
declare function _remainder(context: AS.EvalContextBase, metadata: AS.Metadata, argv: AS.Value[]): AS.IntegerV | AS.FloatV | AS.ComplexV;
declare const _default: {
    ㄱ: typeof _multiply;
    ㄷ: typeof _add;
    ㅅ: typeof _exponentiate;
    ㄴㄴ: typeof _integerDivision;
    ㄴㅁ: typeof _remainder;
};
export default _default;
