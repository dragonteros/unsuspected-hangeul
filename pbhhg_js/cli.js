/* CLI for Node.js */
import * as url from 'node:url'

import * as pbhhg from './dist/main.module.js'
import { BufferedReader, BufferedWriter, getLoadUtils } from './node.js'

async function interactiveSession() {
  console.log('[평범한 한글 해석기. 종료하려면 Ctrl-C를 누르세요.]')

  const stdin = new BufferedReader()
  const stdout = new BufferedWriter()
  const ioUtils = {
    input: () => stdin.readLine(),
    print: (s) => stdout.writeLine(s),
  }
  const loadUtils = getLoadUtils(stdin, stdout)

  while (true) {
    process.stdout.write('> ')
    const program = await stdin.readLine()
    if (program == null) return

    const result = await pbhhg.main(
      '<command-line>',
      program,
      ioUtils,
      loadUtils
    )
    if (result.length > 1) {
      console.warn(
        `[!] 주의: 한 줄에 ${result.length}개의 객체를 해석했습니다.`
      )
    }
    console.log(result.join(' '))
  }
}

async function run(filename, program, argv) {
  const stdin = new BufferedReader()
  const stdout = new BufferedWriter()
  const ioUtils = {
    input: () => stdin.readLine(),
    print: (s) => stdout.writeLine(s),
  }
  const loadUtils = getLoadUtils(stdin, stdout)

  const exitCode = await pbhhg.run(filename, program, argv, ioUtils, loadUtils)
  process.exit(exitCode)
}

if (import.meta.url.startsWith('file:')) {
  const modulePath = url.fileURLToPath(import.meta.url)
  if (process.argv[1] === modulePath) {
    const USAGE = `난해한 프로그래밍 언어 '평범한 한글'의 해석기입니다.
  
  사용법
    node ${process.argv[1]} [-h | <파일> [<인수> ...] | -c <본문> [<인수> ...]]
  
  사용례
    node ${process.argv[1]} -h
    node ${process.argv[1]} --help
      사용법을 안내합니다.
  
    node ${process.argv[1]} <파일>
    node ${process.argv[1]} <파일> <인수0>
    node ${process.argv[1]} <파일> <인수0> <인수1>
    ...
      <파일>에 있는 '평범한 한글' 함수 모듈을 제공한 인수와 함께 실행합니다.
      실행 결과는 종료 코드가 됩니다.
  
    node ${process.argv[1]} -c <본문>
    node ${process.argv[1]} -c <본문> <인수0>
    node ${process.argv[1]} -c <본문> <인수0> <인수1>
    ...
      '평범한 한글' 함수 <본문>을 제공한 인수와 함께 실행합니다.
      실행 결과는 종료 코드가 됩니다.`

    const argv = process.argv.slice(2)
    if (argv.length === 0) {
      interactiveSession()
    } else if (argv[0] === '-h' || argv[0] === '--help') {
      console.log(USAGE)
    } else if (argv[0] === '-c') {
      if (argv.length === 1) {
        console.error(
          `다음 명령으로 사용법을 확인하십시오.\n  node ${process.argv[1]} --help`
        )
        process.exit(1)
      }
      run('<command>', argv[1], argv.slice(2))
    } else {
      let fd = argv[0]
      if (fd === '-') fd = 0
      const program = fs.readFileSync(fd, { encoding: 'utf-8' })
      run(argv[0], program, argv.slice(1))
    }
  }
}
