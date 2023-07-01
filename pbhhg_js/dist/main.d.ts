import * as AS from './abstractSyntax';
/** Main procedure. Parses, evaluates, and converts to str.
 * @param filename File name of the program
 * @param program raw string that encodes a program
 * @returns A string representing the resulting value */
export declare function main(filename: string, program: string, ioUtils: AS.IOUtils, loadUtils: AS.LoadUtils, formatIO?: boolean): Promise<string[]>;
/** Main procedure. Parses, evaluates, and converts to str.
 * @param filename File name of the program
 * @param program raw string that encodes a program
 * @returns A string representing the resulting value */
export declare function run(filename: string, program: string, argv: string[], ioUtils: AS.IOUtils, loadUtils: AS.LoadUtils): Promise<number>;
