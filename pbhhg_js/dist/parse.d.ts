import * as AS from './abstractSyntax';
export declare function normalize(sentence: string): string[];
export declare function parseNumber(s: string): bigint;
export declare function encodeNumber(number: number | bigint): string;
export declare function parse(filename: string, sentence: string): AS.AST[];
