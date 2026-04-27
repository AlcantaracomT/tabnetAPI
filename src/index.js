const express = require('express');
const cors = require('cors');
const app = express(); 
const apiKeyMiddleware = require('./middlewares/auth');
const sihRoutes = require('./routes/sihRoutes');

app.use(cors());
app.use(express.json());

app.use('/api', apiKeyMiddleware);

app.use('/api/sih', sihRoutes);

app.listen(3000, () => {
  console.log('API rodando');
});