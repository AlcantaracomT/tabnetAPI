#  TabAPI do DATASUS (SIH)

![Versão](https://img.shields.io/badge/versão-2.0.0-blue)
![Node.js](https://img.shields.io/badge/Node.js-18+-green)
![Express](https://img.shields.io/badge/Express-4.x-lightgrey)
![Status](https://img.shields.io/badge/Status-Em_Produção-success)
![Licença](https://img.shields.io/badge/Licença-MIT-red)

<img src="https://png.pngtree.com/png-vector/20230303/ourmid/pngtree-api-vector-icon-design-illustration-png-image_6628969.png" alt="Texto Alternativo" width="300">

## Sobre o Projeto

A **TabAPI** é uma API RESTful  construída para atuar como uma ponte (proxy) rápida e higienizada para o sistema  **TABNET** do **DATASUS** (Departamento de Informática do Sistema Único de Saúde do Brasil).

Diferente de extrações estáticas, esta API consulta os arquivos `.def` do governo em **tempo real**, realiza um complexo *parsing* (limpeza de HTML entities, tratamento de pontos flutuantes em Reais) e entrega um JSON limpo e padronizado, pronto para consumo em Dashboards e sistemas de Business Intelligence (BI).


### Objetivos

- Democratizar o acesso aos dados financeiros e epidemiológicos do SUS.
- Contornar problemas de *encoding* e formatação legada do sistema Tabnet.
- Fornecer endpoints de *Insights* já calculados (médias ponderadas, rankings).

---

## Status da Base de Dados

| Característica | Status |
|----------------|--------|
| **Estados disponíveis** |  **Todos os 27 estados do Brasil**  |
| **Período dos dados** |  **2008 - Atual** |
|  **Arquitetura** |  Proxy *Real-time* (Sem necessidade de BD) |
| **Infraestrutura planejada** |  Nuvem (em migração) |
| **Otimização** | Cache em Memória (TTL 1 hora) |
| **Escopo Atual** | Produção Hospitalar (SIH/SUS) |
| **Infraestrutura atual** |  Nuvem (Deploy no Render) |

### Métricas Disponíveis por Registro Até o Momento

- AIH Aprovadas e Internações
- Valor Total Gasto (R$)
- Dias e Média de Permanência
- Óbitos e Taxa de Mortalidade

---

## Endpoints Principais

A API responde na rota base `/api/sih/`. Parâmetros aceitos via *Query String*: `uf`, `ano`, `mes`, `limit`.

- `GET /` - Retorna todos os municípios do estado filtrado no período especificado.
- `GET /top` - Retorna um ranking focado em volume de internações (AIHs aprovadas).
- `GET /insights` - **[Destaque]** Retorna arrays separados ranqueando automaticamente municípios com **Maior Custo**, **Maior Mortalidade** e **Maior Permanência**, ignorando dados vazios ou não consolidados.

---

##  Tecnologias Utilizadas
O projeto sofreu uma migração completa de stack (Python -> Node.js) para otimização de requisições assíncronas concorrentes.

- **[Node.js](https://nodejs.org/)** & **[Express](https://expressjs.com/)** - Core da aplicação web e rotas.
- **[Axios](https://axios-http.com/)** - Cliente HTTP para comunicação com os servidores do Governo.
- **[Node-Cache](https://www.npmjs.com/package/node-cache)** - Sistema de cache implementado para evitar timeouts e banimentos de IP do Datasus.
- **[He](https://github.com/mathiasbynens/he)** - Decodificador robusto de HTML Entities legados.
- **Segurança Customizada** - Middleware próprio de `x-api-key` com controle de *Rate Limiting* por nível de usuário.

---

## Pré-requisitos

Para rodar este projeto localmente, você precisará do **Node.js** (v18+) e do **npm** instalados na sua máquina.

---
#### Fonte dos dados
- **Fonte:[ http://tabnet.datasus.gov.br](http://tabnet.datasus.gov.br)** 
---

### 1. Clone o repositório
```bash
git clone https://github.com/AlcantaracomT/tabnetAPI.git
cd tabnetAPI

### 2. Instale as dependências
```bash
npm install
