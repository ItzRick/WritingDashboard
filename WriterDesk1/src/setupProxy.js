const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: '/api',
      pathRewrite: {
        '^/api': '/', // rewrite path
      },
      changeOrigin: true,
      rejectUnauthorized: false,
      secure: false,
    })
  );
};