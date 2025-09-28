# Nexa AI Agents

## Requisitos

- [Python](https://www.python.org/) >=3.10
- [Ollama](https://ollama.com/)

## Instalação

### Criação de um ambiente virtual

```sh
python -m venv venv

. venv/bin/activate
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

Servidor web:

- flask
- redis
- pydantic

### Configuração das Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e altere os seus valores.

Os valores recomendados estão definidos no arquivo `.env.example`.

## Executar

```sh
python run.py
```

## Exemplo de interação direta com um agente

A aplicação invoca o agente automaticamente, mas caso queira executar apenas um agente de forma direta, basta executar:

```py
python agent_example.py
```
