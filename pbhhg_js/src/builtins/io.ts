import * as AS from '../abstractSyntax'
import * as E from '../error'
import { encodeNumber } from '../parse'
import {
  checkArity,
  checkMaxArity,
  checkMinArity,
  checkType,
  recursiveMap,
} from '../utils'

const MODE_TABLE = {
  ㄹ: 'r',
  ㅈㄹ: 'w',
  ㅈㄱ: 'a',
  ㄹㅈㄹ: 'r+',
  ㅈㄹㄹ: 'w+',
  ㅈㄱㄹ: 'a+',
} as const

class FileV extends AS.FunctionV {
  constructor(private file: AS.File) {
    super('파일 접근 ')
  }
  execute(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ): AS.Value {
    checkMinArity(metadata, argv, 1)
    const [command] = checkType(
      metadata,
      argv.slice(-1).map((x) => context.strict(x)),
      [AS.IntegerV]
    )
    const commandStr = encodeNumber(command.value)
    if (commandStr === 'ㄷ') {
      return this.close(context, metadata, argv)
    } else if (commandStr === 'ㄹ') {
      return this.read(context, metadata, argv)
    } else if (commandStr === 'ㅈㄹ') {
      return this.write(context, metadata, argv)
    } else if (commandStr === 'ㅈ') {
      return this.seekOrTell(context, metadata, argv)
    } else if (commandStr === 'ㄱ') {
      return this.truncate(context, metadata, argv)
    } else {
      throw new E.UnsuspectedHangeulValueError(
        metadata,
        `${commandStr}은 파일 객체가 인식하지 못하는 명령입니다.`
      )
    }
  }
  private close(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ): AS.Value {
    checkArity(metadata, argv, 1)
    return new AS.IOV('FileV::close', [this], async (doIO, ioUtils) => {
      try {
        this.file.close()
        return new AS.NilV()
      } catch (error) {
        throw new E.UnsuspectedHangeulOSError(
          metadata,
          `파일 닫기에 실패하였습니다: ${error}`
        )
      }
    })
  }
  private read(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ): AS.Value {
    checkArity(metadata, argv, 2)
    const [count] = checkType(
      metadata,
      [context.strict(argv[0])],
      [AS.IntegerV]
    )
    return new AS.IOV('FileV::read', [this, count], async (doIO, ioUtils) => {
      try {
        const content = await this.file.read(Number(count.value))
        return new AS.BytesV(content)
      } catch (error) {
        throw new E.UnsuspectedHangeulOSError(
          metadata,
          `파일 읽기에 실패하였습니다: ${error}`
        )
      }
    })
  }
  private write(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ): AS.Value {
    checkArity(metadata, argv, 2)
    const [content] = checkType(
      metadata,
      [context.strict(argv[0])],
      [AS.BytesV]
    )
    return new AS.IOV(
      'FileV::write',
      [this, content],
      async (doIO, ioUtils) => {
        try {
          const count = this.file.write(content.value)
          return new AS.IntegerV(BigInt(count))
        } catch (error) {
          throw new E.UnsuspectedHangeulOSError(
            metadata,
            `파일 쓰기에 실패하였습니다: ${error}`
          )
        }
      }
    )
  }
  private seekOrTell(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ): AS.Value {
    checkMaxArity(metadata, argv, 3)
    const _argv = argv.map((x) => context.strict(x))
    if (argv.length === 1) {
      return new AS.IOV('FileV::seekOrTell', [this], async (doIO, ioUtils) => {
        try {
          return new AS.IntegerV(BigInt(this.file.tell()))
        } catch (error) {
          throw new E.UnsuspectedHangeulOSError(
            metadata,
            `파일의 어디를 읽고 있는지 알아내는 데 실패하였습니다: ${error}`
          )
        }
      })
    }

    let whence: 'SEEK_SET' | 'SEEK_CUR' = 'SEEK_SET'
    let offset: AS.IntegerV
    if (argv.length === 2) {
      ;[offset] = checkType(metadata, [_argv[0]], [AS.IntegerV])
    } else {
      ;[offset] = checkType(metadata, [_argv[1]], [AS.IntegerV])
      let [_whence] = checkType(metadata, [_argv[0]], [AS.IntegerV])
      switch (encodeNumber(_whence.value)) {
        case 'ㅅㅈㅂㄷ':
          whence = 'SEEK_SET'
          break
        case 'ㅈㄱㅂㄷ':
          whence = 'SEEK_CUR'
          break
        default:
          throw new E.UnsuspectedHangeulValueError(
            metadata,
            `파일 객체의 ㅈ 명령에 주는 위치 인수로 ${_whence.value}은 적절하지 않습니다.`
          )
      }
    }
    return new AS.IOV(
      'FileV::seekOrTell',
      [this, ..._argv.slice(0, -1)],
      async (doIO, ioUtils) => {
        try {
          const pos = this.file.seek(Number(offset.value), whence)
          return new AS.IntegerV(BigInt(pos))
        } catch (error) {
          throw new E.UnsuspectedHangeulOSError(
            metadata,
            `파일의 읽는 위치를 수정하는 데 실패하였습니다: ${error}`
          )
        }
      }
    )
  }
  private truncate(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ): AS.Value {
    checkMaxArity(metadata, argv, 2)
    const _argv = checkType(
      metadata,
      argv.map((x) => context.strict(x)),
      [AS.IntegerV]
    )
    const size = _argv.length > 1 ? Number(_argv[0].value) : undefined
    return new AS.IOV(
      'FileV::truncate',
      [this, ..._argv.slice(0, -1)],
      async (doIO, ioUtils) => {
        try {
          const newSize = this.file.truncate(size)
          return new AS.IntegerV(BigInt(newSize))
        } catch (error) {
          throw new E.UnsuspectedHangeulOSError(
            metadata,
            `파일 크기를 재조정하는 데 실패하였습니다: ${error}`
          )
        }
      }
    )
  }
}

function _input(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  argv: AS.Value[]
) {
  checkArity(metadata, argv, 0)
  return new AS.IOV('ㄹ', argv, async function (doIO, ioUtils) {
    const input = await ioUtils.input()
    return input == null ? new AS.NilV() : new AS.StringV(input)
  })
}
function _print(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  argv: AS.Value[]
) {
  checkArity(metadata, argv, 1)
  const _argv = checkType(
    metadata,
    argv.map((x) => context.strict(x)),
    [AS.StringV]
  )
  return new AS.IOV('ㅈㄹ', _argv, async function (doIO, ioUtils) {
    ioUtils.print(_argv[0].str)
    return new AS.NilV()
  })
}
function _return(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  argv: AS.Value[]
) {
  checkArity(metadata, argv, 1)
  const arg = recursiveMap(argv[0], (x) => context.strict(x))
  return new AS.IOV('ㄱㅅ', [arg], async function (doIO, ioUtils) {
    return arg
  })
}
function _bind(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  argv: AS.Value[]
) {
  checkArity(metadata, argv, [2, 3])
  const [ioToBind] = checkType(metadata, [context.strict(argv[0])], [AS.IOV])
  return new AS.IOV('ㄱㄹ', argv, async function (doIO, ioUtils) {
    let arg: AS.NonIOStrictValue
    try {
      arg = await doIO(ioToBind)
    } catch (error) {
      if (error instanceof AS.UnsuspectedHangeulError) {
        if (argv.length < 3) throw error
        const result = context.procFunctional(metadata, argv[2])(
          context,
          metadata,
          [error.err]
        )
        const [_result] = checkType(
          metadata,
          [context.strict(result)],
          [AS.IOV]
        )
        return _result
      }
      throw error
    }
    const result = context.procFunctional(metadata, argv[1])(
      context,
      metadata,
      [arg]
    )
    const [_result] = checkType(metadata, [context.strict(result)], [AS.IOV])

    return _result
  })
}
function _file(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  argv: AS.Value[]
) {
  checkArity(metadata, argv, 2)
  const [path] = checkType(
    metadata,
    [context.strict(argv[0])],
    [AS.IntegerV, AS.StringV]
  )
  const _path = path instanceof AS.IntegerV ? Number(path.value) : path.str

  const [mode] = checkType(metadata, [context.strict(argv[1])], [AS.IntegerV])
  const modeStr = encodeNumber(mode.value)
  if (!(modeStr in MODE_TABLE)) {
    throw new E.UnsuspectedHangeulValueError(
      metadata,
      `${modeStr}은 기본 제공 함수 ㄱㄴ이 이해하는 파일 열기 방식이 아닙니다.`
    )
  }
  const _mode = MODE_TABLE[modeStr as keyof typeof MODE_TABLE]
  return new AS.IOV('ㄱㄴ', [path, mode], async function (doIO, ioUtils) {
    try {
      return new FileV(context.loadUtils.open(_path, _mode))
    } catch (error) {
      throw new E.UnsuspectedHangeulOSError(
        metadata,
        `파일 열기에 실패하였습니다: ${error}`
      )
    }
  })
}

export default {
  ㄹ: _input,
  ㅈㄹ: _print,
  ㄱㅅ: _return,
  ㄱㄹ: _bind,
  ㄱㄴ: _file,
}
