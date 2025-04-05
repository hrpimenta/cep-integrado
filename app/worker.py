import pika
import json
import psycopg2
import time

# Tentativa de conexão ao RabbitMQ com retries
max_retries = 10
connected = False

for attempt in range(max_retries):
    try:
        print(f"🔄 Tentando conectar ao RabbitMQ... (tentativa {attempt + 1})")
        rabbit_conn = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        channel = rabbit_conn.channel()
        channel.queue_declare(queue="cep_queue")
        connected = True
        print("✅ Conectado ao RabbitMQ!")
        break
    except pika.exceptions.AMQPConnectionError:
        print("❌ Não foi possível conectar ao RabbitMQ. Aguardando 5s...")
        time.sleep(5)

if not connected:
    print("❌ Erro fatal: não foi possível conectar ao RabbitMQ após várias tentativas.")
    exit(1)

# Conexão com o banco de dados PostgreSQL
pg_conn = psycopg2.connect(
    host="db",
    database="cepdata",
    user="test",
    password="test"
)
cur = pg_conn.cursor()

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("📬 Mensagem recebida:", data)

    cur.execute(
        "INSERT INTO ceps (cep, logradouro, bairro, localidade, uf) VALUES (%s, %s, %s, %s, %s)",
        (
            data.get("cep"),
            data.get("logradouro"),
            data.get("bairro"),
            data.get("localidade"),
            data.get("uf"),
        ),
    )
    pg_conn.commit()
    print("💾 Gravado no banco!")

channel.basic_consume(queue="cep_queue", on_message_callback=callback, auto_ack=True)
print("👂 Aguardando mensagens na fila 'cep_queue'...")
channel.start_consuming()