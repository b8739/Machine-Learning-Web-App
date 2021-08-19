const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;
const VuefyLoaderPlugin = require("vuetify-loader/lib/plugin");

module.exports = {
  lintOnSave: false,
  assetsDir: "./static",
  publicPath: "/",
  // 용량 커서
  productionSourceMap: false,
  configureWebpack: {
    // mode: "development",
    // devtool: "eval"
    plugins: [new VuefyLoaderPlugin()]
  }
};
