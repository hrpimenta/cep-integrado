# 🚀 Projeto: Integração Resiliente com Kong, n8n, RabbitMQ, PostgreSQL e Worker Python

Este projeto demonstra uma arquitetura moderna de integração pensada para ambientes corporativos que exigem **resiliência**, **orquestração de processos**, **desacoplamento** e **facilidade de manutenção**.

---

## 🎯 Objetivo da Arquitetura

Muitas integrações em sistemas legados ocorrem de forma direta, sem pontos de entrada bem definidos, com baixo controle de falhas e sem visibilidade. Esta arquitetura foi proposta para resolver exatamente esse cenário com uma estrutura simples, porém robusta, rodando 100% local via Docker.

---

## 🧱 Componentes da Arquitetura e Justificativas

| Componente   | Função                                                                 |
|--------------|------------------------------------------------------------------------|
| **Kong**     | Gateway de API que centraliza chamadas externas, controla acessos e fornece observabilidade e resiliência às APIs. Aqui ele expõe o endpoint `/consulta-cep` publicamente. |
| **n8n**      | Ferramenta low-code para orquestração de workflows. Permite criar integrações com lógica de negócios sem codificação. Aqui ele orquestra a requisição ao ViaCEP e o envio à fila. |
| **RabbitMQ** | Broker de mensagens que desacopla o processamento assíncrono. Garante que dados não sejam perdidos e que possam ser processados com resiliência. |
| **Worker (Python)** | Serviço leve que consome mensagens do RabbitMQ e processa de forma isolada, com possibilidade de escalar e reaproveitar lógica de negócio de forma desacoplada. |
| **PostgreSQL** | Banco de dados relacional utilizado para persistir os dados normalizados dos CEPs. |
| **Docker Compose** | Orquestração local dos serviços para facilitar testes, desenvolvimento e demonstrações. |

---

## 📁 Estrutura do Projeto

```
cep-integrado/
├── app/
│   ├── Dockerfile
│   └── worker.py
├── cep-workflow.json
├── docker-compose.yml
└── README.md
```

---

## 🚀 Como Executar

1. Clone este repositório
2. No terminal:

```bash
docker-compose up -d --build
```

3. Acesse os serviços:

- n8n: http://localhost:5678 (login: `admin` / `adminpass`)
- RabbitMQ: http://localhost:15672 (login: `guest` / `guest`)
- Kong Admin: http://localhost:8001
- Endpoint da API via Kong: `POST http://localhost:8000/consulta-cep`

---

## 🔁 Fluxo da Requisição

1. A requisição chega via **Kong** na rota `/consulta-cep`
2. O **n8n** recebe via Webhook, consulta a API pública do **ViaCEP**
3. A resposta da API é enviada como mensagem para o **RabbitMQ**
4. O **Worker Python** consome a mensagem da fila `cep_queue`
5. O Worker grava os dados no banco **PostgreSQL**

---

## 📦 Teste com Postman

Faça um `POST` para `http://localhost:8000/consulta-cep` com o corpo:

```json
{
  "cep": "01001000"
}
```

---

## 🧠 Motivação e Benefícios

- 🔗 **Desacoplamento** entre orquestração e execução
- ♻️ **Reusabilidade** de componentes
- 🧩 **Flexibilidade** com n8n para ajustes sem código
- 📊 **Observabilidade** e **pontos de entrada únicos**
- 🔁 **Escalabilidade** futura com filas
- 💥 **Resiliência** com retry em falhas

---

## 📥 Importar o Workflow

1. Acesse o n8n em http://localhost:5678
2. Clique em **"Import"** e selecione `cep-workflow.json`

---

## 🛠 Estrutura recomendada no banco de dados

```sql
CREATE TABLE ceps (
  id SERIAL PRIMARY KEY,
  cep VARCHAR(10),
  logradouro TEXT,
  bairro TEXT,
  localidade TEXT,
  uf TEXT
);
```

---

## 🙌 Autor

Criado por **Henrique** com apoio do ChatGPT — ideal para testes locais de arquiteturas modernas com foco em mensageria e automação de processos.

---