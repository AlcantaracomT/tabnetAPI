const he = require('he');

function parseTabnet(raw) {
  const clean = raw.replace(/&\s*$/, '').trim();

  const decodedRaw = he.decode(clean);

  const linhas = decodedRaw
    .split('\n')
    .map(l => l.trim())
    .filter(l => l);

  if (linhas.length < 2) return [];

  const headers = linhas[0]
    .split(';')
    .map(h => h.replace(/"/g, '').trim());

  return linhas.slice(1).map(linha => {
    const colunas = linha.split(';');
    const obj = {};

    headers.forEach((h, i) => {
      let valor = colunas[i] || '';
      
      valor = valor.replace(/"/g, '').trim();

      obj[h] = valor;
    });

    return obj;
  });
}

function normalizarMunicipio(obj) {
  const chaveMunicipio = Object.keys(obj).find(k =>
    k.toLowerCase().includes('munic')
  );

  if (!chaveMunicipio) return obj;

  const campo = obj[chaveMunicipio];

  if (!campo) return obj;

  const match = campo.match(/^(\d+)\s+(.*)$/);

  return {
    ...obj,
    municipio_codigo: match ? match[1] : null,
    municipio_nome: match ? match[2] : campo
  };
}

function normalizarCampos(obj) {
  const findKey = (termo) => Object.keys(obj).find(k => 
    k.toLowerCase().includes(termo.toLowerCase())
  );

  const keyAih = findKey('aih');
  const keyInternacoes = findKey('interna');
  const keyValor = findKey('valor total');
  const keyMortalidade = findKey('mortalidade');
  const keyPermanencia = findKey('perman');

  const parseNumber = (val) => {
    if (val === undefined || val === null || val === '-' || val === '') return 0;
    
    if (typeof val === 'number') return val;

    let str = String(val).trim().replace(/\./g, '').replace(',', '.');

    const num = Number(str);
    return isNaN(num) ? 0 : num;
  };

  return {
    municipio_codigo: obj.municipio_codigo,
    municipio_nome: obj.municipio_nome,

    aih_aprovadas: parseNumber(obj[keyAih]),
    internacoes: parseNumber(obj[keyInternacoes]),
    valor_total: parseNumber(obj[keyValor]),

    taxa_mortalidade: parseNumber(obj[keyMortalidade]),
    media_permanencia: parseNumber(obj[keyPermanencia])
  };
}

module.exports = {
  parseTabnet,
  normalizarMunicipio,
  normalizarCampos
};