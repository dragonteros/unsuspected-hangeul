import { parseNumber } from 'parse'
import * as AS from './abstractSyntax.js'

export class UnsuspectedHangeulBuiltinError extends AS.UnsuspectedHangeulError {
  constructor(metadata, message, codes) {
    const _codes = [parseNumber('ㅂ'), ...codes]
    const argv = _codes.map((code) => AS.IntegerV(code))
    const err = AS.ErrorV([metadata], message, argv)
    super(err)
  }
}

export class UnsuspectedHangeulOSError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata, message) {
    const code = parseNumber('ㅈㅈ') // 체제
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulArithmeticError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata, message) {
    const code = parseNumber('ㅅㅅ') // 산술
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulTypeError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata, message) {
    const code = parseNumber('ㄱ') // 꼴
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulValueError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata, message) {
    const code = parseNumber('ㅈㅁ') // 잘못
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulDivisionError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata, message) {
    const code = parseNumber('ㄴㄴ') // 나누기
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulNotFoundError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata, message) {
    const code = parseNumber('ㅁㅈ') // 못찾
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulImportError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata, message) {
    const code = parseNumber('ㅂ') // 불러오기
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulOutOfRangeError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata, message) {
    const code = parseNumber('ㅂㄱ') // 바깥
    super(metadata, message, [code])
  }
}

export class UnsuspectedHangeulKeyboardInterruptError extends UnsuspectedHangeulBuiltinError {
  constructor(metadata, message) {
    const code = parseNumber('ㅈㄷ') // 중단
    super(metadata, message, [code])
  }
}
