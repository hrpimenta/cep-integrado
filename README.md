
# 🚀 Ambiente de Integração com Kong, n8n, RabbitMQ, PostgreSQL e Worker Python

Este projeto demonstra uma arquitetura moderna de integração baseada em:
- Gateway de API com **Kong**
- Orquestração de fluxos com **n8n**
- Comunicação assíncrona com **RabbitMQ**
- Processamento com **Worker em Python**
- Persistência com **PostgreSQL**

---

## 📁 Estrutura do projeto

```
cep-integrado/
├── app/
│   ├── worker.py
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Componentes

| Serviço     | Porta         | Função                                 |
|-------------|---------------|----------------------------------------|
| Kong        | 8000 (proxy)  | Entrada de requisições HTTP            |
| Kong Admin  | 8001          | Configuração do Kong via Admin API     |
| n8n         | 5678          | Orquestração de workflows              |
| RabbitMQ    | 5672 / 15672  | Mensageria e painel de controle        |
| PostgreSQL  | interno       | Armazena dados de CEPs                 |
| Worker      | -             | Escuta fila e grava dados no banco     |

---

## 🚀 Como iniciar

1. Clone ou baixe este projeto.
2. Rode o ambiente com:

```bash
docker-compose up -d --build
```

3. Acesse os serviços:

- n8n: http://localhost:5678 (login: admin / adminpass)
- RabbitMQ: http://localhost:15672 (guest / guest)
- Kong Admin: http://localhost:8001
- Endpoint API (via Kong): POST http://localhost:8000/consulta-cep

---

## 🧪 Testando a integração

1. Faça um POST com o corpo:

```json
{
  "cep": "01001000"
}
```

2. O fluxo será:
```
Postman → Kong → n8n → ViaCEP → RabbitMQ → Worker → PostgreSQL
```

3. Verifique o resultado no banco de dados:

```bash
docker exec -it cep-integrado-db-1 psql -U test -d cepdata
SELECT * FROM ceps;
```

---

## 🙌 Créditos

Criado por Henrique com apoio do ChatGPT — arquitetura baseada em microserviços e eventos, com foco em testes locais e mensageria resiliente.
