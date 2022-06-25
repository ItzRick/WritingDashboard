const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'https://backend-lv2fs4hn6a-ew.a.run.app',
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