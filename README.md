# Nexa AI Agents

## Requisitos

- [Python](https://www.python.org/) >=3.10
- [Ollama](https://ollama.com/)

## Instalação

### Criação de um ambiente virtual

#### No Linux ou macOS:
```sh
python -m venv venv
source venv/bin/activate
```

#### No Windows:
```sh
python -m venv venv
.\venv\Scripts\activate
```

### Instalação das dependências

```sh
pip install -r requirements.txt
```

Principais dependências:

- smolagents[litellm,toolkit]
- pydantic
- ollama - para execução dos modelos localmente.
- beautifulsoup4 - para pesquisas na web.
- wikipedia api

RAG (Retrieval-Augmented Generation):

- chromadb - para conexão com o banco de dados vetorial
- sentence-transformers para criar o embeddings para o BD vetorial
- pandas

Servidor web:

- flask
- redis
- pydantic

### Configuração das Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e altere os seus valores.

Os valores recomendados estão definidos no arquivo `.env.example`.

### Configuração do Banco de Dados Vetorial - Sistema RAG

Recomendamos configurá-lo com docker com o seguinte comando:

```sh
docker compose up --build -d
```

Mas, também pode executá-lo diretamente do projeto, executando:

```sh
chroma run --host localhost --port 8000
```

### Popular Banco de Dados com os NCMs

O agente de classificação espera que o banco de dados vetorial armazene os NCMs (Nomenclatura Comum do Mercosul) e EX (excessão) dos produtos. Assim, é necessário popular o BD com alguns dados relacionados ao NCM e EX.

Esses dados podem ser obtidos no site do Comércio Exterior [COMEX](https://comexstat.mdic.gov.br/pt/home). Em seguida, adicione os arquivos à pasta do projeto seguindo as seguintes regras:

- Os arquivos CSV devem ser colocados no diretório `database/data` e serem nomeados: `ncm.csv` e `tipi.csv`.
- Os arquivos devem possuir codificação **UTF-8** e separador **vírgula** (,).
- O arquivo `ncm.csv` deve possuir os seguintes campos **com estes nomes**:
  1. **CO_NCM**: O código NCM
  2. **NO_NCM_POR**: A descrição em português
  3. **NO_NCM_ING**: A descrição em inglês
- O arquivo `tipi.csv` deve possuir os seguintes campos **com estes nomes**:
  1. **NCM**: O código NCM
  2. **EX**: O código EX

Veja mais sobre esses dados em [Algumas informações importantes](#algumas-informações-importantes).

E execute o seguinte comando:

```sh
python database/create.py
```

Esse programa irá criar os embeddings dos dados contidos no arquivo CSV e guardá-los em uma coleção no banco de dados vetorial.

#### Algumas informações importantes

- **Campo de Embedding**: A descrição do NCM em inglês será o campo utilizado para a pesquisa no BD. **Deve ser a coluna 3 do CSV**.
- **Campos retornados**: Após encontrar resultados, o BD irá retornar
  - o código NCM
  - o código EX
  - a descrição do NCM em Português

## Executar

```sh
python run.py
```

### Exemplo de interação direta com um agente

A aplicação invoca os agentes automaticamente, se desejar executar os agentes manualmente, vocẽ pode executar:

```sh
python agent_example.py
```

- rodar docker.
- popular banco de dados vetorial
- testar banco de dados vetorial

### Exemplo de interação direta com o banco de dados

A aplicação utiliza o banco de dados automaticamente, mas se desejar executar requisições contra o BD, você pode executar:

```sh
python databse/query.py
```
