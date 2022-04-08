const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;
const VuefyLoaderPlugin = require("vuetify-loader/lib/plugin");

module.exports = {
  lintOnSave: false,
  assetsDir: "./static",
  publicPath: "/",
  // devServer: {
  //   port: 80,
  //   host: "0.0.0.0"
  // },
  // 용량 커서
  productionSourceMap: false,
  configureWebpack: config => {
    // mode: "development",
    // devtool: "eval"
    config.output.filename = "js/[name].[hash].js";
    config.output.chunkFilename = "js/[name].[hash].js";
  },
  configureWebpack: {
    // plugins: [new BundleAnalyzerPlugin(), new VuefyLoaderPlugin()]
    plugins: [new VuefyLoaderPlugin()]
  }
};
