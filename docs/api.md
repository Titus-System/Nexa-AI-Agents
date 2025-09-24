# Documentação da API – Nexa-AI-Agents

## Visão Geral

O Nexa-AI-Agents é um microsserviço responsável por processar requisições de classificação de part numbers, fornecendo feedback de progresso em tempo real via Redis Pub/Sub. Ele expõe uma rota HTTP para submissão de jobs e utiliza canais Redis para reportar o andamento e o resultado do processamento.

- **Ambiente:** Todos os serviços rodam na mesma máquina.
- **API Gateway:** Comunica-se com este serviço via HTTP e Redis, rodando em Docker.
- **Redis:** Rodando em Docker, acessível via `localhost`.
- **Nexa-AI-Agents:** Não roda em Docker, executa diretamente no host.

---

## Endpoints

### 1. Submeter Classificação de Part Number

- **URL:** `/process/single_partnumber`
- **Método:** `POST`
- **Content-Type:** `application/json`
- **Descrição:** Inicia o processamento de classificação de um part number. O progresso e o resultado são enviados via canal Redis informado no payload.

#### Payload de Requisição

```json
{
  "progress_channel": "nome_do_canal_redis",
  "partnumber": "12345-XYZ",
  "description": "Descrição opcional do item",
  "manufacturer": "Fabricante opcional",
  "supplier": "Fornecedor opcional"
}
```

- **progress_channel** (string, obrigatório): Nome do canal Redis para receber atualizações.
- **partnumber** (string, obrigatório): Código do part number a ser classificado.
- **description** (string, opcional): Descrição do item.
- **manufacturer** (string, opcional): Fabricante.
- **supplier** (string, opcional): Fornecedor.

#### Resposta

- **Status 202 Accepted**

```json
{
  "job_id": "job-<uuid>"
}
```

- **Status 400 Bad Request** (payload inválido)

```json
{
  "error": "payload inválido"
}
```

---

## Comunicação de Progresso e Resultado

O progresso e o resultado do processamento são enviados via Redis Pub/Sub no canal especificado em `progress_channel`.

### 1. Atualização de Progresso

```json
{
  "status": "processing",
  "job_id": "job-ajgldfgsaerg",
  "progress": {
    "current": 1,
    "total": 3,
    "message": "Analisando dados no servidor Nexa-IA"
  }
}
```

- **status:** Sempre `"processing"` durante o processamento.
- **progress.current:** Etapa atual (int).
- **progress.total:** Total de etapas (int).
- **progress.message:** Mensagem descritiva (string).

### 2. Resultado Final

```json
{
  "status": "done",
  "job_id": "job-ajgldfgsaerg",
  "result": {
    "ncm": "123456788",
    "description": "Descrição detalhada do produto",
    "exception": "01",
    "nve": "01",
    "fabricante": "fábrica Nexa",
    "endereco": "av pequim",
    "pais": "China",
    "confidence_score": 0.98
  }
}
```

- **status:** `"done"` ao finalizar.
- **result:** Objeto com os dados classificados.

### 3. Falha no Processamento

```json
{
  "status": "failed",
  "job_id": "job-ajgldfgsaerg",
  "error": "Descrição do erro"
}
```

- **status:** `"failed"` em caso de erro.
- **error:** Mensagem detalhando o erro.

---

## Exemplo de Fluxo de Integração

1. **API Gateway** envia um POST para `/process/single_partnumber` com o canal Redis desejado.
2. **Nexa-AI-Agents** responde com `job_id` e inicia o processamento em background.
3. **API Gateway** escuta o canal Redis informado:
   - Recebe mensagens de progresso (`status: processing`).
   - Recebe mensagem final de sucesso (`status: done`) ou falha (`status: failed`).

---

## Configuração de Ambiente

- **Redis:** Certifique-se de que o container Docker do Redis está rodando e acessível via `localhost:6379`.
- **API Gateway:** Configure para acessar o Nexa-AI-Agents via HTTP em `http://localhost:5001/process/single_partnumber` e o Redis em `localhost:6379`.
- **Nexa-AI-Agents:** Execute diretamente no host (não em Docker) para máxima performance.

---

## Observações Importantes

- O canal Redis deve ser único por job para evitar colisão de mensagens entre jobs concorrentes.
- O serviço não implementa autenticação; recomenda-se rodar em rede interna segura.
- O payload de resposta e as mensagens Redis seguem rigorosamente os schemas definidos acima. Qualquer alteração deve ser comunicada a todo o time.
