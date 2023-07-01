/** Useful utilities **/
import * as AS from './abstractSyntax';
export declare function isLiteralExpr(expr: AS.Value): expr is AS.ExprV & {
    expr: AS.Literal;
};
export declare function extractValue<T>(arg: {
    value: T;
}): T;
export declare function getLength(arg: {
    length: number;
} | ArrayBuffer): number;
export declare function joinArrayBuffer(bufs: ArrayBuffer[]): ArrayBuffer;
export declare function recursiveMap(item: AS.Value, fn: (value: AS.Value) => AS.StrictValue): AS.StrictValue;
export declare function allEqual<T>(arr: T[]): boolean;
export declare function isType<T extends AS.StrictValueType>(argv: AS.StrictValue[], desiredTypes: readonly T[]): argv is InstanceType<T>[];
export declare function checkType<T extends AS.StrictValueType>(metadata: AS.Metadata, argv: AS.StrictValue[], desiredTypes: readonly T[]): InstanceType<T>[];
export declare function checkArity<T>(metadata: AS.Metadata, argv: T[], desiredArities: number | number[]): void;
export declare function checkMinArity<T>(metadata: AS.Metadata, argv: T[], minimumArity: number): void;
export declare function checkMaxArity<T>(metadata: AS.Metadata, argv: T[], maximumArity: number): void;
export declare function matchDefaults<T>(metadata: AS.Metadata, argv: T[], arity: number, defaults?: T[]): T[];
export declare function josa(content: string, particleBatchim: string, particleNoBatchim: string): string;
