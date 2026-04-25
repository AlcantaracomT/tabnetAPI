#  TabAPI do DATASUS

![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue)
![Licença](https://img.shields.io/badge/Licença-MIT-red)

<img src="https://png.pngtree.com/png-vector/20230303/ourmid/pngtree-api-vector-icon-design-illustration-png-image_6628969.png" alt="Texto Alternativo" width="300">

## Sobre o Projeto

A **TabAPI** é uma API RESTful desenvolvida para fornecer acesso a dados extraídos do sistema  **TABNET** do **DATASUS** (Departamento de Informática do Sistema Único de Saúde do Brasil).

Esta API permite consultas aos dados, facilitando análises estatísticas, pesquisas acadêmicas e desenvolvimento de aplicações na área da saúde.

### Objetivos

- Permitir integração com sistemas de análise de dados e BI
- Facilitar pesquisas na área da saúde pública

---

## Status da Base de Dados

| Característica | Status |
|----------------|--------|
| **Estados disponíveis** |  Bahia (BA) |
| **Período dos dados** |  2008 - Atual |
| **Infraestrutura atual** |  Servidor local |
| **Infraestrutura planejada** |  Nuvem (em migração) |
| **Indicadores disponíveis** | 14+ métricas hospitalares |
| **Próximas atualizações** |  Expansão para outros estados |

### Métricas Disponíveis por Registro Até o Momento

- AIH aprovadas
- Internações
- Valor total
- Valor de serviços hospitalares
- Valor médio de internação
- Dias de permanência
- Média de permanência
- Óbitos
- Taxa de mortalidade

---

##  Tecnologias Utilizadas

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** (v0.115.6) - Framework web assíncrono de alto desempenho
- **[Uvicorn](https://www.uvicorn.org/)** (v0.34.0) - Servidor ASGI
- **[Psycopg2](https://www.psycopg.org/)** (v2.9.10) - Adaptador PostgreSQL
- **[Python-dotenv](https://github.com/theskumar/python-dotenv)** (v1.0.1) - Gerenciamento de variáveis de ambiente

### Banco de Dados
- **PostgreSQL** - Sistema de gerenciamento de banco de dados relacional
- **Connection Pool** - Otimização de conexões simultâneas

### Segurança
- **API Key Authentication** - Chave secreta para todas as rotas
- **CORS** - Configuração para origens específicas

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python** 3.8 ou superior
- **PostgreSQL** 13 ou superior
- **pip** (gerenciador de pacotes Python)
- **Git** (para clonar o repositório)

---
#### Fonte dos dados
- **Fonte:[ http://tabnet.datasus.gov.br](http://tabnet.datasus.gov.br)** 
---


## Instalação e Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/tabapi.git
cd tabapi```

---
