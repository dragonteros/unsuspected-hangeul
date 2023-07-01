import * as AS from '../abstractSyntax';
export default function (procFunctional: AS.ProcFunctionalFn, strict: AS.StrictFn, loadUtils: AS.LoadUtils): {
    ㅅ: {
        ㅂ: number;
        ㅈ: number;
        ㅁ: number;
        ㄴ: number;
        ㄱ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.BooleanV;
        ㄴㄴ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.BooleanV;
        ㅁㄴ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.BooleanV;
        ㅈㄷ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.IntegerV | AS.FloatV | AS.ComplexV;
        ㄹㄱ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.FloatV | AS.ComplexV;
        ㅅㄴ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.FloatV | AS.ComplexV;
        ㄴㅅ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.FloatV | AS.ComplexV;
        ㄱㅅ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.FloatV | AS.ComplexV;
        ㅅㄱ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.FloatV | AS.ComplexV;
        ㄷㄴ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.FloatV | AS.ComplexV;
        ㄴㄷ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.FloatV | AS.ComplexV;
        ㅂㄹ: {
            ㄱ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.IntegerV;
            ㄴ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.IntegerV;
            ㄷ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.IntegerV;
            ㄹ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.IntegerV;
            ㅁ: (metadata: AS.Metadata, argv: AS.Value[]) => AS.IntegerV;
        };
    };
};
