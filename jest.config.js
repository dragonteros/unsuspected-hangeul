/** @type {import('jest').Config} */
const config = {
  preset: 'ts-jest/presets/js-with-ts-esm',
  testEnvironment: 'node',
  transformIgnorePatterns: ['//node_modules'],
  testRegex: '/test/test_.*\\.ts$',
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  globals: {
    'ts-jest': {
      isolatedModules: true,
    },
  },
  workerThreads: true,
}

module.exports = config
