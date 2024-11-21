const path = require('path');

module.exports = function override(config) {
  config.resolve.alias = {
    ...config.resolve.alias,
    '@styles': path.resolve(__dirname, 'src/styles'),
  };
  return config;
};

