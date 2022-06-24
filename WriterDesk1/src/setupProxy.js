const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'https://localhost:5000',
      pathRewrite: {
        '^/api': '/', // rewrite path
      },
      changeOrigin: true,
      // remove lines below when we have a proper SSL cert
      rejectUnauthorized: false,
      secure: false,
    })
  );
};