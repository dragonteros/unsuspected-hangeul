import Complex from 'complex.js';
import * as AS from '../abstractSyntax';
export declare function wrapNumber(num: bigint | number | Complex): AS.IntegerV | AS.FloatV | AS.ComplexV;
export default function (procFunctional: AS.ProcFunctionalFn, strict: AS.StrictFn, loadUtils: AS.LoadUtils): Record<string, AS.Evaluation>;
