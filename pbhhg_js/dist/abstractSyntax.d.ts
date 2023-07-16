/** Abstract syntax and values. **/
import Complex from 'complex.js';
export declare class Metadata {
    filename: string;
    line_no: number;
    start_col: number;
    end_col: number;
    line: string;
    private str?;
    constructor(filename: string, line_no: number, start_col: number, end_col: number, line: string);
    toString(): string;
}
export declare class Literal {
    metadata: Metadata;
    value: bigint;
    constructor(metadata: Metadata, value: bigint);
}
export declare class FunRef {
    metadata: Metadata;
    rel: number;
    constructor(metadata: Metadata, rel: number);
}
export declare class ArgRef {
    metadata: Metadata;
    relA: AST;
    relF: number;
    constructor(metadata: Metadata, relA: AST, relF: number);
}
export declare class FunDef {
    metadata: Metadata;
    body: AST;
    constructor(metadata: Metadata, body: AST);
}
export declare class FunCall {
    metadata: Metadata;
    fun: AST;
    argv: AST[];
    constructor(metadata: Metadata, fun: AST, argv: AST[]);
}
export type AST = Literal | FunRef | ArgRef | FunDef | FunCall;
export type IOUtils = {
    input(): Promise<string | undefined>;
    print(content: string): void;
};
export type File = {
    close(): void;
    read(numBytes: number): Promise<ArrayBuffer>;
    write(bytes: ArrayBuffer): number;
    seek(offset: number, whence: 'SEEK_SET' | 'SEEK_CUR'): number;
    tell(): number;
    truncate(size?: number): number;
};
export type LoadUtils = {
    open(path: string | number, flags: 'a' | 'a+' | 'r' | 'r+' | 'w' | 'w+'): File;
    load(location: string): string;
    isFile(location: string): boolean;
    listdir(location: string): string[];
    joinPath(...parts: string[]): string;
    normalizePath(path: string): string;
};
export declare class Env {
    funs: ClosureV[];
    args: Value[][];
    constructor(funs: ClosureV[], args: Value[][]);
}
export declare class UnsuspectedHangeulError extends Error {
    err: ErrorV;
    constructor(err: ErrorV);
}
declare abstract class ValueBase {
    abstract format(context: EvalContextBase): string;
    asKey(context: EvalContextBase): string;
}
export declare class IntegerV extends ValueBase {
    value: bigint;
    static typeName: string;
    constructor(value: bigint);
    format(context: EvalContextBase): string;
}
export declare class FloatV extends ValueBase {
    value: number;
    static typeName: string;
    constructor(value: number);
    format(context: EvalContextBase): string;
    asKey(context: EvalContextBase): string;
}
export declare class ComplexV extends ValueBase {
    value: Complex;
    static typeName: string;
    constructor(value: Complex);
    format(context: EvalContextBase): string;
    asKey(context: EvalContextBase): string;
}
export declare class BooleanV extends ValueBase {
    value: boolean;
    static typeName: string;
    constructor(value: boolean);
    format(context: EvalContextBase): "True" | "False";
}
export declare class ListV extends ValueBase {
    value: Value[];
    static typeName: string;
    constructor(value: Value[]);
    format(context: EvalContextBase): string;
    asKey(context: EvalContextBase): string;
}
export declare class StringV extends ValueBase {
    str: string;
    static typeName: string;
    value: string[];
    constructor(str: string);
    format(context: EvalContextBase): string;
}
export declare class BytesV extends ValueBase {
    value: ArrayBuffer;
    static typeName: string;
    private str?;
    constructor(value: ArrayBuffer);
    formatByte(c: number): string;
    format(context: EvalContextBase): string;
}
export declare class DictV extends ValueBase {
    value: Record<string, Value>;
    static typeName: string;
    private _keys?;
    private _values?;
    constructor(value: Record<string, Value>);
    keys(): string[];
    values(): Value[];
    format(context: EvalContextBase): string;
    asKey(context: EvalContextBase): string;
}
export declare class IOV extends ValueBase {
    inst: string;
    argv: Value[];
    continuation: (doIO: (ioValue: IOV) => Promise<NonIOStrictValue>, ioUtils: IOUtils) => Promise<StrictValue>;
    static typeName: string;
    constructor(inst: string, argv: Value[], continuation: (doIO: (ioValue: IOV) => Promise<NonIOStrictValue>, ioUtils: IOUtils) => Promise<StrictValue>);
    format(context: EvalContextBase): string;
    asKey(context: EvalContextBase): string;
}
export declare class NilV extends ValueBase {
    static typeName: string;
    constructor();
    format(context: EvalContextBase): string;
}
export declare abstract class FunctionV extends ValueBase {
    static typeName: string;
    private id;
    protected str: string;
    constructor(adj?: string);
    format(context: EvalContextBase): string;
    asKey(context: EvalContextBase): string;
    abstract execute(context: EvalContextBase, metadata: Metadata, argv: Value[]): Value;
}
export declare class ClosureV extends FunctionV {
    body: AST;
    env: Env;
    constructor(body: AST, env: Env);
    execute(context: EvalContextBase, metadata: Metadata, argv: Value[]): ExprV;
}
export declare class BuiltinModuleV extends FunctionV {
    module: Evaluation;
    constructor(module: Evaluation, name: string);
    execute(context: EvalContextBase, metadata: Metadata, argv: Value[]): Value;
}
export declare class ErrorV extends ValueBase {
    metadatas: Metadata[];
    message: string;
    value: StrictValue[];
    static typeName: string;
    constructor(metadatas: Metadata[], message: string, value: StrictValue[]);
    format(context: EvalContextBase): string;
    asKey(context: EvalContextBase): string;
}
export declare class ExprV {
    expr: AST;
    env: Env;
    cache: StrictValue | UnsuspectedHangeulError | null;
    constructor(expr: AST, env: Env, cache: StrictValue | UnsuspectedHangeulError | null);
}
export declare const RealV: readonly [typeof IntegerV, typeof FloatV];
export declare const NumberV: readonly [typeof IntegerV, typeof FloatV, typeof ComplexV];
export declare const SequenceV: readonly [typeof ListV, typeof StringV, typeof BytesV];
export declare const CallableV: readonly [typeof FunctionV, typeof BooleanV, typeof DictV, typeof ComplexV, typeof ErrorV, typeof ListV, typeof StringV, typeof BytesV];
export declare const AnyV: readonly [typeof IntegerV, typeof FloatV, typeof ComplexV, typeof FunctionV, typeof BooleanV, typeof DictV, typeof ComplexV, typeof ErrorV, typeof ListV, typeof StringV, typeof BytesV, typeof IOV, typeof NilV];
export type StrictValueType = (typeof AnyV)[number];
export type NonIOStrictValue = IntegerV | FloatV | ComplexV | ListV | StringV | BytesV | BooleanV | DictV | ErrorV | FunctionV | NilV;
export type StrictValue = NonIOStrictValue | IOV;
export type Value = StrictValue | ExprV;
export type ProcFunctionalFn = (metadata: Metadata, fun: Value, generalCallable?: boolean) => Evaluation;
export type StrictFn = (value: Value) => StrictValue;
export type Evaluation = (context: EvalContextBase, metadata: Metadata, argv: Value[]) => Value;
export declare abstract class EvalContextBase {
    loadUtils: LoadUtils;
    constructor(loadUtils: LoadUtils);
    abstract strict(value: Value): StrictValue;
    abstract procFunctional(metadata: Metadata, fun: Value, generalCallable?: boolean): Evaluation;
}
export {};
