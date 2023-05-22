const path = require('path')

module.exports = {
  entry: './pbhhg_js/src/main.ts',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
  output: {
    filename: 'pbhhg.js',
    path: path.resolve(__dirname, 'pbhhg_js/dist'),
  },
  mode: 'development',
}
