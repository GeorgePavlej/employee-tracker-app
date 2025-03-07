module.exports = {
  devServer: {
    host: '0.0.0.0',
    port: 8080,
    hot: true,
    liveReload: true,
    watchFiles: {
      paths: ['src/**/*'],
      options: {
        usePolling: true,
        interval: 300,
        poll: 300
      }
    },
    client: {
      webSocketURL: 'auto://0.0.0.0:0/ws',
      progress: true,
      overlay: {
        errors: true,
        warnings: false
      }
    },
    proxy: {
      '/employee/auth': {
        target: 'http://backend:8000',
        changeOrigin: true
      },
      '/auth': {
        target: 'http://backend:8000',
        changeOrigin: true
      },
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true
      }
    }
  },
  configureWebpack: {
    devtool: 'source-map',
    watchOptions: {
      poll: 300,
      ignored: /node_modules/
    }
  }
};