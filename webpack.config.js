const path = require('path')

module.exports = {
  entry: './pbhhg_js/main.js',
  output: {
    filename: 'pbhhg.js',
    path: path.resolve(__dirname, 'pbhhg_js/dist')
  },
  mode: 'production'
}
