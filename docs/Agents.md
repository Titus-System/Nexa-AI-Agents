# Nexa-AI-Agents

Comportamento dos agentes
---

## 1. Visão geral

O Nexa-Ai-Agents é composto por 4 agentes:

- **Agente gerente:** `manager_agent`
- **Agente web:** `web_search_agent`
- **Agente de descrição:** `description_writer_agent`
- **Agente de classificação:** `classification_writer_agent`

Todos os agentes utilizam o modelo de IA **qwen2.5:14b** 

---

## 2. Agentes

---

### 2.1 Agente gerente

Ele é responsavel por receber o partnumber e gerenciar a chamada dos demais agentes.

#### 2.1.1 Funcionamento

Recebe um `system prompt` passando o partnumber, suas instruções e como se comunicar com os outros agentes. Os agentes sao chamados da seguinte ordem:

- 1º Chama o `web_search_agent` para buscar os dados tecnicos do produto na web.
- 2º Chama o `description_writer_agent` que gera uma descrição humanizada dos dados tecnicos.
- 3º Chama o `classification_writer_agent` que classifica o NCM desse produto.

---

### 2.1 Agente web

Ele é responsavel por procurar os dados tecnicos do partnumber na web.

#### 2.1.1 Funcionamento

É acionado pelo `manager_agent`, recebendo um `system prompt` passando as intruções do que fazer, juntamente com o partnumber e os dados conhecidos sobre ele, como: fabricante etc. Entao o agente começa a procurar na web o site do fabricante e as especificações tecnicas do produto.

```json
{
  "part_number": "LM317T",
  "supplier": "TechCorp",
  "additional_context": ""
}
```

#### 2.1.2 Ferramentas do agente

- **visit_page:** permite ao agente acessar paginas na web.

- **duckduckgo:** permite ao agente fazer buscas na web usando o motor de busca do `DuckDuckGo`. 

- **wikipedia:** permite buscar e extrair informações diretamente da Wikipedia. 

- **PythonInterpreterTool(bs4, lxml):** permite que o agente execute código Python para processar ou analisar dados diretamente durante a execução.

---

### 2.1 Agente de descrição

Ele é responsavel por gerar uma descrição humanizada do produto, usando os dados tecnicos como base.

#### 2.1.1 Funcionamento

É acionado pelo `manager_agent`, recebendo um `system prompt` passando as intruções do que fazer, juntamente com o partnumber e os dados tecnicos encontrados pelo agente web.

```json
{
  "part_number": "LM317T",
  "supplier": "TechCorp",
  "technical_data": {
    "weight": "100g",
    "material": "plastic",
    "voltage": "5V"
  },
  "additional_context": ""
}
```

---

### 2.1 Agente de descrição

**CONTINUAR...**