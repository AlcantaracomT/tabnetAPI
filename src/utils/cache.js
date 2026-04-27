const NodeCache = require('node-cache');

const cache = new NodeCache({
  stdTTL: 3600, 
  checkperiod: 120
});

function gerarChave(params) {
  return JSON.stringify(params);
}

module.exports = { cache, gerarChave };