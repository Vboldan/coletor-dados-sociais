# Coletor de Dados Sociais - Morena Dados 📋

Uma solução Full-Stack desenvolvida para coleta, validação e estruturação de dados demográficos e opiniões cidadãs sobre serviços públicos em Campo Grande (MS). O sistema gera bases em formato CSV preparadas para análise em Power BI e Excel.

## ⚖️ Validação Regulatória e Regras de Negócio

O sistema aplica em tempo real as diretrizes da legislação brasileira (Constituição Federal e LDB):
* **Proteção ao Trabalho Infantil (Art. 7º, XXXIII - CF):** Para menores de 14 anos, o campo "Profissão" é desabilitado e preenchido automaticamente como "Não se aplica".
* **Educação Básica (LDB - Lei nº 9.394/1996):** Para crianças abaixo de 4 anos (faixa de creche facultativa), o campo "Escolaridade" tem o preenchimento dispensado.

## 🚀 Funcionalidades

- **Auto-preenchimento de Bairro por CEP:** Integração com a API do ViaCEP para preenchimento dinâmico de localização.
- **Formulário Responsivo:** Interface limpa em *Card Design* otimizada para computadores e dispositivos móveis.
- **Persistência de Dados:** API em Python (FastAPI) que consolida as respostas diretamente em um banco `.csv` estruturado em UTF-8.

## 🛠️ Tecnologias Utilizadas

- **Back-end:** Python 3, FastAPI, Uvicorn, Python-Multipart
- **Front-end:** HTML5, CSS3, JavaScript (Fetch API)
- **APIs Externas:** ViaCEP

## ⚙️ Como Executar o Projeto

1. **Ativar o Ambiente Virtual:**
   ```bash
   source env_ibge/bin/activate
