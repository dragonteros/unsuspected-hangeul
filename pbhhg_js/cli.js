/* IO & Load utilities for Node.js */
const fs = require('fs')
const path = require('path')
const readline = require('node:readline')

const pbhhg = require('./dist/pbhhg')

const nodeLoadUtils = {
  load(location) {
    return fs.readFileSync(location, 'utf8')
  },
  isFile(location) {
    return fs.statSync(location).isFile()
  },
  listdir: fs.readdirSync,
  joinPath: path.join,
  normalizePath: path.normalize,
}

function interactiveSession() {
  console.log('[평범한 한글 해석기. 종료하려면 Ctrl-D를 누르세요.]')

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: '> ',
  })

  const nodeIOUtils = {
    input: () => {
      return new Promise((resolve, reject) => {
        rl.question('', resolve)
      })
    },
    print: console.log,
  }

  rl.prompt()
  rl.on('line', async (program) => {
    const result = await pbhhg.main(
      '<command-line>',
      program,
      nodeIOUtils,
      nodeLoadUtils
    )
    if (result.length > 1) {
      console.warn(
        `[!] 주의: 한 줄에 ${result.length}개의 객체를 해석했습니다.`
      )
    }
    console.log(result.join(' '))
    rl.prompt()
  })
  // .on('close', () => {
  //   console.log('Have a great day!')
  //   process.exit(0)
  // })
}

if (require.main === module) {
  interactiveSession()
}

module.exports = {
  loadUtils: nodeLoadUtils,
}
