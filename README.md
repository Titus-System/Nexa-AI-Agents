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

### Instalar as dependências

```sh
pip install -r requirements.txt
```

Principais dependências:

- smolagents[litellm,toolkit]
- pydantic
- ollama - para execução dos modelos localmente.

### Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e altere os seus valores.

Os valores recomendados estão definidos no arquivo `.env.example`.

### Testar com um exemplo

```py
python src/example.py
```
