const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')

module.exports = defineConfig({
  configureWebpack: (config) => {
    // Polyfills to get the `fernet` module to work in the
    // Renderer (Browser-Mode)
    const fallback = config.resolve.fallback || {}
    Object.assign(fallback, {
      crypto: require.resolve('crypto-browserify'),
      stream: require.resolve('stream-browserify')
    })
    config.resolve.fallback = fallback

    config.plugins.push(
      new webpack.ProvidePlugin({
        process: 'process/browser',
        Buffer: ['buffer', 'Buffer']
      })
    )
  },
  // chainWebpack: (config) => {},
  pluginOptions: {
    electronBuilder: {
      // chainWebpackMainProcess: (config) => {
      //   config.module
      //     .rule('style')
      //     .test(/\.(sass|scss|css)$/)
      //     .use(['style-loader', 'css-loader', 'sass-loader'])
      //     .loader(['style-loader', 'css-loader', 'sass-loader'])
      //     .end()
      // },
      // chainWebpackRendererProcess: (config) => {
      // },
      preload: 'src/main/preload.js',
      mainProcessFile: 'src/main/main.js',
      rendererProcessFile: 'src/renderer/main.js',
      nodeIntegration: false,
      builderOptions: {
        // options here will be merged with default electron-builder options
        // https://www.electron.build/configuration/configuration
      }
    }
  },
  transpileDependencies: [
    'vuetify'
  ]
})
