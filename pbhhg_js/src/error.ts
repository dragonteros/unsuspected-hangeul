import * as AS from './abstractSyntax'
import { parseNumber } from './parse'

export class UnsuspectedHangeulBuiltinError extends AS.UnsuspectedHangeulError {
  constructor(metadata: AS.Metadata, message: string, codes: bigint[]) {
    const _codes = [parseNumber('ㅂ'), ...codes]
    const argv = _codes.map((code) => new AS.IntegerV(code))
    const err = new AS.ErrorV([metadata], message, argv)
    super(err)
  }
}

export class UnsuspectedHangeulOSError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata: AS.Metadata, message: string) {
    const code = parseNumber('ㅈㅈ') // 체제
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulArithmeticError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata: AS.Metadata, message: string) {
    const code = parseNumber('ㅅㅅ') // 산술
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulSyntaxError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata: AS.Metadata, message: string) {
    const code = parseNumber('ㅁㅂ') // 문법
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulTypeError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata: AS.Metadata, message: string) {
    const code = parseNumber('ㄱ') // 꼴
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulValueError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata: AS.Metadata, message: string) {
    const code = parseNumber('ㅈㅁ') // 잘못
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulDivisionError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata: AS.Metadata, message: string) {
    const code = parseNumber('ㄴㄴ') // 나누기
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulNotFoundError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata: AS.Metadata, message: string) {
    const code = parseNumber('ㅁㅈ') // 못찾
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulImportError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata: AS.Metadata, message: string) {
    const code = parseNumber('ㅂ') // 불러오기
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulOutOfRangeError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata: AS.Metadata, message: string) {
    const code = parseNumber('ㅂㄱ') // 바깥
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulKeyboardInterruptError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata: AS.Metadata, message: string) {
    const code = parseNumber('ㅈㄷ') // 중단
    super(metadata, message, [code])
  }
}
