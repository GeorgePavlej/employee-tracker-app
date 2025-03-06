module.exports = {
  devServer: {
    host: '0.0.0.0',
    port: 8080,
    hot: true,
    watchFiles: {
      paths: ['src/**/*'],
      options: {
        poll: true
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
  }
};