const axios = require('axios');
const estados = require('../utils/estados');
const { parseTabnet, normalizarMunicipio, normalizarCampos } = require('../utils/parser');
const { cache, gerarChave } = require('../utils/cache');

const client = axios.create({
  timeout: 60000,
  headers: { 'User-Agent': 'Mozilla/5.0' }
});

function gerarArquivo(uf, ano, mes) {
  const base = estados[uf];
  if (!base) throw new Error(`UF inválida: ${uf}`);

  const aa = String(ano).slice(-2);
  const mm = String(mes).padStart(2, '0');

  return `${base}${aa}${mm}.dbf`;
}


async function consultarSIH({ uf, ano, mes }) {
  const hoje = new Date();
  const anoAtual = hoje.getFullYear();
  const mesAtual = hoje.getMonth();

  if (ano > anoAtual || (ano === anoAtual && mes >= mesAtual)) {
    console.log('RECUSADO: Tentativa de busca no futuro ou mês não consolidado.');
    return {
      uf, ano, mes, total: 0, dados: [],
      aviso: "Dados ainda não disponibilizados pelo Ministério da Saúde para este período."
    };
  }
  const key = gerarChave({ uf, ano, mes });


  if (cache.has(key)) {
    console.log('CACHE HIT');
    return cache.get(key);
  }

  console.log('BUSCANDO...');

  const base = estados[uf];
  if (!base) throw new Error('UF não suportada');

  const rota = `sih/cnv/${base}.def`;
  const arquivo = gerarArquivo(uf, ano, mes);
  const url = `http://tabnet.datasus.gov.br/cgi/tabcgi.exe?${rota}`;

  const body = `
  Linha=Munic%EDpio_gestor
  &Coluna=--N%E3o-Ativa--
  &Incremento=AIH_aprovadas
  &Incremento=Interna%E7%F5es
  &Incremento=Valor_total
  &Incremento=Valor_servi%E7os_hospitalares
  &Incremento=Val_serv_hosp_-_compl_federal
  &Incremento=Val_serv_hosp_-_compl_gestor
  &Incremento=Valor_servi%E7os_profissionais
  &Incremento=Val_serv_prof_-_compl_federal
  &Incremento=Val_serv_prof_-_compl_gestor
  &Incremento=Valor_m%E9dio_AIH
  &Incremento=Valor_m%E9dio_intern
  &Incremento=Dias_perman%EAncia
  &Incremento=M%E9dia_perman%EAncia
  &Incremento=%D3bitos
  &Incremento=Taxa_mortalidade
  &Arquivos=${arquivo}
  &SMunic%EDpio_gestor=TODAS_AS_CATEGORIAS__
  &formato=prn
  &mostre=Mostra
  `.replace(/\n/g, '').replace(/\s+/g, '');

  const response = await client.post(url, body, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });

  const match = response.data.match(/<PRE>([\s\S]*?)<\/PRE>/i);

  if (!match) {
    if (response.data.toLowerCase().includes('inexistente') || response.data.toLowerCase().includes('não encontrado')) {
      console.log('ARQUIVO NÃO ENCONTRADO NO DATASUS PARA ESTE MÊS');
      return {
        uf, ano, mes, total: 0, dados: [],
        aviso: "O Datasus ainda não processou o arquivo deste estado/mês específico."
      };
    }

    console.log(' RESPOSTA DATASUS NÃO RECONHECIDA:\n', response.data.substring(0, 500));
    throw new Error('Erro ao obter dados do Datasus. O servidor deles pode estar instável.');
  }

  const dadosBrutos = parseTabnet(match[1]).map(normalizarMunicipio).map(normalizarCampos);

  const dadosLimpos = dadosBrutos.filter(d =>
    d.municipio_codigo &&
    d.municipio_nome &&
    d.municipio_nome !== 'Total'
  );

  const resultado = {
    uf,
    ano,
    mes,
    total: dadosLimpos.length,
    dados: dadosLimpos
  };

  cache.set(key, resultado);

  return resultado;
}

module.exports = { consultarSIH };