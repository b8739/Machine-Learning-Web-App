module.exports = {
  lintOnSave: false,
  assetsDir: "./static",
  publicPath: "/",
  // 용량 커서
  productionSourceMap: false,
  configureWebpack: {
    mode: "production",
    devtool: "eval"
  }
};
