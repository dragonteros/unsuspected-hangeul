/* IO & Load utilities for Node.js */
const readlineSync = require('readline-sync')
const fs = require('fs')
const path = require('path')

const pbhhg = require('./dist/pbhhg')

const nodejsIO = {
  input: () => readlineSync.question(''),
  print: console.log
}

const nodejsLoad = {
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

if (require.main === module) {
  console.log('[Unsuspected Hangeul Interpreter shell. Quit with Ctrl-C.]')
  readlineSync.promptLoop(function (program) {
    let result = pbhhg.main(program, nodejsIO, nodejsLoad)
    if (result.length > 1) {
      console.log('[!] Warning: Interpreted ' + result.length + ' objects in 1 line.')
    }
    console.log(result.join(' '))
  })
}

module.exports = {
  ioUtils: nodejsIO,
  loadUtils: nodejsLoad,
}