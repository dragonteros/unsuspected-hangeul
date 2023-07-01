/**
 * Number operations made generic of argument types
 */
import Complex from 'complex.js';
export type JSNumber = number | bigint | Complex;
export declare function toComplex(x: JSNumber | string): Complex;
export declare function arrayToInt(bigEndianArr: (number | bigint)[] | string, radix?: number | bigint): bigint;
export declare function intToArray(num: bigint, radix?: number | bigint): bigint[];
export declare function isinf(num: JSNumber): boolean;
export declare function isnan(num: JSNumber): boolean;
export declare function eq(a: JSNumber, b: JSNumber): boolean;
export declare function isclose(a: JSNumber, b: JSNumber, rel_tol?: number, abs_tol?: number): boolean;
export declare function abs(num: bigint): bigint;
export declare function abs(num: number | Complex): number;
export declare function abs(num: JSNumber): JSNumber;
export declare function add(a: JSNumber, b: JSNumber): number | bigint | Complex;
export declare function mul(a: JSNumber, b: JSNumber): number | bigint | Complex;
export declare function div(a: number | bigint, b: number | bigint): number | bigint;
export declare function mod(a: number | bigint, b: number | bigint): number | bigint;
export declare function pow(a: JSNumber, b: JSNumber): number | bigint | Complex;
