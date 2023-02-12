const { defineConfig } = require('@vue/cli-service')
const CompressionPlugin = require('compression-webpack-plugin')
module.exports = defineConfig({
  lintOnSave: true,
  productionSourceMap: false,
  publicPath: '/myapp/',
  devServer: {
    host: '0.0.0.0',
    port: 8001,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
      'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization'
    }
  },
  configureWebpack: config => {
    if (process.env.NODE_ENV === 'production') {
      return {
        performance: {
          maxEntrypointSize: 512000
        },
        optimization: {
          splitChunks: {
            minSize: 20000,
            maxSize: 500000
          }
        }
      }
    }
  },
  chainWebpack(config) {
    config.plugin('CompressionPlugin').use(CompressionPlugin)
  }
})
