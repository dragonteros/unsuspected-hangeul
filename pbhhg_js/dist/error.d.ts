import * as AS from './abstractSyntax';
export declare class UnsuspectedHangeulBuiltinError extends AS.UnsuspectedHangeulError {
    constructor(metadata: AS.Metadata, message: string, codes: bigint[]);
}
export declare class UnsuspectedHangeulOSError extends UnsuspectedHangeulBuiltinError {
    constructor(metadata: AS.Metadata, message: string);
}
export declare class UnsuspectedHangeulArithmeticError extends UnsuspectedHangeulBuiltinError {
    constructor(metadata: AS.Metadata, message: string);
}
export declare class UnsuspectedHangeulSyntaxError extends UnsuspectedHangeulBuiltinError {
    constructor(metadata: AS.Metadata, message: string);
}
export declare class UnsuspectedHangeulTypeError extends UnsuspectedHangeulBuiltinError {
    constructor(metadata: AS.Metadata, message: string);
}
export declare class UnsuspectedHangeulValueError extends UnsuspectedHangeulBuiltinError {
    constructor(metadata: AS.Metadata, message: string);
}
export declare class UnsuspectedHangeulDivisionError extends UnsuspectedHangeulBuiltinError {
    constructor(metadata: AS.Metadata, message: string);
}
export declare class UnsuspectedHangeulNotFoundError extends UnsuspectedHangeulBuiltinError {
    constructor(metadata: AS.Metadata, message: string);
}
export declare class UnsuspectedHangeulImportError extends UnsuspectedHangeulBuiltinError {
    constructor(metadata: AS.Metadata, message: string);
}
export declare class UnsuspectedHangeulOutOfRangeError extends UnsuspectedHangeulBuiltinError {
    constructor(metadata: AS.Metadata, message: string);
}
export declare class UnsuspectedHangeulKeyboardInterruptError extends UnsuspectedHangeulBuiltinError {
    constructor(metadata: AS.Metadata, message: string);
}
