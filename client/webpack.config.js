module.exports = {
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: "ify-loader"
      }
    ]
  },
  externals: {
    plotly: "plotly"
  }
};
