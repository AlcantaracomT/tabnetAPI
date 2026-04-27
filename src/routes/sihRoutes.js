const express = require('express');
const router = express.Router();
const { consultarSIH } = require('../services/tabnetService');

router.get('/', async (req, res) => {
  const { uf = 'CE', ano = 2025, mes = 1 } = req.query;

  try {
    const resultado = await consultarSIH({
      uf: uf.toUpperCase(),
      ano: Number(ano),
      mes: Number(mes)
    });

    res.json({
      success: true,
      ...resultado
    });

  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});


router.get('/top', async (req, res) => {
  const { uf = 'CE', ano = 2025, mes = 1, limit = 10 } = req.query;

  try {
    const resultado = await consultarSIH({ uf, ano, mes });

    const top = resultado.dados.sort((a, b) => b.aih_aprovadas - a.aih_aprovadas).slice(0, limit);

    res.json(top);

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/insights', async (req, res) => {
  const { uf = 'CE', ano = 2025, mes = 1, limit = 10 } = req.query;

  try {
    const resultado = await consultarSIH({
      uf: uf.toUpperCase(),
      ano: Number(ano),
      mes: Number(mes)
    });

    
    const dados = resultado.dados || [];

    if (!dados.length) {
      return res.json({
        success: true,
        insights: {
          maior_mortalidade: [],
          maior_custo: [],
          maior_permanencia: []
        },
        aviso: 'Sem dados disponíveis'
      });
    }

    const top = (campo) =>
      dados
        .filter(d => typeof d[campo] === 'number' && d[campo] > 0) 
        .sort((a, b) => b[campo] - a[campo])
        .slice(0, limit);

    res.json({
      success: true,
      insights: {
        maior_mortalidade: top('taxa_mortalidade'),
        maior_custo: top('valor_total'),
        maior_permanencia: top('media_permanencia')
      }
    });

  } catch (error) {
    console.error('Erro insights:', error.message);

    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router;