const CHAVE_ADMIN = process.env.CHAVE_AADMIN || "free-key"

const keys = {
  [CHAVE_ADMIN]: { limit: 200, used: 0 },
  "free-key": { limit: 10, used: 0 }
};

function apiKeyMiddleware(req, res, next) {
  const apiKey = req.headers['x-api-key'];

  if (!apiKey || !keys[apiKey]) {
    return res.status(401).json({
      error: 'API key inválida'
    });
  }

  const user = keys[apiKey];

  if (user.used >= user.limit) {
    return res.status(429).json({
      error: 'Limite de requisições atingido'
    });
  }

  user.used++;

  next();
}

module.exports = apiKeyMiddleware;